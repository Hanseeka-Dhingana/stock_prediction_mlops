from typing import List
from setuptools import find_packages, setup


HYPEN_E_DOT = "-e ."
def get_requirements(file_path : src) -> List[str]:
    
    "This function will return the list of requirements"""
    
    requirements = []
    with open (file_path) as file_obj: 
        requirements = file_obj.readlines()
        requirements= [req.replace("\n", "") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
            
            
    return requirements


setup(
  name='stock_prediction_mlops',
  version='0.0.1',
  author='Hanseeka Dhingana',
  description='A stock price prediction project using machine learning and MLOps practices.',
  packages=find_packages(),
  install_requires=get_requirements('requirements.txt'),
     
) 