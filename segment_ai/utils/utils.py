import yaml,sys
import numpy as np
import os, sys
import numpy as np
import dill
import pandas as pd
from segment_ai.constant import *
from segment_ai.exception import CustomException
import pickle


def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys) from e
    
