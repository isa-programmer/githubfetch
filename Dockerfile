FROM python:3.12-slim AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/tmp/deps -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=build /tmp/deps /usr/local/lib/python3.12/site-packages

COPY githubfetch.py .

ENTRYPOINT ["python", "githubfetch.py"]
