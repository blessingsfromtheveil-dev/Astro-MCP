FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

EXPOSE 8000

CMD ["python","-m","astro_mcp.main"]
