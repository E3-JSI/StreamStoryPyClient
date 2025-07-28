# StreamStory Python Client

A Python client for the StreamStory API, providing easy access to stream processing and anomaly detection capabilities.

## Installation

### Option 1: Install from repository (development)

Clone the repository and install in development mode:

```bash
git clone git@github.com:E3-JSI/StreamStoryPyClient.git
cd StreamStoryPyClient
uv venv
uv sync
```

### Option 2: Install published package

Using pip:
```bash
pip install streamstory
```

Using uv:
```bash
uv add streamstory
```

## Usage

### Basic Setup

```python
from streamstory import StreamStory
from streamstory.entities import BuildModelRequest, DataSource, Config, Attribute, Operation

# Initialize client
client = StreamStory(api_url="https://your-api-url.com", api_key="your-api-key")
```

### Get Available Models

```python
# Get all models
models = client.get_models()
for model in models:
    print(f"Model: {model.name}, UUID: {model.uuid}")

# Get specific model by UUID
model = client.get_model_by_uuid("model-uuid-here")
```

### Build a New Model

```python
# Create data source
data_source = DataSource(
    format="csv",
    fieldSep=",",
    data="your,csv,data,here"
)

# Define attributes
attributes = [
    Attribute(name="value", type="numeric", subType="continuous"),
    Attribute(name="timestamp", type="time", subType="timestamp")
]

# Define operations
operations = [
    Operation(
        op="mean",
        inAttr="value",
        outAttr="value_mean",
        windowUnit="minutes",
        windowSize=5
    )
]

# Create configuration
config = Config(
    numInitialStates=12,
    numHistogramBuckets=10,
    attributes=attributes,
    ops=operations
)

# Build model request
request = BuildModelRequest(
    name="My Model",
    description="Description of the model",
    dataset="dataset_name",
    public=False,
    dataSource=data_source,
    config=config
)

# Build the model
model_info = client.build_model(request)
```

### Delete a Model

```python
client.delete_model_by_uuid("model-uuid-here")
```

## Examples

Check the `examples/` directory for complete working examples showing how to:
- Load and process datasets
- Configure experiments using YAML files
- Build models with different configurations
- Handle time series data

## Requirements

- Python >= 3.10
- requests >= 2.32.3
- pandas >= 2.2.2
- numpy >= 1.26.4
- python-dotenv >= 1.0.1
- dacite >= 1.8.1
- pydantic >= 2.8.2


## License

StreamStoryPyClient is distributed under the MIT License. See LICENSE for more information.


## Acknowledgements

[StreamStoryPyClient](https://github.com/E3-JSI/StreamStoryPyClient) is developed by the
[Department for Artificial Intelligence](http://ailab.ijs.si/) at the
[Jozef Stefan Institute](http://www.ijs.si/), and other contributors.

The project has received funding from the European Union's Horizon Europe innovation programme under Grant Agreement No 101092639 ([FAME](https://www.fame-horizon.eu/)).
