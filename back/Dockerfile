FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip uninstall -y pytube

# fix pytube
# https://github.com/pytube/pytube/issues/1678
RUN python -m pip install git+https://github.com/oncename/pytube

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app", "-c", "gunicorn.config.py"]
