# StreamStory Client


## Requirements
- Python 3.10 or higher 🐍
- Poetry for dependency management 📦

## Installation 🔧

To install StreamStory, follow these simple steps:

### Step 1: Install Poetry
If you haven't already, you need to install Poetry. You can do this by following the official Poetry installation guide:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Alternatively, you can install it via pip:

```bash
pip install poetry
```

### Step 2: Clone the Repository 📂

```bash
git clone https://github.com/yourusername/streamstory.git
```


### Step 3: Install Dependencies

Use Poetry to install the package dependencies:

```bash
poetry install
```

### Step 4: Activate the Virtual Environment 🔄

Activate the virtual environment created by Poetry:

```bash
poetry shell
```


#### Init client

```python
api_url = "http://streamstory.ijs.si/api/v1"
# create api key- http://streamstory.ijs.si/profile/api-keys
api_key = "212ze441-d9b7-4cf8-97d6-961484436f4a"
streamstory = StreamStory(api_url, api_key)
```

#### Get models

```python
models = streamstory.get_models()
```

#### Get model

```python
model_uuid = 'cceea9f2-cde7-410e-9111-ccd08b799f79
model = streamstory.get_model_by_uuid(model_uuid)
```

#### Delete model
```python
model_uuid = 'cceea9f2-cde7-410e-9111-ccd08b799f79'
streamstory.delete_model_by_uuid(model_uuid)
```

#### Build model

```python
...
```


### Examples 📚
Run existing examples by navigating to the examples directory.

```bash
cd streamstory/examples
python main.py
```


## License 📄
StreamStoryPyClient is distributed under the MIT License. See LICENSE for more information.
