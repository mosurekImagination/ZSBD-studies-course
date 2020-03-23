import json
import os
import subprocess
import time

import cx_Oracle

host = '127.0.0.1'
port = '1521'
service_name = 'pdb'
user = 'usr'
password = 'pwd'

tables_to_check = [
    ("CAR", 1000),
    ("CARBODYTYPE", 5),
    ("CARSTATION", 1000),
    ("COMPANY", 1000),
    ("DAMAGE", 1000),
    ("DAMAGESTATUS", 3),
    ("DOCUMENTTYPE", 3),
    ("INSPECTION", 1000),
    ("INVOICE", 1000),
    ("LOCATION", 1000),
    ("PAYMENT", 1000),
    ("PAYMENTSTATUS", 3),
    ("PAYMENTTYPE", 2),
    ("RENTALHISTORY", 1000),
    ("STATIONWORKER", 1000),
    ("SYSTEMUSER", 1000),

]


class bcolors:
    HEADER = '\033[95m'
    INFO = '\033[90m'
    SUCCESS = '\033[92m'
    WARNING = '\033[91m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'


class log:

    @staticmethod
    def header(message):
        print(f"{bcolors.HEADER}{message}{bcolors.ENDC}")

    @staticmethod
    def info(message):
        print(f"{bcolors.INFO}{message}{bcolors.ENDC}")

    @staticmethod
    def error(message):
        print(f"{bcolors.ERROR}{message}{bcolors.ENDC}")

    @staticmethod
    def warn(message):
        print(f"{bcolors.WARNING}{message}{bcolors.ENDC}")

    @staticmethod
    def success(message):
        print(f"{bcolors.SUCCESS}{message}{bcolors.ENDC}")


def connect_to_database():
    connection_succeeded = False
    number_of_tries = 0
    time_between_retries = 5

    dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)

    while not connection_succeeded and number_of_tries < 5:
        try:
            number_of_tries += 1
            conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
            connection_succeeded = True
        except cx_Oracle.DatabaseError as err:
            log.warn("Problem with connection to database. Retrying in " + str(time_between_retries) + "s...")
            time.sleep(time_between_retries)

    if not connection_succeeded:
        log.error('Problem with database connection. Giving up after ' + str(number_of_tries) + ' tries.')
        return None

    log.info('Successfully connected to the database')
    return conn


def get_number_of_rows_per_table(db_connection=None):
    close_connection = False

    if db_connection is None:
        db_connection = connect_to_database()
        close_connection = True

    c = db_connection.cursor()

    checked_tables = []

    for table in tables_to_check:
        try:
            log.info('Querying ' + table[0])
            c.execute('select COUNT(*) from ' + table[0])
            rows_number = c.fetchone()[0]
        except cx_Oracle.DatabaseError as err:
            checked_tables.append((table[0], table[1], None))
            break

        checked_tables.append((table[0], table[1], rows_number))

    if close_connection:
        db_connection.close()

    return checked_tables


def divide_into_failed_and_successful_tables(tables_info):
    failed_tables = []
    successful_tables = []

    for table_info in tables_info:
        if table_info[1] == table_info[2]:
            successful_tables.append(table_info)
        else:
            failed_tables.append(table_info)

    return successful_tables, failed_tables


def print_failed_tables(failed_tables):
    for table in failed_tables:
        log.error('ERROR: ' + table[0] + ' SHOULD HAVE ' + str(table[1]) + ', was ' + str(table[2]))


def print_successful_tables(successful_tables):
    for table in successful_tables:
        log.success('OK: ' + table[0] + ' has ' + str(table[2]) + ' rows')


def check_data_in_tables(db_connection=None):
    log.header('\n----- DATA CHECK STARTED -----')

    db_connection = connect_to_database()

    tables_info = get_number_of_rows_per_table(db_connection)
    successful_tables, failed_tables = divide_into_failed_and_successful_tables(tables_info)

    retries = 0
    time_between_retries = 6

    while len(failed_tables) > 0 and retries < 10:
        retries += 1
        tables_info = get_number_of_rows_per_table(db_connection)
        successful_tables, failed_tables = divide_into_failed_and_successful_tables(tables_info)

        if len(failed_tables) > 0:
            print_failed_tables(failed_tables)
            log.warn("Some tables have wrong number of rows. Retrying in " + str(time_between_retries) + "...")
            time.sleep(time_between_retries)

    log.info('\nFinal results of database check:')

    print_successful_tables(successful_tables)
    print_failed_tables(failed_tables)

    if len(failed_tables) > 0:
        log.error('\n----- DATA CHECK FAILURE -----')
    else:
        log.success('\n----- DATA CHECK SUCCESS -----')

    return len(failed_tables) == 0


def reinitialize_database():
    log.header('----- REINITIALIZING DATABASE ----- ')
    os.system('cd .. && docker-compose stop && docker-compose start')
    log.header('----- REINITIALIZING DATABASE COMPLETED ----- ')


def get_docker_id():
    get_docker_id_cmd = r'docker ps | sed -rn "s/^([^ ]+) +zaawansowanesystemybazdanych\/bazadanych.*$/\1/p"'
    process = subprocess.Popen(get_docker_id_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    docker_id = process.communicate()[0].strip()

    return docker_id


def execute_json_file(file):
    log.info("----- Running " + file + " -----")
    db_connection = connect_to_database()
    c = db_connection.cursor()

    with open(file, 'r') as f:
        queries = json.load(f)

    db_connection.begin()
    for query in queries:
        log.info("\nRunning: " + query['name'])
        log.info("Query: " + query['query'])

        c.execute(query['query'])

    db_connection.commit()
    log.success("----- " + file + " completed -----")


def execute_transaction(transaction):
    reinitialize_database()
    data_correct = check_data_in_tables()

    if data_correct:
        start = time.time()
        execute_json_file(transaction)
        end = time.time()
        duration = end - start
        log.success(transaction + " took: " + str(duration) + "s")
        return duration

    log.error("Transaction failed")
    return None


transactions_durations = []
last_duration = 0

if last_duration is not None:
    transaction = "transaction1.json"
    last_duration = execute_transaction(transaction)
    transactions_durations.append((transaction, last_duration))

if last_duration is not None:
    transaction = "transaction2.json"
    last_duration = execute_transaction(transaction)
    transactions_durations.append((transaction, last_duration))

if last_duration is not None:
    transaction = "transaction3.json"
    last_duration = execute_transaction(transaction)
    transactions_durations.append((transaction, last_duration))

log.success("\n\nTransactions' durations:")
for duration in transactions_durations:
    log.success(duration[0] + ": " + str(duration[1]) + "s")
