FROM public.ecr.aws/lambda/python:3.9

COPY *.py ShipporiAntique-Regular.ttf requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .

CMD ["lambda_function.handler"]