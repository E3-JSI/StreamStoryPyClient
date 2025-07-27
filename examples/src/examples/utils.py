import os
import time
import yaml
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime
from streamstory.model import StreamStory
from streamstory.entities import DataSource

class Experiment(BaseModel):
    model_name: str
    description: str
    public: bool
    data_path: str
    date_format: str
    sep: str
    resample_unit: str
    datetime_col: str
    num_initial_states: int
    num_histogram_buckets: int



def init_streamstory_client():
    load_dotenv()
    api_url = os.getenv("STREAMSTORY_API_URL")
    api_key = os.getenv("STREAMSTORY_API_KEY")
    assert api_url is not None and api_url.strip() != "", "STREAMSTORY_API_URL not set or empty, add it to the .env file inside the examples folder"
    assert api_key is not None and api_key.strip() != "", "STREAMSTORY_API_KEY not set or empty, add it to the .env file inside the examples folder"
    return StreamStory(api_url, api_key)



def load_dataset(
        data_path: str,
        sep: str,
        datetime_col: str,
        date_format: str,
        resample_unit: str, # pandas resample unit- 1d, 1h, etc.
        create_prev_columns: bool = False,
    ) -> pd.DataFrame:
    """
    Load any dataset with the specified datetime column name.
    
    Note: It is recommended to perform imputation before loading the data,
    otherwise NaN values will be removed which may result in data loss.
    """
    df = pd.read_csv(data_path, sep=sep)
    # Convert datetime and set as index
    df[datetime_col] = pd.to_datetime(df[datetime_col], format=date_format)
    df.set_index(datetime_col, inplace=True)
    # Resample and create previous day column
    df = df.resample(resample_unit).mean()
    
    # Create previous period column for all numeric columns (optional)
    if create_prev_columns:
        for col in df.select_dtypes(include=['number']).columns:
            prev_col_name = f"{col}_prev_{resample_unit}"
            df[prev_col_name] = df[col].shift(1)
    
    # Drop NaN values
    df = df.dropna()
    return df


def dt_to_unix_timestamp(dt: datetime) -> int:
    """
    Convert a datetime object to a unix timestamp, which is required by the StreamStory API.
    """
    return int(time.mktime(dt.timetuple()))


def transform_to_streamstory_csv_str(df: pd.DataFrame) -> str:
    """
    Convert the data to a csv string that can be used by the StreamStory API.
    """
    # Check if the DataFrame has a datetime index
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame must have a datetime index. Use df.set_index('datetime_column') to set the datetime column as index.")
    
    df_streamstory = df.copy()
    df_streamstory['ss_timestamp'] = df_streamstory.index.map(dt_to_unix_timestamp)
    # ss_timestamp should be the first column
    df_streamstory = df_streamstory[['ss_timestamp'] + [col for col in df_streamstory.columns if col != 'ss_timestamp']]
    data = ",".join(col for col in df_streamstory.columns)
    for _, row in df_streamstory.iterrows():
        data += "\n" + ",".join(str(row[col]) for col in df_streamstory.columns)
    return data


def create_datasource(data: str) -> DataSource:
    """
    Create a datasource object that can be used by the StreamStory API.
    """
    return DataSource(
        format="csv",
        fieldSep=",", # Default seperator in StreamStory API
        data=data, 
    )


def load_experiments_config(experiments_path: str) -> dict:
    """Load experiments configuration from YAML file."""
    with open(experiments_path, 'r') as file:
        return yaml.safe_load(file)


def load_datasets_config(datasets_path: str) -> dict:
    """Load datasets configuration from YAML file."""
    with open(datasets_path, 'r') as file:
        return yaml.safe_load(file)
