"""Extract, transform and load data from S3 to local db."""

from os import environ as ENV
from datetime import datetime
from logging import getLogger
from argparse import Namespace, ArgumentParser
from json import loads

from dotenv import load_dotenv
from boto3 import client
from psycopg2 import connect
from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import connection, cursor
from progress.bar import Bar

from extract import get_files, get_data_from_file
from consumer import get_consumer, log_message, get_message_data
from logger import get_logger


def get_connection() -> connection:
    """Get connection to database"""
    return connect(
        user=ENV["DATABASE_USERNAME"],
        password=ENV["DATABASE_PASSWORD"],
        host=ENV["DATABASE_IP"],
        port=ENV["DATABASE_PORT"],
        dbname=ENV["DATABASE_NAME"]
    )


def get_cursor(conn: connection) -> cursor:
    """Get cursor from database connection."""
    return conn.cursor()


def get_client():
    """Return an AWS S3 client."""
    return client("s3",
                  aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                  aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])


def upload_data_from_cluster(conn: connection, rows: int = None):
    """Upload data from kafka cluster"""
    cons = get_consumer()
    cons.subscribe(loads([ENV["TOPIC"]]))
    i = 0
    is_done = False
    while not is_done:
        message = cons.poll(1.0)
        if message:
            log_message(message)
            data = get_message_data(message)
            if data is not None:
                upload_message(conn, data)
        if i == rows:
            is_done = True
        i += 1


def upload_message(conn: connection, row: list) -> None:
    """Upload the list data to db."""
    logger = getLogger("etl_logger")
    row[0] = datetime.strftime(
        datetime.fromisoformat(row[0]), r'%Y-%m-%d %H:%M:%S')

    if row[2] == -1:
        if input_row(conn, row, 'request'):
            logger.info("Message has been uploaded as request entry.")
        else:
            logger.warning(
                "Skipping Message: Already exists in request_interaction table.")
    elif input_row(conn, row, 'rating'):
        logger.info("Message has been uploaded as rating entry.")
    else:
        logger.warning(
            "Skipping Message: Already exists in rating_interaction table.")


def upload_data(conn: connection, data: list[list]) -> None:
    """Upload the list data to db."""
    logger = getLogger('etl_logger')
    skipped = 0
    with Bar('Uploading Rows...', max=len(data)) as prog_bar:
        for row in data:
            if row[2] == '-1':
                if not input_row(conn, row, 'request'):
                    skipped += 1
            elif not input_row(conn, row, 'rating'):
                skipped += 1
            prog_bar.next()
    if skipped:
        logger.info("%s Rows have been skipped.", skipped)


def is_duplicate(conn: connection,
                 table: str, at: datetime,
                 exhibit_id: int, table_id: int) -> bool:
    """Return True when datapoint is already present in db."""
    with get_cursor(conn) as curs:
        curs.execute(
            SQL("""
            SELECT * FROM {table} 
            WHERE {pkey} = %s AND exhibition_id = %s AND event_at = %s
            """).format(table=Identifier(f"{table}_interaction"),
                        pkey=Identifier(f"{table}_id")),
            (table_id, exhibit_id, at))
        if curs.fetchone():
            return True
        return False


def input_row(conn: connection, row: list, table_name: str) -> bool:
    """Return True if row was successfully input into database."""
    with get_cursor(conn) as curs:
        req_map = {'0.0': 0, '1.0': 1, 0: 0, 1: 1}
        row_value = req_map[row[3]] if table_name == "request" else int(row[2])
        curs.execute(
            SQL("SELECT {field} from {table} where {pkey} = %s").format(
                field=Identifier(f"{table_name}_id"),
                table=Identifier(table_name),
                pkey=Identifier(f"{table_name}_value")),
            (row_value, ))
        row_id = curs.fetchone()
        conn.commit()

        curs.execute("SELECT exhibition_id from exhibition where public_id = %s",
                     (f"EXH_0{row[1]}", ))
        exh_id = curs.fetchone()

        dt_row = datetime.strptime(row[0], r'%Y-%m-%d %H:%M:%S')

        if not is_duplicate(conn, table_name, dt_row, exh_id, row_id):
            curs.execute(SQL("""
                            INSERT INTO {table} (exhibition_id, {field}, event_at)
                            VALUES (%s, %s, %s)
                            """).format(table=Identifier(f"{table_name}_interaction"),
                                        field=Identifier(f"{table_name}_id")),
                         (exh_id[0], row_id[0], dt_row)
                         )
            conn.commit()
            return True
        return False


def etl(arguments: Namespace) -> None:
    """Extract, transform and load data from s3 bucket into db."""
    conn = get_connection()

    logger = getLogger("etl_logger")

    logger.info("Starting ETL...")

    if arguments.stream:
        upload_data_from_cluster(conn, arguments.rows)
    else:
        s_client = get_client()
        file_names = get_files(s_client, arguments.bucket)
        logger.info("All files downloaded: %s", file_names)
        data = get_data_from_file(arguments.rows)
        upload_data(conn, data)
        logger.info("All data uploaded!")

    conn.close()


def get_arguments() -> Namespace:
    """Return arguments from cli."""
    parser = ArgumentParser(add_help=False,
                            epilog="""
                                            This is an extract, transform load script
                                            for taking data from and AWS s3 bucket
                                            and uploading it to the db of your choice.
                                            """)
    parser.add_argument('-b', '--bucket', type=str,
                        help='Name of AWS s3 bucket.')
    parser.add_argument('-r', '--rows', type=int,
                        help='Number of rows to pull from data.')
    parser.add_argument('-l', '--log', action='store_true',
                        help='Flag to set true for storing error logs in an output file.')
    parser.add_argument('-s', '--stream', action='store_true',
                        help='Flag to set true for changing the data source from s3 bucket to kafka cluster.')
    parser.add_argument('-h', '--help', action='help')
    arguments = parser.parse_args()

    return arguments


def run():
    """Run full etl script."""
    load_dotenv()

    args = get_arguments()

    get_logger(args.log)
    logger = getLogger("etl_logger")
    logger.info("Logger Initiated.")

    etl(args)


if __name__ == "__main__":

    run()
