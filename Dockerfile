FROM python:3.10-slim

WORKDIR /app

COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py .
COPY src/ ./src/
RUN pip install --no-cache-dir -e .

COPY app.py .
COPY templates/ ./templates/
COPY data_schema/ ./data_schema/
COPY final_model/ ./final_model/

RUN mkdir -p /app/prediction_output

EXPOSE 7860

CMD ["python", "app.py"]
