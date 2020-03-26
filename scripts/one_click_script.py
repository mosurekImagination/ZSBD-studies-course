import json
import subprocess
import time

import cx_Oracle

host = '127.0.0.1'
port = '1521'
service_name = 'pdb'

user = 'usr'
user_password = 'pwd'

admin_user = 'sys'
admin_user_password = 'pwd'

tables_to_check = [
    ("CAR", 206000),
    ("CARBODYTYPE", 5),
    ("CARSTATION", 201000),
    ("COMPANY", 201000),
    ("DAMAGE", 206000),
    ("DAMAGESTATUS", 3),
    ("DOCUMENTTYPE", 3),
    ("INSPECTION", 201000),
    ("INVOICE", 201000),
    ("LOCATION", 201000),
    ("PAYMENT", 201000),
    ("PAYMENTSTATUS", 3),
    ("PAYMENTTYPE", 2),
    ("RENTALHISTORY", 201000),
    ("STATIONWORKER", 201000),
    ("SYSTEMUSER", 201000)
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


class DatabaseConfiguration:
    host = '127.0.0.1'
    port = '1521'
    service_name = 'pdb'

    user = 'usr'
    user_password = 'pwd'

    admin_user = 'sys'
    admin_user_password = 'pwd'

    def __init__(self):
        self.docker_id = self.get_docker_id()

    @staticmethod
    def get_docker_id():
        get_docker_id_cmd = r'docker ps | sed -rn "s/^([^ ]+) +zaawansowanesystemybazdanych\/bazadanych.*$/\1/p"'
        process = subprocess.Popen(get_docker_id_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        docker_id = process.communicate()[0].strip()
        return docker_id

    @staticmethod
    def get_connection_url(admin):
        if admin:
            return admin_user + '/' + admin_user_password + '@' + service_name + ' as sysdba'
        else:
            return user + '/' + user_password + '@' + service_name


class DatabaseService:

    def __init__(self, databaseConfiguration):
        self.config = databaseConfiguration
        self.db_connection = self.connect_to_database()

    def execute_sql_file(self, file, admin=False):
        connection_url = self.config.get_connection_url(admin)
        execute_sql_file_cmd = 'docker exec -t ' + self.config.docker_id + ' /bin/sh -c "sqlplus ' + connection_url + ' < ' + file + '"'

        log.info("Executing file: " + file)
        log.info(execute_sql_file_cmd)

        process = subprocess.Popen(execute_sql_file_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(process.communicate()[0])

    def execute_sql(self, sql, admin=False):
        connection_url = self.config.get_connection_url(admin)

        execute_sql_cmd = r'docker exec -t ' + self.config.docker_id + ' /bin/sh -c "echo \'' + sql + '\' | sqlplus ' + connection_url + '"'

        log.info("Executing SQL: " + sql)
        log.info(execute_sql_cmd)

        process = subprocess.Popen(execute_sql_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(process.communicate()[0])

    def import_data(self, dump_file_name):
        chmod_dump_file_cmd = "chmod 666 ../dump/" + dump_file_name
        subprocess.Popen(chmod_dump_file_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)

        import_cmd = "impdp usr/pwd@pdb schemas=USR directory=dump_dir dumpfile=" + dump_file_name
        docker_exec = "docker exec -t " + self.config.docker_id + " /bin/sh -c '" + import_cmd + "'"

        log.info(docker_exec)

        process = subprocess.Popen(docker_exec, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        print(process.communicate()[0])

    def reinitialize_database(self):
        log.header('----- REINITIALIZING DATABASE ----- ')

        if self.db_connection is not None:
            log.info("Close connection for USR")
            self.db_connection.close()

        drop_user_and_schema_cmd = "DROP USER USR CASCADE;"
        log.info(drop_user_and_schema_cmd + " (Removes schema)")

        self.execute_sql(drop_user_and_schema_cmd, True)

        create_user_and_schema_file = "/opt/oracle/scripts/setup/01_user.sql"
        log.info("Running " + create_user_and_schema_file + " (create user and schema)")

        self.execute_sql_file(create_user_and_schema_file, True)

        dump_file_name = "schema_dump.dmp"
        log.info("Importing data from file: " + dump_file_name)

        self.import_data(dump_file_name)

        log.info("Create connection for USR")
        self.db_connection = self.connect_to_database()

        log.header('----- REINITIALIZING DATABASE COMPLETED ----- ')

    def connect_to_database(self):
        connection_succeeded = False
        number_of_tries = 0
        time_between_retries = 5

        dsn_tns = cx_Oracle.makedsn(self.config.host, self.config.port, service_name=self.config.service_name)

        while not connection_succeeded and number_of_tries < 3:
            try:
                number_of_tries += 1
                conn = cx_Oracle.connect(user=self.config.user, password=self.config.user_password, dsn=dsn_tns)
                connection_succeeded = True
            except cx_Oracle.DatabaseError as err:
                log.warn("Problem with connection to database. Retrying in " + str(time_between_retries) + "s...")
                time.sleep(time_between_retries)

        if not connection_succeeded:
            log.error('Problem with database connection. Giving up after ' + str(number_of_tries) + ' tries.')
            return None

        log.info('Successfully connected to the database')
        return conn

    def get_number_of_rows_per_table(self):

        c = self.db_connection.cursor()

        checked_tables = []

        for table in tables_to_check:
            try:
                log.info('Querying ' + table[0])
                c.execute('select COUNT(*) from ' + table[0])
                rows_number = c.fetchone()[0]
                checked_tables.append((table[0], table[1], rows_number))
            except cx_Oracle.DatabaseError as err:
                checked_tables.append((table[0], table[1], None))

        return checked_tables

    def divide_into_failed_and_successful_tables(self, tables_info):
        failed_tables = []
        successful_tables = []

        for table_info in tables_info:
            if table_info[1] == table_info[2]:
                successful_tables.append(table_info)
            else:
                failed_tables.append(table_info)

        return successful_tables, failed_tables

    def print_failed_tables(self, failed_tables):
        for table in failed_tables:
            log.error('ERROR: ' + table[0] + ' SHOULD HAVE ' + str(table[1]) + ', was ' + str(table[2]))

    def print_successful_tables(self, successful_tables):
        for table in successful_tables:
            log.success('OK: ' + table[0] + ' has ' + str(table[2]) + ' rows')

    def check_data_in_tables(self):
        log.header('\n----- DATA CHECK STARTED -----')

        tables_info = self.get_number_of_rows_per_table()
        successful_tables, failed_tables = self.divide_into_failed_and_successful_tables(tables_info)

        retries = 0
        time_between_retries = 6

        while len(failed_tables) > 0 and retries < 5:
            retries += 1
            tables_info = self.get_number_of_rows_per_table()
            successful_tables, failed_tables = self.divide_into_failed_and_successful_tables(tables_info)

            if len(failed_tables) > 0:
                self.print_failed_tables(failed_tables)
                log.warn("Some tables have wrong number of rows. Retrying in " + str(time_between_retries) + "...")
                time.sleep(time_between_retries)

        log.info('\nFinal results of database check:')

        self.print_successful_tables(successful_tables)
        self.print_failed_tables(failed_tables)

        if len(failed_tables) > 0:
            log.error('\n----- DATA CHECK FAILURE -----')
        else:
            log.success('\n----- DATA CHECK SUCCESS -----')

        return len(failed_tables) == 0

    @staticmethod
    def get_queries_from_json_file(file):
        with open(file, 'r') as f:
            return json.load(f)

    def execute_transaction(self, transaction):
        self.reinitialize_database()
        data_correct = self.check_data_in_tables()

        if not data_correct:
            log.error("Data check failed - " + transaction + " will not be executed")
            return None

        log.info("----- Running " + transaction + " -----")

        transaction_queries = self.get_queries_from_json_file(transaction)
        queries_durations = []

        transaction_start_time = time.time()
        c = self.db_connection.cursor()

        self.db_connection.begin()

        for query in transaction_queries:
            log.info("\nRunning: " + query['name'])
            log.info("Query: " + query['query'])
            query_start_time = time.time()
            c.execute(query['query'])
            query_duration = time.time() - query_start_time
            queries_durations.append((query, query_duration))

        self.db_connection.commit()
        transaction_duration = time.time() - transaction_start_time
        log.success(transaction + " took: " + str(transaction_duration) + "s")
        return transaction_duration, queries_durations


def benchmark_transactions(repeat_number=10):
    transactions = ["../manual/transaction1.json", "../manual/transaction2.json", "../manual/transaction3.json"]
    statistics = []

    for transaction in transactions:
        transaction_stats = benchmark_transaction(transaction, repeat_number)
        statistics.append((transaction, transaction_stats))

    return statistics


def benchmark_transaction(transaction, repeat_number=10):
    transaction_stats = []

    for i in range(repeat_number):
        last_stats = db.execute_transaction(transaction)
        transaction_stats.append(last_stats)

    return transaction_stats


# (transaction_name, [(transaction_duration, [(query, duration), (query, duration), ...]), ...])

def print_transaction_statistics(statistics):
    transaction_file = statistics[0]
    transaction_durations = list(map(lambda stats: stats[0], statistics[1]))

    max_transaction_duration = str(round(max(transaction_durations), 5))
    min_transaction_duration = str(round(min(transaction_durations), 5))
    avg_transaction_duration = str(round(sum(transaction_durations) / len(transaction_durations), 5))

    log.success("\n\n--- " + transaction_file + " stats ---")
    log.success(
        "min: " + min_transaction_duration + "   |   " + "max: " + max_transaction_duration + "   |   " + "avg: " + avg_transaction_duration)

    # [
    #   [(query, duration), (query, duration), ...],
    #   [(query, duration), (query, duration), ...],
    #   ...
    # ]
    queries_iterations = list(map(lambda stats: stats[1], statistics[1]))

    # [({name, query}, [duration1, duration2, ...]), ...]
    queries_stats = []

    for query_id in range(len(queries_iterations[0])):
        query_stats = []
        for iteration in range(len(queries_iterations)):
            query_stats.append(queries_iterations[iteration][query_id][1])
        queries_stats.append((queries_iterations[0][query_id][0], query_stats))

    log.success("\n--- Queries: \n")

    for i, query_stats in enumerate(queries_stats):
        durations = query_stats[1]
        max_query_duration = str(round(max(durations), 5))
        min_query_duration = str(round(min(durations), 5))
        avg_query_duration = str(round(sum(durations) / len(durations), 5))

        log.success("Query " + str(i) + ": " + query_stats[0]["name"])
        log.success(
            "min: " + min_query_duration + "   |   " + "max: " + max_query_duration + "   |   " + "avg: " + avg_query_duration)


if __name__ == '__main__':
    db = DatabaseService(DatabaseConfiguration())
    # db.check_data_in_tables()
    # db.reinitialize_database()

    for stats in benchmark_transactions(20):
        print_transaction_statistics(stats)
