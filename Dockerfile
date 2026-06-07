FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 -i "${PIP_INDEX_URL}" -r requirements.txt

COPY src/ ./src/
COPY models/ ./models/

EXPOSE 8501

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
