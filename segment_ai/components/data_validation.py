import os  
import sys 
from segment_ai.config import *
from segment_ai.entity.config_entity import DataValidationConfig
from segment_ai.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from segment_ai.exception import CustomException
from segment_ai.logger import logging
from segment_ai.utils.utils import read_yaml_file
from segment_ai.entity.raw_data_validation import IngestedDataValidation
import shutil
from segment_ai.constant import *
import pandas as pd
import json
import pandas as pd



class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>' * 30}Data Validation log started.{'<<' * 30} \n\n") 
            
            # Creating_instance           
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            
            # Schema_file_path
            self.schema_path = self.data_validation_config.schema_file_path
            
            
            # creating instance for row_data_validation
            self.train_data = IngestedDataValidation(
                                validate_path=self.data_ingestion_artifact.train_file_path, schema_path=self.schema_path)
            
            # Data_ingestion_artifact--->Unvalidated train 
            self.train_path = self.data_ingestion_artifact.train_file_path
            
            
            # Data_validation_config --> file paths to save validated_data
            self.validated_train_path = self.data_validation_config.validated_train_path
            
        
        except Exception as e:
            raise CustomException(e,sys) from e


    def isFolderPathAvailable(self) -> bool:
        try:

            # check is the train and test file exists (Unvalidated file)
             
            isfolder_available = False
            train_path = self.train_path
            
            if os.path.exists(train_path):
                    isfolder_available = True
            return isfolder_available
        except Exception as e:
            raise CustomException(e, sys) from e     
      


        
    def is_Validation_successfull(self):
        try:
            validation_status = True
            logging.info("Validation Process Started")
            if self.isFolderPathAvailable() == True:
                
                # Train file 
                train_filename = os.path.basename(
                    self.data_ingestion_artifact.train_file_path)

                is_train_filename_validated = self.train_data.validate_filename(
                    file_name=train_filename)

                is_train_column_name_same = self.train_data.check_column_names()
                validating_train_data_types=self.train_data.validate_data_types(filepath=self.train_path,
                                                                                schema_path=self.data_validation_config.schema_file_path)

                is_train_missing_values_whole_column = self.train_data.missing_values_whole_column()
                
                
                self.train_data.replace_null_values_with_nan()

                
                
                logging.info(
                    f"Train_set status: "
                    f"is Train filename validated? {is_train_filename_validated} | "
                    f"is train column name validated? {is_train_column_name_same} | "
                    f"whole missing columns? {is_train_missing_values_whole_column}"
                    f"Data type validation? {validating_train_data_types}"
                )
  

                if is_train_filename_validated  & is_train_column_name_same & is_train_missing_values_whole_column & validating_train_data_types :
                    
                    ## Exporting Train.csv file 
                    # Create the directory if it doesn't exist
                    os.makedirs(self.validated_train_path, exist_ok=True)
                    
                    schema_data=read_yaml_file(self.schema_path)
                    file_name=schema_data['FileName']

                    # Copy the CSV file to the validated train path
                    shutil.copy(self.train_path, self.validated_train_path)
                    self.validated_train_path=os.path.join(self.validated_train_path,file_name)
                    # Log the export of the validated train dataset
                    logging.info(f"Exported validated train dataset to file: [{self.validated_train_path}]")
                                     
                                    
                    
                    return validation_status,self.validated_train_path
                else:
                    validation_status = False
                    logging.info("Check your Training Data! Validation Failed")
                    raise ValueError(
                        "Check your Training data! Validation failed")
                

            return validation_status,"NONE","NONE"
        except Exception as e:
            raise CustomException(e, sys) from e      
        

    def initiate_data_validation(self):
        try:
            
            # Data Validation
            is_validated, validated_train_path = self.is_Validation_successfull()
            
            
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.schema_path,
                is_validated=is_validated,
                message="Data_validation_performed ",
                validated_train_path=validated_train_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e


    def __del__(self):
        logging.info(f"{'>>' * 30}Data Validation log completed.{'<<' * 30}")