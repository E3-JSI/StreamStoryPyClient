from pydantic import BaseModel, Field, validator
from typing import Union, Optional, List, Any, Dict
from enum import Enum
import datetime


# Data Source Definitions
class DataSource(BaseModel):
    format: str
    fieldSep: str
    data: str


# Attribute Specifications
class Attribute(BaseModel):
    name: str
    source: str
    type: str
    subType: str
    timeType: Optional[str] = None

# Operation Specification
class Operation(BaseModel):
    op: str
    inAttr: str
    outAttr: str
    windowUnit: str
    windowSize: Union[int, float]
    timeAttr: Optional[str] = None

# Configurations
class Config(BaseModel):
    numInitialStates: int = 12
    numHistogramBuckets: int = 10
    attributes: List[Attribute] = []
    ops: List[Operation] = []
    decTree_maxDepth: Optional[int] = 5
    decTree_minNormInfGainToSplit: Optional[float] = 0.1
    decTree_minEntropyToSplit: Optional[float] = 0.1
    ignoreConversionErrors: bool = False
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
    id: int
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


class ClassifySamplesRequest(BaseModel):
    dataSource: DataSource
    model: Model


class BuildModelRequest(BaseModel):
    name: str
    description: str
    dataset: str
    public: bool
    dataSource: DataSource
    config: Config
