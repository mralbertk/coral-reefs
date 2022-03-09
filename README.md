# coral-reefs
Analyse coral growth images with deep learning. Student Project, [Data
ScienceTech Institute](https://datasciencetech.institute).

## About
The aim of this project is to support Oceanographers at [CRIOBE](http://www.criobe.pf/eng/)
in their study of coral reefs in the pacific ocean. Researchers should be able to
upload raw images of coral reefs to the application, which will apply automated
image treatment steps before executing a segmentation model to detect coral
families present on the image and generating statistical data for further analysis.

#### Implemented Features
- Apply underwater image restoration filters
- Apply underwater image enhancement filters

#### Features in Development
- Automatic perspective correction & cropping of raw coral images
- Segmentation of corals
- Generation of statistics about the coral families present on the image

## Structure
The main application is contained in `app/` and distributed as follows:

- `application/` contains the frontend, built with
[Streamlit](https:https://streamlit.io/)
- `modelapi/` contains the backend, built with [FastAPI](https://fastapi.tiangolo.com/)
- `storage/` is just a file system; to be replaced by a DBMS later

The directory `/exp` contains some experimental stand-alone code written for testing
purposes.

## Installation
**Important:** 
- `Python 3.10` is required to run the application.
- The commands to operate virtual environment on Windows or Linux/MacOS are slightly different

After cloning the repository:

1. Prepare a virtual environment for the frontend application:
```bash
# Navigate to the frontend directory
$ cd [repository]/app/application
# Create a python virtual environment
$ python3 -m venv [yourEnvironment]
# Activate the virtual environment
$ source [yourEnvironment]/bin/activate # Linux/MacOS
> [yourEnvironment]\Script\activate # Windows
# Install dependencies
$ pip install -r requirements.txt
```
2. Repeat for the backend application:
```bash
# Navigate to the backend directory
$ cd [repository]/app/modelapi
# Create a python virtual environment
$ python3 -m venv [yourEnvironment]
# Activate the virtual environment
$ source [yourEnvironment]/bin/activate # Linux/MacOS
> [yourEnvironment]\Script\activate # Windows
# Install dependencies
$ pip install -r requirements.txt (Linux/MacOS)
$ pip install -r requirements-win.txt (Windows)
```
3. Verify `app/storage/export` and `app/storage/preview` exist. If not:
```bash
# Navigate to the app directory
$ cd [repository]/app/
# Create directory storage
$ mkdir storage
# Navigate to the newly created directory
$ cd storage
# Create directory export
$ mkdir export
# Create directory preview
$ mkdir preview
```
4. *(Optional)* Prepare a virtual environment for the experimental code:
```bash
# Navigate to the experimental code directory
$ cd [repository]/exp
# Create a python virtual environment
$ python3 -m venv [yourEnvironment]
# Activate the virtual environment
$ source [yourEnvironment]/bin/activate # Linux/MacOS
> [yourEnvironment]\Script\activate # Windows
# Install dependencies
$ pip install -r requirements.txt
```

## Use

#### Launching the application
Currently, all parts of the application have to be launched separately. You might
need to use multiple terminals.

1. Start the backend application:
```bash
# Navigate to the backend directory
$ cd [repository]/app/modelapi
# Activate the virtual environment
$ source [yourEnvironment]/bin/activate # Linux/MacOS
> [yourEnvironment]\Script\activate # Windows
# Launch the FastAPI application
$ uvicorn main:app --reload
```
  *NB: `--reload` is an optional parameter; when used the API will refresh on code changes/*

2. Start the frontend application:
```bash
# Navigate to the frontend directory
$ cd [repository]/app/application
# Activate the virtual environment
$ source [yourEnvironment]/bin/activate # Linux/MacOS
> [yourEnvironment]\Script\activate # Windows
# Launch the FastAPI application
$ streamlit run main.py
```

A new browser window should open once `streamlit` has launched successfully. If
not, navigate to ```https://localhost:8501```.

To shutdown, cancel both the frontend and the backend application in their
respective terminal windows (default `CTRL + Z`).

## Project Team

### Students
**Mohammed BOUAYOUN**  
mohammed.bouayoun@edu.dsti.institute  
Applied MSc in Data Science and AI

**Albert KONRAD**  
albert.konrad@edu.dsti.institute  
Applied MSc in Data Engineering for AI  

**Noah MARVISI**  
noah.marvisi@edu.dsti.institute  
Applied MSc in Data Science and AI

**Pauline SALIS**  
pauline.salis@edu.dsti.institute  
Applied MSc in Data Science and AI


### Instructor
**Assan SANOGO**  
assan.sanogo@dsti.institute  
Data Scientist
