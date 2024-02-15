import openai
from openai import AsyncOpenAI
import json
import asyncio

from textprofilerbackend.utils import timeit


PROMPT_GET_JSON_FORMAT = """# Instruction
You are a data processing assistant. You will be helping a user transform a text column by extracting the requested information and turning it into new columns. To do this, we need to know the JSON specification of the requested columns. Given a user instruction, return the following information about the columns that will be generated to help answer that question.

# Response format
The response should be an object where the keys are the column names that map to an object with two keys
1. "type": the response type of either "number", "string", or "bool"
2. "num_replies": if the response will be a "single" item or "multiple" items

# Examples
-----
- Instruction: 
Extract all email addresses from the given text string.
- JSON format: 
{ "email_addresses": { "type": "string", "num_replies": "multiple" } }
-----
- Instruction: 
Summarize this document
- JSON format: 
{ "summary": { "type": "string", "num_replies": "single" } }
-----
- Instruction: 
Extract the salary from this job posting
- JSON format: 
{ "salaries": { "type": "number", "num_replies": "single" } }
-----
- Instruction: 
keywords about each study, the number of participants in the study, and if the study was successful 
- JSON format: 
{
  "keywords": { "type": "string", "num_replies": "multiple" },
  "num_participants": { "type": "number", "num_replies": "single" },
  "study_success": { "type": "string", "num_replies": "single" }
}
-----
"""

PROMPT_GET_RESULT = """# Overall Description
You are a data processing assistant. I am going to give you a piece of text and a description of what to extract, and I need you to extract the data for me.  If you are not confident the data is actually present, then return empty JSON.

# Format
Extract the specified data from the given piece of text and return it in the requested JSON format. If multiple things are requested, then separate them into separate keys. The response must be valid JSON and only contain double quoted strings.

# Examples
-----
- Instruction: 
Extract all email addresses from the given text string.
- Response JSON format: 
{ "email_addresses": { "type": "string", "num_replies": "multiple" } }
- Text:
Please email me at username@gmail.com or myotheremail@uni.edu.
- Response:
{ "email_addresses": ["username@gmail.com", "myotheremail@uni.edu"] }
-----
- Instruction: 
Extract the salary from this job posting
- JSON format: 
{ "salary": { "type": "number", "num_replies": "single" } }
- Text:
Hello there! We are looking for a new employee to join our team. The salary is $50,000 per year.
- Response:
{ "salary": 50000 }
-----
- Instruction: 
keywords about each study and the number of participants in the study
- JSON format: 
{
  "keywords": { "type": "string", "num_replies": "multiple" },
  "num_participants": { "type": "number", "num_replies": "single" },
}
- Text:
In this paper we discuss a study on caffeine and its effect on sleep. We ran a comparative study with 48 participants across 3 age groups. Each participants consumed caffeine or a placebo
and then we measured how long it took them to fall asleep they slept. We found that on average, participants in the caffeine group took 30 minutes longer to fall asleep than the placebo group.
- Response:
{
  "keywords": ["caffeine", "sleep", "comparative study"],
  "num_participants": 48,
}
-----
"""


def format_query(instruction, format, document):
    return f"""- Instruction: 
{instruction}
- JSON format: 
{format}
- Text: 
{document}
- Response:
"""


######## SERIAL QUERYING ########

# def make_processing_requests_serial(instruction, documents, task_format):

#     responses = []
#     for d in tqdm(documents):
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo-0125",
#             response_format={"type": "json_object"},
#             messages=[
#                 {"role": "system", "content": PROMPT_GET_RESULT},
#                 {"role": "user", "content": format_query(instruction, task_format, d)},
#             ],
#         )
#         content = response.choices[0].message.content
#         r = json.loads(content)
#         responses.append(r)

#     return responses


class LLMClient:
    def __init__(
        self,
    ):
        print("Making new LLMClient")
        self.client = AsyncOpenAI()  # reads API key from env

    ##### ASYNC QUERY FUNCTIONS
    async def _get_format_async(self, instruction):
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": PROMPT_GET_JSON_FORMAT},
                {"role": "user", "content": instruction},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content
        r = json.loads(content)
        return r

    async def _get_transform_retry(self, id, instruction, document, task_format):
        """
        Get the transformation response from OpenAI API. Retry twice if rate limited.
        """

        sleepAmount = [10, 60]

        for tryIdx in range(len(sleepAmount)):
            try:
                r = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": PROMPT_GET_RESULT},
                        {
                            "role": "user",
                            "content": format_query(instruction, task_format, document),
                        },
                    ],
                )
                return r
            except openai.RateLimitError as e:
                print(
                    f"[RQ {id}]\tTry {tryIdx}: Rate limit error, waiting for ",
                    sleepAmount[tryIdx],
                )
                await asyncio.sleep(sleepAmount[tryIdx])

        print(f"[RQ {id}]\tFailed to get response after {len(sleepAmount)} tries")
        return None

    async def _run_parallel(self, instruction, documents, task_format):
        # limiter = aiolimiter.AsyncLimiter(MAX_REQUESTS_PER_MINUTE)

        # issue parallel queries
        responses = await asyncio.gather(
            *[
                self._get_transform_retry(idx, instruction, d, task_format)
                for idx, d in enumerate(documents)
            ]
        )

        # parse results
        processed_results = []
        for response in responses:
            if response:
                item = response.choices[0].message.content
                try:
                    r = json.loads(item)
                except Exception as e:
                    try:
                        print("Bad initial json, trying to fix")
                        item = item.replace("'", '"')
                        r = json.loads(item)
                    except Exception as e:
                        print("Error parsing JSON: ", e)
                        r = item
            else:
                r = None

            processed_results.append(r)

        return processed_results

    ##### PUBLIC SYNC QUERY FUNCTIONS
    @timeit
    def get_response_format(self, user_prompt):
        task_format = asyncio.run(self._get_format_async(user_prompt))
        return task_format

    @timeit
    def get_transformations(self, user_prompt, task_format, data):
        response = asyncio.run(self._run_parallel(user_prompt, data, task_format))

        return response
