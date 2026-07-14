FROM python:3.12-slim

WORKDIR /app
COPY server.py demo_data.json README.md ./

ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

CMD ["python", "server.py"]
