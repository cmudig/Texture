from textprofilerbackend.models import DatasetInfo

dataset_vis_papers = DatasetInfo(
    name="vis_papers",
    primary_key={"name": "id", "type": "number"},
    joinDatasetInfo={
        "joinDatasetName": "vis_papers_words",
        "joinKey": "id",
        "joinColumn": {
            "name": "word",
            "type": "text",
            "associated_text_col_name": "Abstract",
        },
    },
    origin="example",
    column_info=[
        {
            "name": "id",
            "type": "number",
        },
        {
            "name": "Abstract",
            "type": "text",
        },
        {
            "name": "Title",
            "type": "categorical",
        },
        {
            "name": "Conference",
            "type": "categorical",
        },
        {
            "name": "AuthorNames-Deduped",
            "type": "categorical",
        },
        {
            "name": "AuthorKeywords",
            "type": "categorical",
        },
        {
            "name": "Abstract_text_length",
            "type": "number",
            "associated_text_col_name": "Abstract",
        },
        {
            "name": "MODEL_num_participants",
            "type": "number",
            # "associated_text_col_name": "Abstract",
        },
        {
            "name": "MODEL_keywords",
            "type": "categorical",
            # "associated_text_col_name": "Abstract",
        },
        {
            "name": "MODEL_summary",
            "type": "text",
            # "associated_text_col_name": "Abstract",
        },
        {
            "name": "MODEL_has_user_study",
            "type": "categorical",
            # "associated_text_col_name": "Abstract",
        },
        # {
        #     "name": "DOI",
        #     "type": "categorical",
        # },
        # {
        #     "name": "Link",
        #     "type": "categorical",
        # },
        # {
        #     "name": "FirstPage",
        #     "type": "number",
        # },
        # {
        #     "name": "LastPage",
        #     "type": "number",
        # },
        # {
        #     "name": "AuthorNames",
        #     "type": "categorical",
        # },
        # {
        #     "name": "AuthorAffiliation",
        #     "type": "categorical",
        # },
        # {
        #     "name": "InternalReferences",
        #     "type": "categorical",
        # },
        #
        # {
        #     "name": "Year",
        #     "type": "number",
        # },
        # {
        #     "name": "PaperType",
        #     "type": "categorical",
        # },
        # {
        #     "name": "AminerCitationCount",
        #     "type": "number",
        # },
        # {
        #     "name": "CitationCount_CrossRef",
        #     "type": "number",
        # },
        # {
        #     "name": "PubsCited_CrossRef",
        #     "type": "number",
        # },
        # {
        #     "name": "Award",
        #     "type": "categorical",
        # },
        # {
        #     "name": "Abstract_num_words",
        #     "type": "number",
        #     "associated_text_col_name": "Abstract",
        # },
        # {
        #     "name": "Abstract_max_word_length",
        #     "type": "number",
        #     "associated_text_col_name": "Abstract",
        # },
        # {
        #     "name": "Abstract_avg_word_length",
        #     "type": "number",
        #     "associated_text_col_name": "Abstract",
        # },
        # {
        #     "name": "Abstract_perc_special_chars",
        #     "type": "number",
        #     "associated_text_col_name": "Abstract",
        # },
    ],
)


EXAMPLE_DATASETS = [
    dataset_vis_papers,
]
