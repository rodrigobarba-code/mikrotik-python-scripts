# Alembic migrations
This directory contains the Alembic migrations for the database schema.

## Running migrations
To run the migrations, use the following command:
```bash
alembic upgrade head
```

## Generating a new migration
To generate a new migration, use the following command:
```bash
alembic revision --autogenerate -m "Your migration message"
```
or
```bash
alembic revision --autogenerate
```

## Reverting a migration
To revert the last migration, use the following command:
```bash
alembic downgrade -1
```

## Reverting all migrations
To revert all migrations, use the following command:
```bash
alembic downgrade base
```

## Generating a new migration with a specific revision number
To generate a new migration with a specific revision number, use the following command:
```bash
alembic revision -m "Your migration message" --rev-id 1234567890
```

## Running migrations with a specific revision number
To run the migrations with a specific revision number, use the following command:
```bash
alembic upgrade 1234567890
```

## Running migrations with last revision number
To run the migrations with the last revision number, use the following command:
```bash
alembic upgrade head
```

## Reverting a migration with a specific revision number
To revert the migration with a specific revision number, use the following command:
```bash
alembic downgrade 1234567890
```