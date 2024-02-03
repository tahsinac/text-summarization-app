from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (DataIngestionConfig, DataValidationConfig, DataTransformationConfig)


# The ConfigurationManager class is used for managing configuration settings in a Python program.
class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """
        The function `get_data_ingestion_config` returns a `DataIngestionConfig` object with values from
        the `config` object.
        :return: an instance of the DataIngestionConfig class.
        """
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        The function `get_data_validation_config` returns a `DataValidationConfig` object with the
        specified configuration values.
        :return: an instance of the DataValidationConfig class.
        """
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        The function `get_data_transformation_config` returns a `DataTransformationConfig` object with
        the specified configuration parameters.
        :return: an instance of the DataTransformationConfig class.
        """
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name = config.tokenizer_name
        )

        return data_transformation_config