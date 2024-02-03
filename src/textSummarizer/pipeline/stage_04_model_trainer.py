
from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.components.model_trainer import ModelTrainer
from textSummarizer.logging import logger


# The ModelTrainerTrainingPipeline class is used for training machine learning models.
class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        """
        The main function initializes a model trainer configuration object, trains the model using the
        configuration, and returns the trained model.
        """
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config=model_trainer_config)
        model_trainer_config.train()