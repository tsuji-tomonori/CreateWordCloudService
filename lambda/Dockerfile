FROM public.ecr.aws/lambda/python:3.9

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:git-core/ppa \
    && apt-get update -y

RUN apt-get install -y git 

COPY lambda/*.py requirements.txt ./

RUN python3.9 -m pip install -r requirements.txt -t .

RUN git clone https://github.com/fontdasu/ShipporiAntique.git

CMD ["lambda_function.lambda_handler"]