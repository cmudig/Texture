from typing import List, Dict, Union, Literal
from pydantic import BaseModel

DataType = Literal["text", "number", "date", "categorical"]


class Column(BaseModel):
    name: str
    type: DataType


class QualityInfo(BaseModel):
    type: str
    text_column: Column
    plot_columns: List[Column] = []


class DatasetMetadata(BaseModel):
    text_columns: List[Column]
    other_columns: List[Column]
    text_meta_columns: Dict[str, List[Column]]
    text_quality_info: List[QualityInfo] = []


class DatasetInfo(BaseModel):
    name: str
    filename: str
    metadata: DatasetMetadata


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
