from influxdb import InfluxDBClient
import time
import pandas as pd
from datetime import datetime
from oslo_log import log as logging
from iotronic_lightningrod.modules.plugins import Plugin
import os
import requests

LOG = logging.getLogger(__name__)

# Configuration
CSV_DIR = "/opt/data"
CSV_FILE = os.path.join(CSV_DIR, "structured_time_series_v2.csv")
STATE_FILE = os.path.join(CSV_DIR, "last_index.state")
CSV_URL = "https://drive.google.com/uc?id=1ryiOeb_c2xqAi0JWPfAJqbNLSTM51BP0"

# Logging fallback
def log_info(msg):
    try:
        LOG.info(msg)
    except Exception:
        print("[INFO]", msg)

def log_error(msg):
    try:
        LOG.error(msg)
    except Exception:
        print("[ERROR]", msg)

class Worker(Plugin.Plugin):
    def __init__(self, uuid, name, q_result=None, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

        # Ensure the directory exists
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)
            log_info(f"Created directory {CSV_DIR}")

        # Download the CSV if missing
        if not os.path.isfile(CSV_FILE):
            log_info("CSV file not found locally. Downloading...")
            try:
                self.download_csv()
                log_info(f"Downloaded CSV to {CSV_FILE}")
            except Exception as e:
                log_error(f"CSV download failed: {e}")
                raise

        # Load and validate CSV
        try:
            self.df = pd.read_csv(CSV_FILE)
            if self.df.shape[0] == 0 or self.df.shape[1] <= 1:
                raise ValueError("CSV file is empty or corrupt.")
            self.df['time'] = pd.to_datetime(self.df['time'])
            self.df = self.df.fillna(0)
            log_info(f"Loaded CSV with {len(self.df)} rows.")
        except Exception as e:
            log_error(f"Error reading CSV: {e}")
            raise

        # InfluxDB setup
        self.host = 'influxdb'
        self.port = 8086
        self.user = 'admin'
        self.password = 'admin'
        self.dbname = 'secco'

        self.client = InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.dbname
        )
        self.client.create_database(self.dbname)

        # Index resume support
        self.last_index = self.load_last_index()

    def download_csv(self):
        """Download the CSV from a public Google Drive URL."""
        response = requests.get(CSV_URL)
        if response.status_code == 200:
            with open(CSV_FILE, 'wb') as f:
                f.write(response.content)
        else:
            raise Exception(f"Failed to download file. Status: {response.status_code}")

    def load_last_index(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return int(f.read().strip())
            except Exception as e:
                log_error(f"Failed to read state file: {e}")
        return 0

    def save_last_index(self, index):
        try:
            with open(STATE_FILE, 'w') as f:
                f.write(str(index))
        except Exception as e:
            log_error(f"Failed to write state file: {e}")

    def generate_data_point(self, row):
        def safe_float(value):
            try:
                return float(str(value).strip('"'))
            except:
                return 0.0

        return {
            "measurement": "environmental_data",
            "tags": {
                "host": row.get('name', 'unknown'),
                "source": row.get('source_file', 'unknown')
            },
            "time": datetime.utcnow().isoformat(),
            "fields": {
                "Gust": safe_float(row['Gust']),
                "Humidity": safe_float(row['Humidity']),
                "Light": safe_float(row['Light']),
                "PM10": safe_float(row['PM10']),
                "PM100": safe_float(row['PM100']),
                "PM25": safe_float(row['PM25']),
                "Part03": safe_float(row['Part03']),
                "Part05": safe_float(row['Part05']),
                "Part10": safe_float(row['Part10']),
                "Part100": safe_float(row['Part100']),
                "Part25": safe_float(row['Part25']),
                "Part50": safe_float(row['Part50']),
                "Precipitation": safe_float(row['Precipitation']),
                "Pressure": safe_float(row['Pressure']),
                "Temperature": safe_float(row['Temperature']),
                "UVI": safe_float(row['UVI']),
                "Wind_direction": safe_float(row['Wind_direction']),
                "Wind_speed": safe_float(row['Wind_speed']),
                "alt": safe_float(row['alt']),
                "lat": safe_float(row['lat']),
                "lon": safe_float(row['lon'])
            }
        }

    def run(self):
        log_info(f"Plugin '{self.name}' started.")
        log_info(f"InfluxDB target: {self.host}:{self.port}, DB: {self.dbname}")
        log_info(f"Starting from row {self.last_index} of {len(self.df)}")

        while self._is_running and self.last_index < len(self.df):
            current_row = self.df.iloc[self.last_index]
            data_point = self.generate_data_point(current_row)

            try:
                success = self.client.write_points([data_point])
                if success:
                    log_info(f"Row {self.last_index} sent.")
                else:
                    log_error(f"Failed to write row {self.last_index}.")
            except Exception as e:
                log_error(f"Exception during write: {e}")

            self.last_index += 1
            self.save_last_index(self.last_index)
            time.sleep(30)

        log_info("Dataset complete or plugin stopped.")
