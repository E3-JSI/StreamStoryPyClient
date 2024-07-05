import os
from dotenv import load_dotenv
from streamstory.model import StreamStory



if __name__ == "__main__":

    print("Running main.py")

    load_dotenv()

    api_url = os.getenv("STREAMSTORY_API_URL")
    api_key = os.getenv("STREAMSTORY_API_KEY")

    assert api_url is not None, "STREAMSTORY_API_URL not set"
    assert api_key is not None, "STREAMSTORY_API_KEY not set"

    print(f"api_url='{api_url}', api_key='{api_key}'")

    streamstory = StreamStory(api_url, api_key)

    models = streamstory.get_models()

    # print(f"models={models}")

    # for i, model in enumerate(models):
    #     print(f"i={i}, model={model}")
    #     print("=================================================================")

    model_uuid = 'cceea9f3-cde7-410e-9111-ccd07b799f78'
    model_found = streamstory.get_model_by_uuid(model_uuid)

    # print(f"model_found={model_found}")
    # print(f"model_found.uuid={model_found.uuid}, scales.len={len(model_found.model.scales)}")

    print(f"model_found={model_found}")