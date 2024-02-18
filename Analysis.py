from typing import Any, Optional
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import requests
import hashlib
import time


class Analysis():

    def __init__(self, analysis_config: str) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml', 'configs/secrets.yml']

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
        results = self.load_data()['data']['results']
        df = pd.DataFrame(results)
        # compute mean, median, leniar regression for comics, series, stories, events
        df['comics'] = df['comics'].apply(lambda x: x['available'])
        df['series'] = df['series'].apply(lambda x: x['available'])
        df['stories'] = df['stories'].apply(lambda x: x['available'])
        df['events'] = df['events'].apply(lambda x: x['available'])

        # print the results
        print(f"Mean comics: {df['comics'].mean()}")
        print(f"Median comics: {df['comics'].median()}")
        print(f"Mean series: {df['series'].mean()}")
        print(f"Median series: {df['series'].median()}")
        print(f"Mean stories: {df['stories'].mean()}")
        print(f"Median stories: {df['stories'].median()}")
        print(f"Mean events: {df['events'].mean()}")
        print(f"Median events: {df['events'].median()}")

        return df
        

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        df = self.compute_analysis()
        df.set_index('name', inplace=True)

        # Sort the DataFrame by the 'comics' column in descending order and select the top 10
        top_ten_comics = df.sort_values('comics', ascending=False).head(10)

        # Plot a bar chart
        plt.figure(figsize=(12, 6))  # Increase figure size
        plt.bar(top_ten_comics.index, top_ten_comics['comics'])
        plt.title('Top 10 Comics')
        plt.xlabel('Comic Name')
        plt.ylabel('Count')
        plt.xticks(rotation=45, fontsize=8)  # Decrease font size
        plt.tight_layout()  # Add padding
        #plt.show()

        # Save the figure
        plt.savefig('topComics.png', bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

        #top 10 series
        top_ten_series = df.sort_values('series', ascending=False).head(10)

        # Plot a bar chart
        plt.figure(figsize=(12, 6))  # Increase figure size
        plt.bar(top_ten_series.index, top_ten_series['series'])
        plt.title('Top 10 Series')
        plt.xlabel('Series Name')
        plt.ylabel('Count')
        plt.xticks(rotation=45, fontsize=8)  # Decrease font size
        plt.tight_layout()  # Add padding
        #plt.show()

        # Save the figure
        plt.savefig('topSeries.png', bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

        #top 10 stories
        top_ten_stories = df.sort_values('stories', ascending=False).head(10)

        # Plot a bar chart
        plt.figure(figsize=(12, 6))  # Increase figure size
        plt.bar(top_ten_stories.index, top_ten_stories['stories'])
        plt.title('Top 10 Stories')
        plt.xlabel('Story Name')
        plt.ylabel('Count')
        plt.xticks(rotation=45, fontsize=8)  # Decrease font size
        plt.tight_layout()  # Add padding
        #plt.show()

        # Save the figure
        plt.savefig('topStories.png', bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

        #top 10 events
        top_ten_events = df.sort_values('events', ascending=False).head(10)

        # Plot a bar chart
        plt.figure(figsize=(12, 6))  # Increase figure size
        plt.bar(top_ten_events.index, top_ten_events['events'])
        plt.title('Top 10 Events')
        plt.xlabel('Event Name')
        plt.ylabel('Count')
        plt.xticks(rotation=45, fontsize=8)  # Decrease font size
        plt.tight_layout()  # Add padding
        #plt.show()

        # Save the figure
        plt.savefig('topEvents.png', bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure




    def notify_done(self, message: str) -> None:
        topicname = 'Marvel_Result_notification'
        message = 'You request for Marvel Analysis has been compelted'

        requests.post(f"https://ntfy.sh/{topicname}", 
        data=message.encode(encoding='utf-8'))


# Define the path to the analysis configuration file
analysis_config_path = 'configs/job_file.yml'

# Create an Analysis object with the path to the analysis configuration file
analysis = Analysis(analysis_config_path)

# Call the load_data method on the instance
analysis.load_data()
        
    
