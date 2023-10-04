#from setuptools import setup, find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liamhsieh_toolbox",
    version = '0.3.5',
    description = "Collections of Python utility, suppose to be built with Jonathan Carson but he left",
    author = 'Liam Y. Hsieh, PhD',
    author_email = 'liamhsieh@ieee.org',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    project_urls={
        'Homepage': 'https://github.com/liam-hsieh/liamhsieh-toolbox',
        'Docs':'https://liam-hsieh.github.io/liamhsieh-toolbox/'
    },
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
    ],
    #packages = ['toolbox'], #, since I only have a subfolder, toolbox, below setup.py and I don't wanna include docs as well, I just manually list what I need  
    python_requires='>=3.10',
    install_requires=[
        'pandas>=2.0',
        'sqlalchemy>=1.4.40',
        'openpyxl>=3.0.10',
        'pyxlsb>=1.0.9',
        'dask>=2022.8.1',
        'filetype>=1.1.0',
        'cx-Oracle>=8.3.0',
        'pyodbc>=4.0.0',
        'scipy>=1.9.0',
        'scikit-learn>=1.1.2',
        'matplotlib>=3.6.0',
        'pympler>=1.0.0',
        'pyarrow>=9.0.0',
        'streamlit>=1.13.0',
        'streamlit-drawable-canvas>=0.9.2',
        'streamlit-aggrid>=0.3.3',
        'azure-storage-blob>=12.14.0'
    ]
)
