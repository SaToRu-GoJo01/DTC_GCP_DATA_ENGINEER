FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"
COPY pyproject.toml .python-version uv.lock ./
COPY README.md ./
COPY src ./src
COPY pipeline.py ./pipeline.py
RUN uv sync --locked
ENTRYPOINT ["python", "pipeline.py"]