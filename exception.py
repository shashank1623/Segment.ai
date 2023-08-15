from flask import Flask
from segment_ai.logger import logging
from segment_ai.exception import CustomException
import os , sys

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
     try:
          raise Exception("We are testing our custom excetption File")
     except Exception as e:
          customer = CustomException(e,sys)
          logging.info(customer.error_message)
          logging.info("We are testing logging module")
          return "Hello World"

try:
     pass
except Exception as e:
     raise CustomException(e,sys)

if __name__ == "__main__":
     app.run(debug=True)