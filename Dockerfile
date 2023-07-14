FROM python:3.10.0

ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN git clone https://github.com/RafaelSolVargas/Vulkan.git /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y software-properties-common && apt-get install -y ffmpeg
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
CMD ["python", "main.py"]