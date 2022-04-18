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
- `app` contains a standalone-version of the application
- `aws` contains a _serverless-ish_ implementation for AWS
- `exp` contains some experimental code written during development

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
