from pydantic import BaseModel, Field, validator
from typing import Union, Optional, List, Any, Dict
from enum import Enum
import datetime

# Enums for type specifications
class DataSourceType(str, Enum):
    FILE = "file"
    INTERNAL = "internal"

class DataFormat(str, Enum):
    JSON = "json"
    CSV = "csv"

class AttributeType(str, Enum):
    TIME = "time"
    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    TEXT = "text"

class SubType(str, Enum):
    STRING = "string"
    FLOAT = "float"
    INT = "int"

class TimeType(str, Enum):
    TIME = "time"
    FLOAT = "float"
    INT = "int"

class WindowUnit(str, Enum):
    SAMPLES = "samples"
    NUMERIC = "numeric"
    SEC = "sec"
    MIN = "min"
    HOUR = "hour"
    DAY = "day"

class OperationType(str, Enum):
    TIME_SHIFT = "timeShift"
    TIME_DELTA = "timeDelta"
    LIN_TREND = "linTrend"

# Data Source Definitions
class DataSource(BaseModel):
    type: DataSourceType
    format: DataFormat
    fileName: Optional[str] = None
    data: Optional[Union[str, List[str], List[Dict]]] = None

# Attribute Specifications
class Attribute(BaseModel):
    name: str
    type: AttributeType
    source: str = "input"
    sourceName: Optional[str] = None
    label: Optional[str] = None
    distWeight: Optional[float] = None
    subType: Optional[SubType] = None
    timeType: Optional[TimeType] = None

# Operation Specification
class Operation(BaseModel):
    op: OperationType
    inAttr: str
    outAttr: str
    windowUnit: WindowUnit
    windowSize: Union[int, float]
    timeAttr: Optional[str] = None

# Configurations
class Config(BaseModel):
    numInitialStates: int
    numHistogramBuckets: int
    attributes: List[Attribute]
    ops: List[Operation]
    decTree_maxDepth: Optional[int]
    decTree_minNormInfGainToSplit: Optional[float]
    decTree_minEntropyToSplit: Optional[float] = None
    ignoreConversionErrors: bool = True
    distWeightOutliers: Optional[float] = 0.05
    includeHistograms: bool = True
    includeDecisionTrees: bool = True
    includeStateHistory: bool = True

# Model Response and Related Structures
class Histogram(BaseModel):
    attrName: str
    freqSum: int
    freqs: List[int] = []
    bounds: Optional[List[float]] = None
    keys: Optional[List[Union[str, int]]] = None
    dayOfWeekFreqs: Optional[List[int]] = None
    monthFreqs: Optional[List[int]] = None
    hourFreqs: Optional[List[int]] = None

class DecisionTreeNode(BaseModel):
    nPos: int
    nNeg: int
    splitAttr: Optional[str] = None
    splitLabel: Optional[str] = None
    children: List['DecisionTreeNode'] = Field(default_factory=list)
    entropyBeforeSplit: float = 0.0
    splitCost: Optional[float] = None
    entropyAfterSplit: Optional[float] = None
    infGain: Optional[float] = None
    normInfGain: Optional[float] = None

class SuggestedLabel(BaseModel):
    label: str
    nCoveredInState: int
    nCoveredOutsideState: int
    nNotCoveredInState: int
    nNotCoveredOutsideState: int
    logOddsRatio: float

class State(BaseModel):
    stateNo: int
    initialStates: List[int]
    childStates: Optional[List[int]] = None
    parentState: Optional[int] = None
    sameAsParent: bool = False
    centroid: Optional[List[Dict]] = None
    stationaryProbability: Optional[float] = None
    nMembers: Optional[int] = None
    nextStateProbDistr: Optional[List[float]] = None
    histograms: Optional[List[Histogram]] = None
    xCenter: Optional[float] = None
    yCenter: Optional[float] = None
    radius: Optional[float] = None
    suggestedLabel: Optional[SuggestedLabel] = None
    decisionTree: Optional[DecisionTreeNode] = None

class Scale(BaseModel):
    nStates: int
    areTheseInitialStates: bool
    states: List[State]

class Column(BaseModel):
    name: str
    distWeight: float

class Dataset(BaseModel):
    cols: List[Column]

class Model(BaseModel):
    scales: List[Scale]
    totalHistograms: List[Histogram]
    stateHistoryTimes: List[float]
    stateHistoryInitialStates: List[int]
    config: Config
    dataset: Dataset

class ModelInfo(BaseModel):
    uuid: str
    username: str
    name: str
    description: Optional[str]
    dataset: str
    online: bool
    active: bool
    public: bool
    createdAt: datetime.datetime = Field(default_factory=datetime.datetime.now)
    model: Optional[Model] = None

    @validator('createdAt', pre=True, always=True)
    def convert_timestamp(cls, v):
        return datetime.datetime.fromtimestamp(v / 1000) if isinstance(v, (int, float)) else v

    # Additional validators can be added here.

class Response(BaseModel):
    status: str
    errors: List[str]
    model: Optional[Model] = None

class BuildModelRequest(BaseModel):
    dataSource: DataSource
    config: Config

class ClassifySamplesRequest(BaseModel):
    dataSource: DataSource
    model: Model
