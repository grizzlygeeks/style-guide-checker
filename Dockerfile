FROM python:3.9

WORKDIR /usr/src/app

RUN pip3 install --upgrade pip 

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-u", "run.py" ]