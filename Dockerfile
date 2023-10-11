FROM python:3.10.6-slim

ENV OPENAI_API_KEY=""

RUN mkdir app

RUN apt-get update
RUN apt install python3-dev --assume-yes
RUN apt-get install build-essential -y

ENV HNSWLIB_NO_NATIVE=1

COPY requirements.txt ./app
RUN cd app && pip install -r requirements.txt
COPY . ./app
EXPOSE 8000
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]