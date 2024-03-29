from dataclasses import dataclass
from pathlib import Path

# The code defines several data classes that are used to store configuration information for different
# stages of a data pipeline. Each data class represents a specific configuration with its own set of
# attributes.

@dataclass(frozen=True)
# The class `DataIngestionConfig` represents the configuration for data ingestion, including the root
# directory, source URL, local data file, and unzip directory.
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
# The `DataValidationConfig` class defines the configuration for data validation, including the root
# directory, status file, and a list of all required files.
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    ALL_REQUIRED_FILES: list

@dataclass(frozen=True)
# The class `DataTransformationConfig` represents a configuration for data transformation, including
# the root directory, data path, and tokenizer name.
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: Path

@dataclass(frozen=True)
# The DataTransformationConfig class is used for configuring data transformation operations.
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: Path

@dataclass(frozen=True)
# The `ModelTrainerConfig` class is used to store configuration settings for training a model.
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    model_ckpt: Path
    num_train_epochs: int
    warmup_steps: int
    per_device_train_batch_size: int
    weight_decay: float
    logging_steps: int
    evaluation_strategy: str
    eval_steps: int
    save_steps: float
    gradient_accumulation_steps: int

@dataclass(frozen=True)
# The ModelEvaluationConfig class is used to configure the evaluation of a machine learning model.
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    model_path: Path
    tokenizer_path: Path
    metric_file_name: Path
