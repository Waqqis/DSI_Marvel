from typing import Any, Optional
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import requests
import hashlib
import time
import os.path
import logging


class Analysis():

    def __init__(self, analysis_config: str) -> None:

        dirname = os.path.dirname(__file__)

        CONFIG_PATHS = [os.path.join(dirname,'configs/system_config.yml'), 
                        os.path.join(dirname,'configs/user_config.yml'), 
                        os.path.join(dirname,'configs/secrets.yml')]
              


        logging.basicConfig(filename='analysis.log', level=logging.INFO)
        logging.info('Initializing Analysis')

        CONFIG_PATHS = ['src/Analysis_package/configs/system_config.yml', 'src/Analysis_package/configs/user_config.yml', 'src/Analysis_package/configs/secrets.yml']

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
        logging.info('Analysis initialized')

    def load_data(self) -> None:
        ''' Retrieve data from the GitHub API

        This function makes an HTTPS request to the GitHub API and retrieves your selected data. The data is
        stored in the Analysis object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''
        logging.info('Loading data')

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
        #try/except block to handle the case where the domain_url is not defined in the config file
        try:
            url = self.config['domain_url'] + '/v1/public/characters?limit=100&offset=0'
        except:
            url = 'http://gateway.marvel.com' + '/v1/public/characters?limit=100&offset=0'


        # Make the API request
        # try/except block to handle response errors
        try:
            response = requests.get(url, params=params)
            dat = response.json()
            logging.info('Data loaded')
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f'Error loading data: {e}')
            raise SystemExit(e)
        
        
    def compute_analysis(self) -> Any:
        '''Analyze previously-loaded data.

        This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
        and returns the data in a format of your choice.

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Any

        '''

        results = self.load_data()['data']['results']
        df = pd.DataFrame(results)
        logging.info('computing analysis')
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
        ''' Analyze and plot data

        Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
        the path from the configuration file if not specified.

        Parameters
        ----------
        save_path : str, optional
            Save path for the generated figure

        Returns
        -------
        fig : matplotlib.Figure

        '''
        logging.info('plotting data')
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

        # Save the figure to the path in the parameter `save_path` with fig name 'topComics.png'
        save_path = self.config['save_path']
        if save_path is None:
            save_path = 'plots/'
            
        plot_format = self.config['plot_format']    
        if plot_format is None:
            plot_format = 'png'

        logging.info(f'Saving plot to {save_path}topComics.{plot_format}')
        plt.savefig(save_path + 'topComics.' + plot_format, bbox_inches='tight')
        
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

        logging.info(f'Saving plot to {save_path}topSeries.{plot_format}')
        # Save the figure
        plt.savefig(save_path +'topSeries.' + plot_format, bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

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

        logging.info(f'Saving plot to {save_path}topStories.{plot_format}')
        # Save the figure
        plt.savefig(save_path +'topStories.' + plot_format, bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

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

        logging.info(f'Saving plot to {save_path}topEvents.{plot_format}')
        # Save the figure
        plt.savefig(save_path +'topEvents.' + plot_format, bbox_inches='tight')  # Add bbox_inches='tight' to save the full figure

        pass

    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

        Send a notification to the user through the ntfy.sh webpush service.

        Parameters
        ----------
        message : str
        Text of the notification to send

        Returns
        -------
        None

        '''
        logging.info('Notifying user')
        topicname = 'Marvel_Result_notification'
        requests.post(f"https://ntfy.sh/{topicname}", 
        data=message.encode(encoding='utf-8'))

        pass


analysis.load_data()

# Call the plot_data method on the instance
analysis.plot_data()

analysis.notify_done("You request for Marvel Analysis has been compelted")
        
    
