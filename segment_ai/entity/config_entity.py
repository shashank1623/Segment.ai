from collections import namedtuple


DataIngestionConfig= namedtuple("DataIngestionConfig",
                                ["dataset_download_url",
                                 "ingested_data_dir",
                                 "raw_data_dir",
                                 "ingested_train_dir"
                                 ])



TrainingPipelineConfig= namedtuple("TrainingPipelineConfig",["artifact_dir"])

                                    

