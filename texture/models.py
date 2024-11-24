from typing import List, Dict, Union, Literal, Any, Optional
from pydantic import BaseModel


#### Internal API models between frontend and backend

DataType = Literal["text", "number", "date", "categorical"]


class DerivedSchema(BaseModel):
    is_segment: bool  # corresponds to a segment of a text col
    table_name: Optional[str] = None  # table name for this data
    derived_from: Optional[str] = None  # name of col derived from
    derived_how: Optional[Literal["model", "code"]] = None


class Column(BaseModel):
    name: str
    type: DataType
    derivedSchema: Optional[DerivedSchema] = None
    extra: Optional[Dict[str, Any]] = None


class DatasetSchema(BaseModel):
    name: str
    columns: List[Column]
    primary_key: Column
    origin: Literal["example", "uploaded"]
    has_embeddings: bool = False
    has_projection: bool = False
    search_result: Optional[Column] = None


class ColumnSummary(BaseModel):
    column_name: str
    column_type: str
    min: str
    max: str
    approx_unique: str
    avg: str = None
    std: str = None
    q25: str = None
    q50: str = None
    q75: str = None
    count: int
    null_percentage: str


class DuckQueryData(BaseModel):
    uuid: str
    sql: str
    type: Literal["arrow", "exec", "json"]
    buffers: list = []


class ErrorResponse(BaseModel):
    uuid: str
    type: Literal["error"] = "error"
    error: str


class ExecResponse(BaseModel):
    uuid: str
    type: Literal["exec"] = "exec"


class JsonResponse(BaseModel):
    uuid: str
    type: Literal["json"] = "json"
    result: Union[List, Dict]  # any valid JSON


DuckQueryResult = Union[ExecResponse, JsonResponse, ErrorResponse]


class DatasetUploadResponse(BaseModel):
    success: bool
    message: str
    datasetSchema: DatasetSchema = None


class DatasetVerifyResponse(BaseModel):
    success: bool
    message: str


class DatasetTokenizeResponse(BaseModel):
    success: bool
    message: str


class VectorSearchResponse(BaseModel):
    success: bool
    result: List[Dict[str, Any]]


class TransformResponse(BaseModel):
    success: bool
    result: Union[List, Dict]


# TODO rename this to TranformSchema
class TaskFormat(BaseModel):
    name: str
    type: Literal["number", "string", "bool"]
    num_replies: Literal["single", "multiple"]


class LLMTransformRequest(BaseModel):
    userPrompt: str
    taskFormat: TaskFormat
    columnData: List[str]
    exampleData: Optional[List[str]] = None
    exampleResponse: Optional[List[Dict[str, Any]]] = (
        None  # list of strings, numbers, or bools
    )


class LLMTransformCommit(BaseModel):
    userPrompt: str
    taskFormat: TaskFormat
    columnName: str
    tableName: str
    exampleData: List[str]
    exampleResponse: List[Dict[str, Any]]
    applyToIndices: List[int]


class CodeTransformRequest(BaseModel):
    codeString: str
    taskFormat: TaskFormat
    columnData: List[str]


class CodeTransformCommit(BaseModel):
    codeString: str
    taskFormat: TaskFormat
    columnName: str
    tableName: str
    applyToIndices: List[int]


#### public API for running


DataFrameType = Any  # Future: make sure this is pd.DataFrame or huggingface dataset
