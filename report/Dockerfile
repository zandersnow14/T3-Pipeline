FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY database.py .

COPY queries.py .

COPY lambda_function.py .

CMD [ "lambda_function.handler" ]