# Capstone Project: FBI Wanted Data Pipeline

## Overview

This project implements an end-to-end data pipeline that fetches data from the FBI Wanted API, cleans it, stores it in a PostgreSQL database, and schedules the data fetching process using Apache Airflow. The project is organized into directories for Airflow, database, and data fetching services.

## Project Structure


## Setup Instructions

### 1. Database Setup

Navigate to the `database` directory and follow these steps to set up the PostgreSQL database:

1. **Build the Docker image:**
    ```
    docker build -t postgres_db .
    ```
2. **Run the container:**
    ```
    docker-compose up -d
    ```

### 2. Data Fetching Service

Navigate to the `data_fetching` directory and follow these steps to set up the data fetching service:

1. **Build the Docker image:**
    ```
    docker build -t data_fetching_service .
    ```

### 3. Airflow Setup

Navigate to the `airflow` directory and follow these steps to set up Apache Airflow:

1. **Run the containers:**
    ```
    docker-compose up -d
    ```

### 4. Environment Variables

Create a `.env` file in the root directory with the following content:
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    POSTGRES_DB=fbi_db


## Usage

The data fetching service will be scheduled to run periodically by Airflow, fetching data from the FBI API and storing it in the PostgreSQL database.

## Project Files

### Database

- **init.sql:** SQL script to initialize the database schema.
- **Dockerfile:** Docker configuration for the PostgreSQL database.
- **docker-compose.yml:** Docker Compose file to deploy the database.

### Data Fetching Service

- **fetch_fbi_data.py:** Python script to fetch and clean data.
- **Dockerfile:** Docker configuration for the data fetching service.
- **requirements.txt:** Python dependencies.

### Airflow

- **dags/fetch_fbi_data_dag.py:** DAG definition to schedule the data fetching process.
- **Dockerfile:** Docker configuration for Airflow.
- **docker-compose.yml:**


