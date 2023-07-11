FROM python:3.11-slim

RUN python -m pip install --upgrade pip

WORKDIR /WEBTRONICS

COPY . .

RUN pip install -r requirements.txt

CMD python main.py
