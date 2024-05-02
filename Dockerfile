FROM python:3.10-slim

WORKDIR /usr/app

COPY requirements.txt /usr/app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./texture /usr/app/texture
COPY ./.texture_cache/raw_data /usr/app/.texture_cache/raw_data

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

EXPOSE 8080

CMD ["uvicorn", "--factory", "texture.server:get_server", "--host", "0.0.0.0", "--port", "8080"]

# CMD ["python", "texture/runner_dev.py"]