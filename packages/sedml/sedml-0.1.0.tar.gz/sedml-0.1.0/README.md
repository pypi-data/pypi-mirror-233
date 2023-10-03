# sedml

A [SED-ML](https://sed-ml.org) Python reader based on [pydantic](https://docs.pydantic.dev/latest/).

Currently supports:

- L1V1
- L1V2
- L1V3
- L1V4

## Usage

To parse from a string,
use `sedml.loads`:

```python
>>> import sedml
>>> s = sedml.loads("""<sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
...   <listOfSimulations>
...     <uniformTimeCourse id="sim1" initialTime="0" outputStartTime="0" outputEndTime="1000" numberOfSteps="1000">
...       <algorithm kisaoID="KISAO:0000019"/>
...     </uniformTimeCourse>
...   </listOfSimulations>
...   <listOfModels>
...     <model id="model1" language="urn:sedml:language:sbml.level-3.version-1" source="https://example.com/model.xml"/>
...   </listOfModels>
...   <listOfTasks>
...     <task id="task1" modelReference="model1" simulationReference="sim1"/>
...   </listOfTasks>
... </sedML>
... """)
>>> s
SEDML(
    level='1',
    version='4',
    models=[
        Model(
            id='model1',
            source='https://example.com/model.xml',
            language='urn:sedml:language:sbml.level-3.version-1'
        )
    ],
    simulations=[
        UniformTimeCourse(
            id='sim1',
            algorithm=Algorithm(kisaoID='KISAO:0000019'),
            initialTime=0.0,
            outputStartTime=0.0,
            outputEndTime=1000.0,
            numberOfSteps=1000
        )
    ],
    tasks=[
        Task(id='task1', modelReference='model1', simulationReference='sim1')
    ]
)

```

To export a SED-ML model,
use `sedml.dumps`:

```python
>>> b = sedml.dumps(s)
>>> print(b.decode())
<?xml version='1.0' encoding='UTF-8'?>
<sedML xmlns="http://sed-ml.org/sed-ml/level1/version4" level="1" version="4">
  <listOfModels>
    <model id="model1" source="https://example.com/model.xml" language="urn:sedml:language:sbml.level-3.version-1"/>
  </listOfModels>
  <listOfSimulations>
    <uniformTimeCourse id="sim1" initialTime="0.0" outputStartTime="0.0" outputEndTime="1000.0" numberOfSteps="1000">
      <algorithm kisaoID="KISAO:0000019"/>
    </uniformTimeCourse>
  </listOfSimulations>
  <listOfTasks>
    <task id="task1" modelReference="model1" simulationReference="sim1"/>
  </listOfTasks>
</sedML>

```

By default,
it includes the XML declaration with UTF-8 encoding,
and it is pretty-printed.
This can be customized when calling `sedml.dumps`.

To read from or write to a `os.PathLike`,
use `sedml.load` or `sedml.dump`,
respectively.

## Installation

```
pip install sedml
```

## Development

We are using pytest for testing,
and pre-commit hooks to format and lint the codebase.

To easily set-up a development environment,
run the following commands:

```
git clone https://github.com/maurosilber/sedml
cd sedml
conda env create --file environment-dev.yml
pre-commit install
```

which assume you have git and conda preinstalled.
