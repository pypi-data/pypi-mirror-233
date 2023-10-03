from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import ConfigDict
from pydantic_xml import attr, element, wrapped
from pydantic_xml.element.element import SearchMode

from .common import BOOL, FLOAT, FLOAT_BOOL_STR, INT, _BaseSEDML
from .xml import Element

SID: TypeAlias = str
URI: TypeAlias = str
XML: TypeAlias = Element
TargetType: TypeAlias = str
XPath: TypeAlias = str
MathML: TypeAlias = XML


class Base(
    _BaseSEDML,
    nsmap={"": "http://sed-ml.org/sed-ml/level1/version2"},
    search_mode=SearchMode.UNORDERED,
):
    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )

    id: SID | None = attr(default=None)
    name: str | None = attr(default=None)
    metaid: SID | None = attr(default=None)
    notes: XML | None = element(
        default=None,
        nsmap={"": "http://www.w3.org/1999/xhtml"},
    )
    annotations: XML | None = element(default=None)


class Parameter(Base, tag="parameter"):
    value: FLOAT = attr()


class Variable(Base, tag="variable"):
    target: XPath | None = attr(default=None)
    symbol: str | None = attr(default=None)
    modelReference: SID = attr(default=None)
    taskReference: SID = attr(default=None)


class Change(Base):
    target: XPath = attr()


class ChangeAttribute(Change, tag="changeAttribute"):
    newValue: str = attr()


class AddXML(Change, tag="addXML"):
    newXML: XML = element()


class ChangeXML(Change, tag="changeXML"):
    newXML: XML = element()


class RemoveXML(Change, tag="removeXML"):
    pass


class ComputeChange(Change, tag="computeChange"):
    math: MathML = element(nsmap={"": "http://www.w3.org/1998/Math/MathML"})
    variables: list[Variable] = wrapped(
        "listOfVariables",
        element(default=[]),
    )
    parameters: list[Parameter] = wrapped(
        "listOfParameters",
        element(default=[]),
    )


class Model(Base, tag="model"):
    language: URI | None = attr(default=None)
    source: URI = attr()
    changes: list[Change] = wrapped("listOfChanges", element("change", default=[]))


class AlgorithmParameter(Base, tag="algorithmParameter"):
    kisaoID: str = attr()
    value: FLOAT_BOOL_STR = attr()


class Algorithm(Base, tag="algorithm"):
    kisaoID: str = attr()
    parameters: list[AlgorithmParameter] = wrapped(
        "listOfAlgorithmParameters",
        element(default=[]),
    )


class Simulation(Base):
    algorithm: Algorithm = element()


class UniformTimeCourse(Simulation, tag="uniformTimeCourse"):
    initialTime: FLOAT = attr()
    outputStartTime: FLOAT = attr()
    outputEndTime: FLOAT = attr()
    numberOfPoints: INT = attr()


class OneStep(Simulation, tag="oneStep"):
    step: FLOAT = attr()


class SteadyState(Simulation, tag="steadyState"):
    pass


Simulations = UniformTimeCourse | OneStep | SteadyState


class AbstractTask(Base):
    pass


class Task(AbstractTask):
    modelReference: SID = attr()
    simulationReference: SID = attr()


class SetValue(ComputeChange, tag="setValue"):
    modelReference: SID = attr()
    range: SID | None = attr(default=None)
    target: XPath | None = attr(default=None)
    symbol: str | None = attr(default=None)


class Range(Base):
    pass


class UniformRange(Range, tag="uniformRange"):
    start: FLOAT = attr()
    end: FLOAT = attr()
    numberOfPoints: INT = attr()
    type: str = attr()


class VectorRange(Range, tag="vectorRange"):
    value: list[FLOAT] = element()


class FunctionalRange(Range, tag="functionalRange"):
    range: SID | None = attr(default=None)  # TODO: index?
    variables: list[Variable] = wrapped(
        "listOfVariables", element("variable", default=[])
    )
    parameters: list[Parameter] = wrapped(
        "listOfParameters", element("parameter", default=[])
    )
    math: MathML = element(nsmap={"": "http://www.w3.org/1998/Math/MathML"})


Ranges = UniformRange | VectorRange | FunctionalRange


class SubTask(Base, tag="subTask"):
    task: SID = attr()
    order: INT | None = attr(default=None)


class RepeatedTask(AbstractTask, tag="repeatedTask"):
    range: SID = attr()
    resetModel: BOOL = attr()
    changes: list[SetValue] = wrapped("listOfChanges", element(default=[]))
    subtasks: list[SubTask] = wrapped("listOfSubTasks", element(default=[]))
    ranges: list[Ranges] = wrapped("listOfRanges", element(default=[]))


Tasks = Task | RepeatedTask


class DataGenerator(Base, tag="dataGenerator"):
    variables: list[Variable] = wrapped("listOfVariables", element(default=[]))
    parameters: list[Parameter] = wrapped("listOfParameters", element(default=[]))
    math: MathML = element(nsmap={"": "http://www.w3.org/1998/Math/MathML"})


class Output(Base):
    pass


class Curve(Base, tag="curve"):
    logX: BOOL = attr()
    xDataReference: SID = attr()
    logY: BOOL = attr()
    yDataReference: SID = attr()


class Plot2D(Output, tag="plot2D"):
    curves: list[Curve] = wrapped("listOfCurves", element(default=[]))


class Surface(Curve, tag="surface"):
    logZ: BOOL = attr()
    zDataReference: SID = attr()


class Plot3D(Output, tag="plot3D"):
    surfaces: list[Surface] = wrapped("listOfSurfaces", element(default=[]))


class DataSet(Base, tag="dataSet"):
    label: str = attr()
    dataReference: SID = attr()


class Report(Output):
    datasets: list[DataSet] = wrapped("listOfDataSets", element(default=[]))


Outputs = Plot2D | Plot3D | Report


class SEDML(Base, tag="sedML"):
    level: Literal["1"] = attr()
    version: Literal["2"] = attr()
    models: list[Model] = wrapped(
        "listOfModels",
        element(tag="model", default=[]),
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
