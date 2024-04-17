FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# TODO: ignore ignored files when copying
COPY ./texturebackend /usr/src/app/texturebackend
COPY ./texturebackend/.texture_cache/raw_data /usr/src/app/.texture_cache/raw_data
COPY main.py /usr/src/app/

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

EXPOSE 8080

# CMD ["uvicorn", "--factory", "texturebackend.server:get_server", "--host", "0.0.0.0", "--port", "8080"]
# ENTRYPOINT ["python3", "main.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]