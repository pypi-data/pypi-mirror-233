# PythonUtilitiesProject

Utilities used for the german supermarket web scrapping project

## Python environment setup
In the root directory of the project setup python virtual environment using virtualenv
>  python3 -m virtualenv .venv

Start the virtualenv using
> source .venv/bin/activate

Install python libraries
> pip install -r requirements.txt

## Testing the application
To test the application
> python3 -m pytest tests

## Build the module
To build the application you can run
> python3 setup.py sdist
this will generate a dist folder containing a `.tar.gz` file.

You can also use the build added from `requirements.txt`. To use this, run
> python3 -m build
this generates an additional `.whl` file in the dist folder

