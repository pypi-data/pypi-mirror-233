from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import ConfigDict
from pydantic_xml import attr, element, wrapped
from pydantic_xml.element.element import SearchMode

from .common import BOOL, FLOAT, FLOAT_BOOL_STR, INT, _BaseSEDML
from .xml import Element

SID: TypeAlias = str
URI: TypeAlias = str
XML: TypeAlias = str
TargetType: TypeAlias = str
XPath: TypeAlias = str
MathML: TypeAlias = Element

CurveType: TypeAlias = Literal[
    "points",
    "bar",
    "barStacked",
    "horizontalBar",
    "horizontalBarStacked",
]
SurfaceType: TypeAlias = Literal[
    "parametricCurve",
    "surfaceMesh",
    "surfaceContour",
    "contour",
    "heatMap",
    "stackedCurves",
    "bar",
]
LineType: TypeAlias = Literal[
    "none",
    "solid",
    "dash",
    "dot",
    "dashDot",
    "dashDotDot",
]
SedColor: TypeAlias = str  # RBGA in hex RRGGBBAA
MarkerType: TypeAlias = Literal[
    "none",
    "square",
    "circle",
    "diamond",
    "xCross",
    "plus",
    "star",
    "triangleUp",
    "triangleDown",
    "triangleLeft",
    "triangleRight",
    "hDash",
    "vDash",
]
MappingType: TypeAlias = Literal[
    "time",
    "experimentalCondition",
    "observable",
]
ExperimentType: TypeAlias = Literal[
    "steadyState",
    "timeCourse",
]
AxisType: TypeAlias = Literal[
    "linear",
    "log10",
]
ScaleType: TypeAlias = Literal[
    "linear",
    "log",
    "log10",
]


class Base(
    _BaseSEDML,
    nsmap={"": "http://sed-ml.org/sed-ml/level1/version4"},
    search_mode=SearchMode.UNORDERED,
):
    model_config = ConfigDict(protected_namespaces=(), arbitrary_types_allowed=True)

    metaid: SID | None = attr(default=None)
    id: SID | None = attr(default=None)
    name: str | None = attr(default=None)
    notes: XML | None = attr(default=None)
    annotations: XML | None = attr(default=None)


class Parameter(Base, tag="parameter"):
    id: SID = attr()
    value: FLOAT = attr()


class AppliedDimension(Base, tag="appliedDimension"):
    target: SID | None = attr(default=None)  # (to Task, RepeatedTask, or SubTask)
    dimensionTarget: INT | None = attr(default=None)  # NuMLIdRef


class Variable(Base, tag="variable"):
    id: SID = attr()
    modelReference: SID = attr(default=None)
    taskReference: SID = attr(default=None)
    target: TargetType | None = attr(default=None)
    symbol: str | None = attr(default=None)
    target2: TargetType | None = attr(default=None)
    symbol2: str | None = attr(default=None)
    term: URI | None = attr(default=None)
    dimensionTerm: URI | None = attr(default=None)
    applied_dimensions: list[AppliedDimension] = wrapped(
        "ListOfAppliedDimensions",
        element(default=[]),
    )


class Calculation(Base):
    math: MathML = element(nsmap={"": "http://www.w3.org/1998/Math/MathML"})
    variables: list[Variable] = wrapped("listOfVariables", element(default=[]))
    parameters: list[Parameter] = wrapped("listOfParameters", element(default=[]))


class Slice(Base, tag="slice"):
    reference: str = attr()
    value: str = attr()
    index: SID | None = attr(default=None)  # to RepeatedTask
    startIndex: INT | None = attr(default=None)
    endIndex: INT | None = attr(default=None)


class DataSource(Base, tag="dataSource"):
    id: SID = attr()
    name: str | None = attr(default=None)
    indexSet: str | None = attr(default=None)
    slices: list[Slice] = wrapped("listOfSlices", element(default=[]))


class DataDescription(Base, tag="dataDescription"):
    """Reference to external data.

    Contains a description on how to access it, in what format it is, and what subset of data to extract.
    """

    id: SID = attr()
    source: URI = attr()
    format: URI | None = attr(default=None)
    dimensionDescription: XML | None = element(default=None)
    data_sources: list[DataSource] = wrapped("listOfDataSources", element(default=[]))


class Change(Base):
    target: TargetType = attr()


class ChangeAttribute(Change, tag="changeAttribute"):
    newValue: str = attr()


class RemoveXML(Change, tag="removeXML"):
    pass


class AddXML(Change, tag="addXML"):
    newXML: XML = element()


class ChangeXML(Change, tag="changeXML"):
    newXML: XML = element()


class ComputeChange(Change, Calculation, tag="computeChange"):
    symbol: str | None = attr(default=None)


Changes = ChangeAttribute | RemoveXML | AddXML | ChangeXML | ComputeChange


class Model(Base, tag="model"):
    id: SID = attr()
    source: URI = attr()
    language: URI = attr()
    changes: list[Changes] = wrapped("listOfChanges", element(default=[]))


class AlgorithmParameter(Base, tag="algorithmParameter"):
    kisaoID: str = attr()
    value: FLOAT_BOOL_STR = attr()
    parameters: list[AlgorithmParameter] = wrapped(
        "listOfAlgorithmParameters",
        element(default=[]),
    )


class Algorithm(Base, tag="algorithm"):
    kisaoID: str = attr()
    parameters: list[AlgorithmParameter] = wrapped(
        "listOfAlgorithmParameters",
        element(default=[]),
    )


class Simulation(Base):
    id: SID = attr()
    algorithm: Algorithm = element()


class UniformTimeCourse(Simulation, tag="uniformTimeCourse"):
    initialTime: FLOAT = attr()
    outputStartTime: FLOAT = attr()
    outputEndTime: FLOAT = attr()
    numberOfSteps: INT = attr()


class OneStep(Simulation, tag="oneStep"):
    step: FLOAT = attr()


class SteadyState(Simulation, tag="steadyState"):
    pass


class Analysis(Simulation, tag="analysis"):
    pass


class AbstractTask(Base):
    id: SID = attr()


class Task(AbstractTask, tag="task"):
    modelReference: SID = attr()
    simulationReference: SID = attr()


class SetValue(ComputeChange, tag="setValue"):
    modelReference: SID = attr()
    range: SID | None = attr(default=None)


class Range(Base):
    id: SID = attr()


class UniformRange(Range, tag="uniformRange"):
    start: FLOAT = attr()
    end: FLOAT = attr()
    numberOfSteps: FLOAT = attr()
    type: str = attr()


class VectorRange(Range, tag="vectorRange"):
    value: list[FLOAT] = element()


class FunctionalRange(Range, Calculation, tag="functionalRange"):
    range: SID | None = attr(default=None)


class DataRange(Range, tag="dataRange"):
    sourceReference: SID = attr()


Ranges = UniformRange | VectorRange | FunctionalRange | DataRange


class Objective(Base):
    pass


class LeastSquareObjectiveFunction(Objective, tag="leastSquareObjectiveFunction"):
    pass


class Bounds(Base, tag="bounds"):
    upperBound: FLOAT = attr()
    lowerBound: FLOAT = attr()
    scale: ScaleType = attr()


class ExperimentReference(Base, tag="experimentReference"):
    experiment: SID = attr()


class AjustableParameters(Base, tag="ajustableParameters"):
    target: TargetType = attr()
    initialValue: FLOAT | None = attr(default=None)
    experiment_references: list[ExperimentReference] = wrapped(
        "listOfExperimentReferences",
        element(default=[]),
    )


class FitMapping(Base, tag="fitMapping"):
    type: MappingType = attr()
    dataSource: SID = attr()
    target: SID = attr()
    weight: FLOAT | None = attr(default=None)  # positve
    pointWeight: SID | None = attr(default=None)


class FitExperiment(Base, tag="fitExperiment"):
    type: ExperimentType = attr()
    algorithm: Algorithm = element()
    fit_mappings: list[FitMapping] = wrapped(
        "listOfFitMappings", element("fitMapping", default=[])
    )


class ParameterEstimationTask(AbstractTask, tag="parameterEstimationTask"):
    modelReference: SID = attr()
    algorithm: Algorithm = element()
    objective: Objective
    fit_parameters: list[AjustableParameters] = wrapped(
        "listOfFitParameters",
        element(default=[]),
    )
    fit_experiments: list[FitExperiment] = wrapped(
        "listOfFitExperiments",
        element(default=[]),
    )


class SubTask(Base, tag="subTask"):
    task: SID = attr()
    order: INT | None = attr(default=None)
    changes: list[SetValue] = wrapped("listOfChanges", element(default=[]))


class RepeatedTask(AbstractTask, tag="repeatedTask"):
    range: SID = attr()
    resetModel: BOOL = attr()
    concatenate: BOOL | None = attr(default=None)
    changes: list[SetValue] = wrapped("listOfChanges", element(default=[]))
    ranges: list[Ranges] = wrapped("listOfRanges", element(default=[]))
    subtasks: list[SubTask] = wrapped("listOfSubTasks", element(default=[]))


class DataGenerator(Calculation, tag="dataGenerator"):
    id: SID = attr()


class Output(Base):
    id: SID = attr()


class Axis(Base, tag="axis"):
    type: AxisType = attr()
    min: FLOAT | None = attr(default=None)
    max: FLOAT | None = attr(default=None)
    grid: BOOL | None = attr(default=None)
    style: SID | None = attr(default=None)
    reverse: BOOL | None = attr(default=None)


class Plot(Output):
    legend: BOOL | None = attr(default=None)
    height: FLOAT | None = attr(default=None)
    width: FLOAT | None = attr(default=None)
    xAxis: Axis | None = element(default=None)
    yAxis: Axis | None = element(default=None)


class AbstractCurve(Base):
    xDataReference: SID = attr()
    order: INT | None = attr(default=None)  # non-negative
    style: SID | None = attr(default=None)
    yAxis: Literal["right", "left", None] = attr(default=None)


class Curve(AbstractCurve, tag="curve"):
    yDataReference: SID = attr()
    type: CurveType | None = attr(default=None)
    xErrorUpper: SID | None = attr(default=None)
    xErrorLower: SID | None = attr(default=None)
    yErrorUpper: SID | None = attr(default=None)
    yErrorLower: SID | None = attr(default=None)


class ShadedArea(AbstractCurve, tag="shadedArea"):
    yDataReferenceFrom: SID = attr()
    yDataReferenceTo: SID = attr()


Curves = Curve | ShadedArea


class Plot2D(Plot, tag="plot2D"):
    rightYAxis: Axis | None = element(default=None)
    curves: list[Curves] = wrapped("listOfCurves", element(default=[]))


class Surface(Base, tag="surface"):
    xDataReference: SID = attr()
    yDataReference: SID = attr()
    zDataReference: SID = attr()
    style: SID | None = attr(default=None)
    type: SurfaceType = attr()
    order: INT | None = attr(default=None)  # non-negative


class Plot3D(Plot, tag="plot3D"):
    zAxis: Axis | None = element(default=None)
    surfaces: list[Surface] = wrapped("listOfSurfaces", element(default=[]))


class DataSet(Base, tag="dataSet"):
    label: str = attr()
    dataReference: SID = attr()


class Report(Output, tag="report"):
    datasets: list[DataSet] = wrapped("listOfDataSets", element(default=[]))


class ParameterEstimationReport(Output, tag="parameterEstimationReport"):
    taskReference: SID = attr()


class SubPlot(Base, tag="subPlot"):
    plot: SID = attr()
    row: INT = attr()  # positive
    col: INT = attr()  # positive
    rowSpan: INT | None = attr(default=None)  # positive
    colSpan: INT | None = attr(default=None)  # positive


class Figure(Output, tag="figure"):
    numRows: INT = attr()  # positive
    numCols: INT = attr()  # positive
    subplots: list[SubPlot] = wrapped("listOfSubPlots", element(default=[]))


class ParameterEstimationResultPlot(Plot, tag="parameterEstimationResultPlot"):
    taskReference: SID = attr()


class WaterfallPlot(Plot, tag="waterfallPlot"):
    taskReference: SID = attr()


class Line(Base, tag="line"):
    type: LineType | None = attr(default=None)
    color: SedColor | None = attr(default=None)
    thickness: FLOAT | None = attr(default=None)


class Marker(Base, tag="marker"):
    type: MarkerType | None = attr(default=None)
    size: FLOAT | None = attr(default=None)
    fill: SedColor | None = attr(default=None)
    lineColor: SedColor | None = attr(default=None)
    lineThickness: FLOAT | None = attr(default=None)


class Fill(Base, tag="fill"):
    color: SedColor = attr()


class Style(Base, tag="style"):
    id: SID = attr()
    baseStyle: SID | None = attr(default=None)
    line: Line | None = element(default=None)
    marker: Marker | None = element(default=None)
    fill: Fill | None = element(default=None)


Simulations = UniformTimeCourse | OneStep | SteadyState | Analysis
Tasks = Task | ParameterEstimationTask | RepeatedTask
Outputs = (
    Plot2D
    | Plot3D
    | Report
    | ParameterEstimationReport
    | Figure
    | ParameterEstimationResultPlot
    | WaterfallPlot
)


class SEDML(Base, tag="sedML"):
    level: Literal["1"] = attr()
    version: Literal["4"] = attr()
    data_descriptions: list[DataDescription] = wrapped(
        "listOfDataDescriptions",
        element(default=[]),
    )
    models: list[Model] = wrapped(
        "listOfModels",
        element(default=[]),
    )
    simulations: list[Simulations] = wrapped(
        "listOfSimulations",
        element(default=[]),
    )
    tasks: list[Tasks] = wrapped(
        "listOfTasks",
        element(default=[]),
    )
    data_generators: list[DataGenerator] = wrapped(
        "listOfDataGenerators",
        element(default=[]),
    )
    outputs: list[Outputs] = wrapped(
        "listOfOutputs",
        element(default=[]),
    )
    styles: list[Style] = wrapped(
        "listOfStyles",
        element(default=[]),
    )
    algorithm_parameters: list[AlgorithmParameter] = wrapped(
        "listOfAlgorithmParameters",
        element(default=[]),
    )
