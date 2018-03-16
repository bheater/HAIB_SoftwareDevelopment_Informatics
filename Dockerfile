FROM python:3
RUN pip3 install flask PyMySQL
RUN mkdir /etc/app/
WORKDIR /etc/app/
ENTRYPOINT ["python3","helloworld.py"]
