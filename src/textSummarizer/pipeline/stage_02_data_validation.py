from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_validation import DataValiadtion
from textSummarizer.logging import logger


# The DataValidationTrainingPipeline class is used for data validation in a training pipeline.
class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        The main function retrieves the data validation configuration, creates a data validation object,
        and then validates the existence of all files.
        """
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValiadtion(config=data_validation_config)
        data_validation.validate_all_files_exist()