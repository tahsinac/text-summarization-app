from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.data_ingestion import DataIngestion
from textSummarizer.logging import logger



# The DataIngestionTrainingPipeline class is used for data ingestion and training pipeline operations.
class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        The main function downloads and extracts a zip file using the data ingestion configuration.
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()