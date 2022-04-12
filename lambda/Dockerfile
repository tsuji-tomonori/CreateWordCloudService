FROM public.ecr.aws/lambda/python:3.9

COPY lambda/*.py ShipporiAntique-Regular.ttf requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .

RUN git clone https://github.com/fontdasu/ShipporiAntique.git

CMD ["lambda_function.lambda_handler"]