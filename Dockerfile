FROM python:3-slim
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install PyGithub==1.55

ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]
