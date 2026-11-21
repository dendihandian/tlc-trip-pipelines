# TLC Trip Pipelines

## Requirements
- Docker and Docker-Compose

## Setup

1. Go to repository directory using CLI
2. Copy `.env.example` into `.env` and provide credentials
3. Run `docker-compose up -d` or `docker compose up -d`

## Run Pipelines

```
docker-compose exec pipelines python pipelines/landing_zone/yellow_tripdata/pipeline.py incremental
docker-compose exec pipelines python pipelines/landing_zone/yellow_tripdata/pipeline.py backfill --start-date 2025-01-01 --end-date 2025-12-31
docker-compose exec pipelines python pipelines/master/taxi_zone_lookup/pipeline.py incremental
```
