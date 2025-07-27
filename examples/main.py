import pandas as pd
from streamstory.entities import BuildModelRequest, DataSource, Config, Attribute, Operation
from src.examples.utils import transform_to_streamstory_csv_str, create_datasource,init_streamstory_client, load_dataset, load_experiments_config, load_datasets_config



def create_config_and_datasource_from_yaml(
        df: pd.DataFrame,
        experiment_config: dict
    ) -> tuple[Config, DataSource]:
    """
    Create the config for the StreamStory API from YAML configuration.
    """
    data = transform_to_streamstory_csv_str(df)
    datasource = create_datasource(data)

    # Convert YAML attributes to Attribute objects
    attributes = []
    for attr_config in experiment_config['config']['attributes']:
        attributes.append(Attribute(**attr_config))

    # Convert YAML operations to Operation objects
    operations = []
    for op_config in experiment_config['config']['operations']:
        operations.append(Operation(**op_config))

    config = Config(
        numInitialStates=experiment_config['config']['num_initial_states'],
        numHistogramBuckets=experiment_config['config']['num_histogram_buckets'],
        attributes=attributes,
        ops=operations,
    )
    return config, datasource


if __name__ == "__main__":
    print("Running main.py")

    # Initialize the StreamStory client
    streamstory = init_streamstory_client()

    # Load configurations
    experiments_config = load_experiments_config('exp/experiments.yaml')
    datasets_config = load_datasets_config('exp/datasets.yaml')

    # Run all experiments
    for experiment_name, experiment_config in experiments_config['experiments'].items():
        print(f"Running experiment: {experiment_name}")
        
        # Get dataset configuration
        dataset_name = experiment_config['dataset']
        dataset_config = datasets_config['datasets'][dataset_name]

        # Use exact name from configuration
        model_name = experiment_config['name']

        # Load dataset
        df = load_dataset(
            data_path=dataset_config['file_path'],
            sep=dataset_config['separator'],
            datetime_col=dataset_config['datetime_col'],
            date_format=dataset_config['date_format'],
            resample_unit=experiment_config['resample_unit'],
        )

        # Create config and datasource
        config, datasource = create_config_and_datasource_from_yaml(
            df=df,
            experiment_config=experiment_config
        )

        # Create model build request
        build_model_req = BuildModelRequest(
            name=model_name,
            description=experiment_config['description'],
            dataset=dataset_config['file_path'],
            public=experiment_config['public'],
            dataSource=datasource,
            config=config,
        )

        # Build StreamStory model
        model = streamstory.build_model(build_model_req)
        print(f"Successfully built model: {model_name}")
