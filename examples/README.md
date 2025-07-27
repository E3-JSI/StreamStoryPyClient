# StreamStory Examples

## Installation

```bash
cd examples
uv venv
uv sync
```

## Configuration

Copy `example.env` to `.env` and update the values:

```
STREAMSTORY_API_URL=https://api.streamstory.ijs.si
STREAMSTORY_API_KEY=your_api_key_here
```

Get your API key from: http://streamstory.ijs.si/profile/api-keys

## Running

```bash
uv run main.py
```

## Configuration Files

### Experiments (`exp/experiments.yaml`)
Define model configurations and parameters for different experiments. Each experiment specifies:
- Model name and description
- Dataset to use
- Resampling unit (1h, 1d, etc.)
- Number of initial states and histogram buckets
- Attributes and operations

### Datasets (`exp/datasets.yaml`)
Define data sources and their properties:
- File paths and formats
- Column mappings
- DateTime configurations

### Data Files
Place your CSV datasets in `exp/data/` directory. The example includes `river_flow.csv`.

## Example Structure

The main script runs all experiments defined in `experiments.yaml`, processing each dataset according to its configuration and building StreamStory models.
