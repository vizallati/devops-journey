FROM python:3.12-slim

COPY . /app

RUN pip install -r app/requirements.txt && chmod u+x app/setup_db.py app/app.py

EXPOSE 5000

CMD python app/setup_db.py; python app/app.py