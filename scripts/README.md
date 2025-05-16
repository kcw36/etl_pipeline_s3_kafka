# Shell Scripts

## `.env` File

- The scripts utilise a `.env` file in the root directory
- The file should contain
    ```
    AWS_ACCESS_KEY_ID=<S3_USER_ACCESS_KEY>
    AWS_SECRET_ACCESS_KEY=<S3_USER_ACCESS_SECRET>
    
    DATABASE_USERNAME=<UPLOAD_DB_USERNAME>
    DATABASE_IP=<UPLOAD_DB_IP>
    DATABASE_PORT=<UPLOAD_DB_PORT>
    DATABASE_NAME=<UPLOAD_DB_PORT>
    DATABASE_PASSWORD=<UPLOAD_DB_PASSWORD>
    ```

## `setup_rds.sh`
- Will create the tables defined in the [schema] for the example_db. 
- Schema.sql will recreate the static information and tables neccessary for Liverpool Natural History Museum data.
- Uses your environment file to locate the database.

## `ssh_ec2.sh`
- Connect to an ec2 instance using a key value.
- Need to provide:
    - ec2 dns or ip
    - ssh key location on local computer

## `upload_pipeline.sh`
- Upload pipeline folder to ec2 instance using `scp`.
- Need to provide:
    - ec2 dns or ip
    - ssh key location on local computer