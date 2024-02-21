from typing import List, Dict, Union, Literal, Any, Optional
from pydantic import BaseModel

DataType = Literal["text", "number", "date", "categorical"]


class Column(BaseModel):
    name: str
    type: DataType
    associated_text_col_name: Optional[str] = None


class JoinInfo(BaseModel):
    joinDatasetName: str
    joinKey: str
    joinColumn: Column


class DatasetInfo(BaseModel):
    name: str
    column_info: List[Column]
    origin: Literal["example", "uploaded"]
    joinDatasetInfo: Optional[JoinInfo] = None
    primary_key: Column


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
    datasetSchema: DatasetInfo = None


class DatasetVerifyResponse(BaseModel):
    success: bool
    message: str


class DatasetTokenizeResponse(BaseModel):
    success: bool
    message: str


class VectorSearchResponse(BaseModel):
    success: bool
    result: List[Dict[str, Any]]


class LLMResponse(BaseModel):
    success: bool
    result: Union[List, Dict]


class LLMTransformRequest(BaseModel):
    userPrompt: str
    taskFormat: str
    columnData: List[str]


class LLMTransformCommit(BaseModel):
    userPrompt: str
    taskFormat: str
    columnName: str
    tableName: str
    newColumnName: str
