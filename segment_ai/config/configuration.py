import os,sys

from segment_ai.constant import *
from segment_ai.entity.config_entity import *
from segment_ai.entity.artifact_entity import *
from segment_ai.logger import logging
from segment_ai.exception import CustomException
from segment_ai.utils.utils import read_yaml_file


class Configuration:

    def __init__(self,
                 config_file_path:str = CONFIG_FILE_PATH,
                 current_time_stamp:str =CURRENT_TIME_STAMP) -> None:
        try:
            self.config_info = read_yaml_file(file_path = config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp = current_time_stamp

        except Exception as e:
            raise CustomException(e,sys)from e
        
#artifact_dir = training_pipeline_config/artifact
#data_ingestion_artifact_dir = artifact_dir/data_ingestion/time_stamp
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir=os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]  # constant folder  # here we call all variable that is under DATA_INGESTION_CONFIG_KEY

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]  # constant folder -- in constant it is from config.yaml


# raw data
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
                                        data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
                                        )


# ingested data
            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )

#train data
            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )

            data_ingestion_config=DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                raw_data_dir=raw_data_dir, 
                ingested_data_dir=ingested_data_dir,
                ingested_train_dir=ingested_train_dir
            )
            logging.info(f"Data Ingestion config: {data_ingestion_config}")
            return data_ingestion_config
        
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            data_validation_artifact_dir=os.path.join(
                artifact_dir,
                DATA_VALIDATION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            
            validated_path=os.path.join(data_validation_artifact_dir,DATA_VALIDATION_VALID_DATASET)
            
            validated_train_path=os.path.join(data_validation_artifact_dir,validated_path,DATA_VALIDATION_TRAIN_FILE)
            
          


            schema_file_path = os.path.join(
                ROOT_DIR,
                data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
                data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )
            

            data_validation_config = DataValidationConfig(
                schema_file_path=schema_file_path,validated_train_path=validated_train_path)
            
            return data_validation_config
        except Exception as e:
            raise CustomException(e,sys) from e
        
        
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]

            artifact_dir = os.path.join(ROOT_DIR,
                                        training_pipeline_config[TRAINING_PIPLELINE_NAME_KEY],
                                        training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY])  
    
            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)

            logging.info(f"Training pipeline Config Completed : {training_pipeline_config}")

            return training_pipeline_config

        except Exception as e:
            raise CustomException(e,sys) from e
        




