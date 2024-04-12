import json
import requests
# import of the sql client

class Tap:
    def __init__(self, config):
        self.config = config

    # The discover function retreives and returns the JSON containing information about the streams
    def discover(self):
        with open('schema.json') as json_file:
            schema = json.load(json_file)
        return schema

    # The read function hits the API and retreives the data using the designated methods from each stream
    def read(self, stream_state, stream_schema, stream_source, bookmark, start, replication_method, replication_key):

        # Full replication method pulls the entire table each execution
        if replication_method == 'full':
            response = requests.get(stream_source)
            if response.status_code != 200:
                raise RuntimeError(f"Failed to fetch data from {stream_source}. Status code: {response.status_code}")
            data = response.json()
            return data

        # Key-based replication method pulls only new or modified records each execution
        elif replication_method == 'key-based':
            print('TODO: implement a key-based approach to save/bookmark the state and reduce # of rows pull each execution')
            # Here I would implement an option to tap the API using the bookmark as a filter to grab only recent rows. 
            # The replication key value in the schema would contain the date row which is used as the bookmark (ex: last_modified_ts).
            # The bookmark value in the schema would contain the datetime of the last row grabbed. It needs to be updated after every execution.

# ####################################################################################

class Target:
    def __init__(self, config):
        self.config = config
        self.database_credentials = {
            'user': config['user'],
            'password': config['password'],
            'database': config['database'],
            'host': config['host']
        }
        self.sql_client = sqlconnector.Client()

    # The write fuction inserts the data into the streams table inside the database. Batching is used to speed up execution time.
    def write(self, stream, records, replication_method):
        self.sql_client.connect(self.database_credentials['host'], self.database_credentials)

        # The full method truncates the table and then adds the entire dataset.
        if replication_method == 'full':
            
            batch_size = 100
            truncate_query = f"TRUNCATE TABLE {stream}"
            insert_query = f"INSERT INTO {stream} ({', '.join(records[0].keys())}) VALUES ({', '.join(['%s' for _ in records[0].keys()])})"

            self.sql_client.execute(truncate_query)

            for i in range(0, len(records), batch_size):
                batch_records = records[i:i+batch_size]
                batch_values = [tuple(record.values()) for record in batch_records]
                self.sql_client.executemany(insert_query, batch_values)

        # The key-based method inserts new rows and updates existing rows that were modified.
        elif replication_method == 'key-based':
            print('TODO: implement a key-based approach to write only new or updated rows to the table')
            # Here I would implement a key-based approach to upsert only new or updated records.
            # The primary key of the table would be used to identify if the row is new or updated.
            # This method is useful for large scale pipeline so we don't need to pull all the rows each execution.

        self.sql_client.commit()
        self.sql_client.close()

# ####################################################################################

# This function executes the pipeline
def run_pipeline(tap, target):
    # Retrieve all of the stream information
    streams = tap.discover()['streams']

    # For each stream, read data from the tap and write it to the target
    for stream in streams:
        stream_name = stream['stream']
        replication_method = stream['replication_method']

        tap_data = tap.read(
            stream_state=None, 
            stream_schema=stream['schema'], 
            stream_source=stream['source'], 
            bookmark=stream['bookmark'], 
            start=stream['start'], 
            replication_method=replication_method, 
            replication_key=stream['replication_key']
        )
        
        target.write(stream_name, tap_data, replication_method)

# ####################################################################################

# Configuration (in production the target info would be moved to a enviroment variable)
tap_config = {}
target_config = {
    'user': 'gcp-database-user',
    'password': 'gcp-database-password',
    'database': 'gcp-database-name',
    'host': 'gcp-database-host'
}

# Initialize Tap and Target instances
tap = Tap(config=tap_config)
target = Target(config=target_config)

# Run the pipeline
run_pipeline(tap, target)

# Implementation Notes:
# Ideally, I would use an existing framework like Singer to decouple my taps and my targets.
# The framework also provides comprehensive data checks that I didn't have time to implement.
# One thing I would add before productionizing is some error logging to track down potential issues.
# Finally, to productionize I would spin up a compute instance on GCP, add the code, setup a CRON job, and add some sort of alerting.