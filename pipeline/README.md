# Pipeline

- This directory contains a pipeline script and the modules that it uses for extracting, transforming and loading data from and s3 bucket/kafka cluster to a postgres database defined by the user.
- If you would like to see an example of a postgres RDS instance there is deploy scripts for that in the [deploy](../deploy/) directory.

## Install dependencies

- Python Scripts
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r pipeline/requirements.txt`

## `.env` File

- The scripts utilise a `.env` file in the root directory.  
    - The base file should contain:
        ```
        DATABASE_USERNAME=<UPLOAD_DB_USERNAME>
        DATABASE_IP=<UPLOAD_DB_IP>
        DATABASE_PORT=<UPLOAD_DB_PORT>
        DATABASE_NAME=<UPLOAD_DB_PORT>
        DATABASE_PASSWORD=<UPLOAD_DB_PASSWORD>
        ```
    - If using an Amazon S3 bucket add:
        ```
        AWS_ACCESS_KEY_ID=<S3_USER_ACCESS_KEY>
        AWS_SECRET_ACCESS_KEY=<S3_USER_ACCESS_SECRET>
        ```
    - If using a Kafka cluster add:
        ```
        BOOTSTRAP_SERVERS=<KAFKA_CLUSTER_IP>
        SECURITY_PROTOCOL=<ACCESS_PROTOCOL>
        SASL_MECHANISM=<ACCESS_PROTOCOL_MECHANISM>
        KAFKA_USERNAME=<USERNAME>
        KAFKA_PASSWORD=<PASSWORD>
        AUTO_OFFSET=<'earliest' OR 'latest'>
        GROUP=<consumer_group>
        ```

## `pipeline` Script

- The script runs the Extract, Transform, Load data pipeline between either:
    - An amazon S3 bucekt and a postgres database.
    - A Kafka cluster and a postgres database.
- It uses the `extract` module to download any required data from the s3 bucket.
- It uses the `consumer` module to recieve messages from the Kafka cluster
- It uses the `logger` module to initiate file and stdout logging
- The target database can be anything as long as it has inetgration with psycopg
- When ran:
    - This script can be passed several options to transform and load that data into a database defined in your `.env`
    - Use `pipeline.py -h` fo information on all the cli options
- **Important notes:** 
    - When ran in stream mode with `-s` it will run continously
    - Depending on the whether you target a s3 bucket or kafka cluster the script will use either `extract` or `consumer` it will never use both modules

## `extract` Module

- This module imports files from an AWS S3 bucket.
- Can be ran directly to test that the link to the s3 bucket was setup correctly in your environment file

## `consumer` Module

- This module creates a confluent kafka consumer that polls messages on the topic and consumer group defined in your environment
- Can be ran directly to test the connection to the kafka cluster has been defined correctly

## `logger` Module

- This module creates a logger than filters logs based on level and start conditions into either `stdout` or to a file titled `etl.log` in `pipeline/`.
