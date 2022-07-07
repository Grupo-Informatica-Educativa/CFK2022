FROM python:3.9.10-slim-buster

WORKDIR /home/app/
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8506

CMD [ "streamlit", "run", "app.py" ]
