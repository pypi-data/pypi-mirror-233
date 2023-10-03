from setuptools import setup, find_packages

setup(
  name="pythonUtilitiesProject",
  version="0.1.1",
  description="Utilities used for the german supermarket web scrapping project",
  long_description=open('README.md').read(),
  packages= find_packages(),
  classifiers=[
        "Programming Language :: Python :: 3",
  ],
  python_requires=">=3.6"
)

