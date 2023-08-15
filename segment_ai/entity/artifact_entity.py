from collections import namedtuple

#data Ingestion

DataIngestionArtifact = namedtuple('DataIngestionArtifact',
                                   ['train_file_path','is_ingested','message'])


