# api.py API integration functions

import requests
from config import NYTimes_API_KEY, NYTimes_API_TopStories_URL

def fetch_top_stories():
    # Request parameters
    params = {
        "api-key": NYTimes_API_KEY
    }

    try:
        # Make the GET request to the API
        response = requests.get(NYTimes_API_TopStories_URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and return the list of top stories
            top_stories = data.get("results", [])
            return top_stories
        else:
            # Handle errors (e.g., print an error message)
            print(f"Error: Unable to fetch top stories. Status code: {response.status_code}")
            return None
    except Exception as e:
        # Handle exceptions (e.g., network issues)
        print(f"An error occurred: {str(e)}")
        return None
