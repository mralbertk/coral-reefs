FROM public.ecr.aws/lambda/python:3.8

# Install build dependencies
RUN yum update -y
RUN yum groupinstall -y "Development Tools"

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY /helpers ${LAMBDA_TASK_ROOT}

# Install python dependencies
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Install Detectron2
RUN python -m pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html

# Configure Lambda
CMD [ "app.handler" ]