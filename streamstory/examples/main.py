import os
import time
import pandas as pd
from dotenv import load_dotenv
from streamstory.model import StreamStory
from streamstory.entities import BuildModelRequest, DataSource, Config, Attribute, Operation


if __name__ == "__main__":

    print("Running main.py")

    load_dotenv()

    api_url = os.getenv("STREAMSTORY_API_URL")
    api_key = os.getenv("STREAMSTORY_API_KEY")

    assert api_url is not None, "STREAMSTORY_API_URL not set"
    assert api_key is not None, "STREAMSTORY_API_KEY not set"

    print(f"api_url='{api_url}', api_key='{api_key}'")

    streamstory = StreamStory(api_url, api_key)

    data_path = "./data/river_flow.csv"  
    date_format = "%Y-%m-%dT%H:%M:%S"
    df = pd.read_csv(data_path, sep=";")

    df['datum'] = pd.to_datetime(df['datum'])
    df.set_index('datum', inplace=True)

    # resample by 1 day
    df = df.resample('1d').mean()
    # store the value of the previous day in a separate column and handle cases where no previous value 
    df['vrednost_prev_day'] = df['vrednost'].shift(1)	
    # drop rows with NaN values- Nan values are not allowed in the input data
    df = df.dropna()

    df['ss_timestamp'] = df.index.map(lambda x: time.mktime(x.timetuple()))

    data = ",".join(col for col in df.columns)

    for index, row in df.iterrows():
        data += "\n" + ",".join(str(row[col]) for col in df.columns)

    datasource = DataSource(
        format="csv",
        fieldSep=",",
        data=data, 
    )

    attributes = [
        Attribute(name="ss_timestamp", source="input", type="time", subType="integer", timeType="time"),
        Attribute(name="vrednost", source="input", type="numeric", subType="float"),
        Attribute(name="vrednost_prev_day", source="input", type="numeric", subType="float"),
    ]
   
    ops = [
        Operation(
            op="timeDelta",
            inAttr="vrednost",
            outAttr="river_flow_derivative",
            windowUnit="samples",
            windowSize=1
        ),
    ]
    
    config = Config(
        numInitialStates=12,
        numHistogramBuckets=10,
        attributes=attributes,
        ops=ops,
    )
    
    build_model_req = BuildModelRequest(
        name="River height",
        description="",
        dataset="river_height.csv",
        public=False,
        dataSource=datasource,
        config=config,
    )

    # build model
    model = streamstory.build_model(build_model_req)
    print(f"Succesfully built model")