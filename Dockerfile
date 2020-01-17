FROM python:3
RUN mkdir /solution
COPY server.py /solution/
WORKDIR /solution
CMD [ "python" , "./server.py" ]