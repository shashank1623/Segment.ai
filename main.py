from segment_ai.exception import CustomException
from segment_ai.logger import logging
from segment_ai.config.configuration import Configuration
from segment_ai.components.data_ingestion import DataIngestion
import os
from segment_ai.pipeline.pipeline import Pipeline

def main():
    try :
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f'{e}')
        print(e)


if __name__ =="__main__":
    main()