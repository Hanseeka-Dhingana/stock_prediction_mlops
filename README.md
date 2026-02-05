# stock_prediction_mlops


### 1) Create the repository
  - Add README.md file
  - Add gitignore (select python)
  - clone the repository through command git clone [text](https://github.com/Hanseeka-Dhingana/stock_prediction_mlops.git)
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

### 7) Create components folder in the src folder 
create __init__.py file in that folder because we do this in each folder. After that create the files for each module i.e data_ingestion.py, data_transformation.py, model_traning.py, etc.


