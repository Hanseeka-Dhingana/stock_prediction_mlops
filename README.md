# stock_prediction_mlops


### 1) Create the repository
  - Add README.md file
  - Add gitignore (select python)
  - clone the repository through command git clone [https://github.com/Hanseeka-Dhingana/stock_prediction_mlops.git](https://github.com/Hanseeka-Dhingana/stock_prediction_mlops.git)
  - Open this in VS code.

### 2) Create virtual environment
  - Open your project terminal then run command:  
    ` python -m venv .venv `
  - activate virtual environment run command:  
    ` .venv/Scripts/activate `


### 3) Create requirements.txt
### 4) Create setup.py file        
   **setup.py tells Python:**  
This is my project, this is its name, version, dependencies, and how to install it.  
  **Main Purpose of setup.py is used to**
  - Convert your project into a Python package
  - Make it installable using pip
  - Manage dependencies
  - Prepare your project for sharing or publishing (like on PyPI)

So instead of sending someone many .py files, you give them a package they can install.


### 5) Create src folder for the entire module that we complete in project
create __init__.py file in the src folder so that setup.py file recognize it and build package.
[more info](https://sarangsurve.medium.com/python-basics-why-use-init-py-c88589e44c91)

### 6) Run the command in terminal pip install -r requirements.txt

#### 1) Create components folder in the src folder 
create __init__.py file in that folder because we do this in each folder. After that create the files for each module i.e data_ingestion.py, data_transformation.py, model_traning.py, etc.

#### 2) Create pipeline folder in the src folder 
create the pipeline for training and also prediction pipeline i.e train_pipeline.py, predict_pipeline.py, etc. 


#### 3) Create Exception.py file in the src folder 
In this file we create our custom Exception that tell the exact filename, line number, and error message.

#### 4) Create logger.py file in the src folder
This code is responsible for creating a system diary (logging). Instead of just printing errors to the console (which vanish when you close the terminal), this code saves everything to a file so you can check it later. It helps to check the error when you automate the project on cloud (Github Actions, Railway).
 [https://medium.com/@HLIBIndustry/python-logging-custom-handlers-f3ba784a9452](https://medium.com/@HLIBIndustry/python-logging-custom-handlers-f3ba784a9452)    
 [https://stackoverflow.com/questions/6918493/in-python-why-use-logging-instead-of-print](https://stackoverflow.com/questions/6918493/in-python-why-use-logging-instead-of-print)



linear regression 
Logistic regression 
Knneighbor
xgboost
SVR
Adaboost
LSTM





