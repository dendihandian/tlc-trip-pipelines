# PostgreSQL Playground

## Requirements
- Docker and Docker-Compose

## Setup

1. Go to repository directory using CLI
2. Copy `.env.example` into `.env` and provide credentials
3. Run `docker-compose up -d` or `docker compose up -d`

## Run Pipelines

```
docker-compose exec pipelines python main.py
```