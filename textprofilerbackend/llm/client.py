import openai
from openai import AsyncOpenAI
import json
import asyncio
from tqdm.asyncio import tqdm_asyncio

from textprofilerbackend.utils import timeit
from textprofilerbackend.models import TaskFormat

# Note - json mode only works with these two model names
# MODEL_NAME = "gpt-4-turbo-preview"
MODEL_NAME = "gpt-3.5-turbo"


################ PROMPT 1: For getting the json representation of the response format
PROMPT_GET_JSON_FORMAT = """# Instruction
You are a data processing assistant. You will be helping a user transform a text column by extracting the requested information and turning it into new columns. To do this, we need to know the JSON specification of the requested columns. Given a user instruction, return the following information about the columns that will be generated to help answer that question.

# Response format
The response should be an object with three keys:
1. "name": the column name
1. "type": the response type of either "number", "string", or "bool"
2. "num_replies": if the response will be a "single" item or "multiple" items

# Examples
-----
- Instruction: 
Extract all email addresses from the given text string.
- JSON format: 
{ "name": "email_addresses", "type": "string", "num_replies": "multiple" }
-----
- Instruction: 
Summarize this document
- JSON format: 
{ "name": "summary", "type": "string", "num_replies": "single" }
-----
- Instruction: 
Extract the salary from this job posting
- JSON format: 
{ "name": "salaries", "type": "number", "num_replies": "single" }
-----
- Instruction: 
keywords about each study
- JSON format: 
{ "name": "keywords", "type": "string", "num_replies": "multiple" }
-----
"""

################ Prompt 2: generic transform prompt when we don't have any examples
PROMPT_GET_RESULT_NO_EXAMPLE = """# Overall Description
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
- Response JSON format: 
{ "salary": { "type": "number", "num_replies": "single" } }
- Text:
Hello there! We are looking for a new employee to join our team. The salary is $50,000 per year.
- Response:
{ "salary": 50000 }
-----
- Instruction: 
keywords about each study
- Response JSON format: 
{
  "keywords": { "type": "string", "num_replies": "multiple" },
}
- Text:
In this paper we discuss a study on caffeine and its effect on sleep. We ran a comparative study with 48 participants across 3 age groups. Each participants consumed caffeine or a placebo
and then we measured how long it took them to fall asleep they slept. We found that on average, participants in the caffeine group took 30 minutes longer to fall asleep than the placebo group.
- Response:
{ "keywords": ["caffeine", "sleep", "comparative study"] }
-----
"""


def format_user_prompt_generic(
    user_task_description: str, response_format: dict, document: str
):
    return f"""- Instruction: 
{user_task_description}
- Response format: 
{json.dumps(response_format)}
- Text: 
{document}
- Response:
"""


################ Prompt 3: Use examples to construct prompt if we have them
PROMPT_W_EXAMPLES_BASE = """# Overall Description
You are a data processing assistant. I am going to give you a piece of text and a description of what to extract, and I need you to extract the data for me as JSON.  If you are not confident the data is actually present, then return empty JSON.

# Format
Extract the specified data according to the format and task below and return a valid JSON object with only double quoted strings.
"""


def get_prompt_w_examples(
    user_task_description: str,
    response_format: dict,
    example_data: list,
    example_responses: list,
):
    """
    Args:
        response_format (dict): { "name": "<name>", "type": "<number|string|bool>", "num_replies": "<single|multiple>" }
        example_data (list): list of strings
        example_responses (list): list of dicts like [{"<name>": <value>}]
    """
    prompt = PROMPT_W_EXAMPLES_BASE
    prompt += f"""The response should look like:
{json.dumps(response_format)}

# Extraction Task
{user_task_description}

# Examples
-----
"""
    for d, r in zip(example_data, example_responses):
        prompt += f"- Text: \n{d}\n- Response:\n{json.dumps(r)}\n-----\n"

    print("\n\n[get_prompt_w_examples] the prompt is:::::\n\n", prompt)
    return prompt


def format_user_prompt(document):
    return f"- Text: \n{document}\n- Response:\n"


class LLMClient:
    def __init__(
        self,
    ):
        print("Making new LLMClient")
        self.client = AsyncOpenAI()  # reads API key from env

    ##### ASYNC QUERY FUNCTIONS
    async def _get_format_async(self, instruction):
        """
        Get the response format in JSON. Try twice with timeout and return None if it fails.
        """
        for tryIdx in range(2):
            try:
                response = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=MODEL_NAME,
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": PROMPT_GET_JSON_FORMAT},
                            {"role": "user", "content": instruction},
                        ],
                        temperature=0,
                    ),
                    timeout=10,
                )
                content = response.choices[0].message.content
                r = json.loads(content)
                # TODO use pydantic to validate here
                return r
            except asyncio.TimeoutError:
                print(
                    f"[Get Format]\tTry {tryIdx}: Operation timed out after 10 seconds"
                )
                continue

        return None

    async def _do_transform_retry(self, id, system_prompt, user_prompt):
        """
        Get the transformation response from OpenAI API. Retry twice if rate limited.
        """
        print(f"[RQ {id}]\tGetting response...")

        sleepAmount = [10, 60]

        for tryIdx in range(len(sleepAmount)):
            try:
                r = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=MODEL_NAME,
                        response_format={"type": "json_object"},
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {
                                "role": "user",
                                "content": user_prompt,
                            },
                        ],
                    ),
                    timeout=10,
                )
                return r
            except asyncio.TimeoutError:
                print(f"[RQ {id}]\tTry {tryIdx}: Operation timed out after 10 seconds")
                continue  # Skip to the next iteration
            except openai.RateLimitError as e:
                print(
                    f"[RQ {id}]\tTry {tryIdx}: Rate limit error, waiting for ",
                    sleepAmount[tryIdx],
                )
                await asyncio.sleep(sleepAmount[tryIdx])

            except Exception as e:
                print(f"[RQ {id}]\tTry {tryIdx}: ERROR: ", e)
                return None

        print(f"[RQ {id}]\tFailed to get response after {len(sleepAmount)} tries")
        return None

    async def _run_transform_generic_parallel(
        self, system_prompt, documents, user_task_description, response_format
    ):
        responses = await tqdm_asyncio.gather(
            *[
                self._do_transform_retry(
                    idx,
                    system_prompt,
                    format_user_prompt_generic(
                        user_task_description, response_format, d
                    ),
                )
                for idx, d in enumerate(documents)
            ]
        )

        return responses

    async def _run_transform_w_examples_parallel(self, system_prompt, documents):
        responses = await tqdm_asyncio.gather(
            *[
                self._do_transform_retry(idx, system_prompt, format_user_prompt(d))
                for idx, d in enumerate(documents)
            ]
        )

        return responses

    def parse_results(self, responses):
        """
        Parses the results as JSON from a list of responses. Expects a list of openai.ChatCompletion objects.
        """
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
    def get_response_format(self, user_task_description: str) -> dict:
        """
        Get the response format for a given user task description.

        Args:
            user_task_description (str): The description of the user's task.

        Returns:
            dict: The response format in form { "name": "<name>", "type": "<number|string|bool>", "num_replies": "<single|multiple>" }
        """
        response_format = asyncio.run(self._get_format_async(user_task_description))
        return response_format

    @timeit
    def get_transformations(
        self,
        user_task_description: str,
        response_format: TaskFormat,
        data: list,
        example_data=None,
        example_responses=None,
    ):
        """
        Runs transformation in parallel based on the given parameters.

        Args:
            user_task_description (str): The description of the user's task.
            response_format: TaskFormat
            data (list): The input data for the transformations.
            example_data (list of strings, optional): The example data for the transformations
            example_response (list, optional): The example response for the transformations. Expects data in dict with similar format to Task Format of {"<col_name": <value> }

        Returns:
            list: The parsed results of the transformations.
        """

        formatted_response_format = {
            response_format.name: {
                "type": response_format.type,
                "num_replies": response_format.num_replies,
            }
        }

        if example_data and example_responses:
            print("Running example based transformations...")
            system_prompt = get_prompt_w_examples(
                user_task_description,
                formatted_response_format,
                example_data,
                example_responses,
            )
            raw_results = asyncio.run(
                self._run_transform_w_examples_parallel(system_prompt, data)
            )

        else:
            print("Running generic transformations...")
            system_prompt = PROMPT_GET_RESULT_NO_EXAMPLE
            raw_results = asyncio.run(
                self._run_transform_generic_parallel(
                    system_prompt,
                    data,
                    user_task_description,
                    formatted_response_format,
                )
            )

        parsed_results = self.parse_results(raw_results)

        return parsed_results


def mainTesting():
    print("\n\n\n~~~~~~~~~~~~~~~~~~~ Starting Run.... ~~~~~~~~~~~~~~~~~~~")
    import pandas as pd

    llm_client = LLMClient()

    df = pd.read_parquet(
        "/Users/wepperso/workspaces/Research/TextProfileAll/TextProfiler/textprofilerbackend/.textprofiler_cache/raw_data/vis_papers/vis_papers.parquet"
    )

    df = df[(df.umap_x > 10.5) & (df.umap_y < 10)]

    gt = ["basketball", "racket", "basketball"]

    data = df.Abstract.tolist()
    user_prompt = "Which sport does this abstract have to do with? If multiple mentioned pick the main sport and if it does not have to do with sports then reply with None."

    # STEP 1: get response format
    response_format = TaskFormat(name="sport_name", type="string", num_replies="single")
    print("Generated response format:", response_format)

    #### VERSION 1: GENERIC RESPONSE
    # call1Data = data[3:]
    # response = llm_client.get_transformations(user_prompt, response_format, call1Data)
    # df_response = pd.DataFrame(response, columns=[response_format["name"]])
    # df_response["data"] = call1Data

    # print("Generic response:", df_response)

    #### VERSION 2: EXAMPLE RESPONSE
    call2Data = data
    call2DataExamples = data[:3]
    call2ExResponses = [
        {"sport_name": "basketball"},
        {"sport_name": "racket"},
        {"sport_name": "basketball"},
    ]

    response2 = llm_client.get_transformations(
        user_prompt,
        response_format,
        call2Data,
        call2DataExamples,
        call2ExResponses,
    )

    df_response2 = pd.DataFrame(response2, columns=[response_format.name])

    df_response2.to_parquet("RESULT.parquet")

    print("Example response:", df_response2)

    breakpoint()
    print("<|endoftext|>")


# if __name__ == "__main__":
#     mainTesting()
