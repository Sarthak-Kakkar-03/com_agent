# Instructions for the backend run

FROM python:3.10
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]