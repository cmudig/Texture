from process_gpt import LLMClient
import pandas as pd

if __name__ == "__main__":
    print("Starting run")
    client = LLMClient()

    # Get data
    df = pd.read_parquet(
        "/Users/wepperso/workspaces/Research/TextProfileAll/TextProfiler/textprofilerbackend/.textprofiler_cache/raw_data/vis_papers_sample/vis_papers.parquet"
    )
    data = df.Abstract.iloc[:5]

    # user_prompt = "Extract the number of participants in the user study, if any. If none specified then return 0"
    user_prompt = "Extract 3 - 5 keywords per abstract"
    # user_prompt = "Summarize with one sentence."
    # user_prompt = (
    #     "Did this paper run a user study with real participants? Reply True or False."
    # )
    # user_prompt = "Is this paper related to accessibility? Reply Yes, No, or Maybe."

    task_format = client.get_response_format(user_prompt)
    print("Format: ", task_format)

    results = client.get_transformations(user_prompt, task_format, data)

    print("results: ", results)
