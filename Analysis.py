from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import hashlib
import time


class Analysis():

    def __init__(self, analysis_config: str) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            if this_config is not None:
                config.update(this_config)

        self.config = config

    def load_data(self) -> None:
        ts = str(time.time())
        
        # Create a hash using md5
        hash_value = hashlib.md5((ts + self.config['private_key'] + self.config['public_key']).encode('utf-8'))
        md5digest = str(hash_value.hexdigest())

        # Define the parameters
        params = {
            'ts': ts,
            'apikey': self.config['public_key'],
            'hash': md5digest
        }
        # Define the API endpoint
        url = self.config['domain_url'] + '/v1/public/characters?limit=100&offset=0'

        # Make the API request
        response = requests.get(url, params=params)

        # Convert the response to JSON
        data = response.json()
        return data

    def compute_analysis(self) -> Any:
        pass

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        pass

    def notify_done(self, message: str) -> None:
        pass


# Define the path to the analysis configuration file
analysis_config_path = 'configs/job_file.yml'

# Create an Analysis object with the path to the analysis configuration file
analysis = Analysis(analysis_config_path)

# Call the load_data method on the instance
analysis.load_data()
        
    