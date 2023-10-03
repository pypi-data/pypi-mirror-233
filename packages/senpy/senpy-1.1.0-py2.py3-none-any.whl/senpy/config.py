import os

data_folder = os.environ.get('SENPY_DATA', None)
if data_folder:
    data_folder = os.path.abspath(data_folder)
testing = os.environ.get('SENPY_TESTING', "") != ""
enable_evaluation = os.environ.get('SENPY_EVALUATION', "").lower() not in ["no", "false", "f"]
