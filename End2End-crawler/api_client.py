from googleapiclient.discovery import build
import logging

class YouTubeAPIClient:
    """
    Client for interacting with the YouTube Data API.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        try:
            self.youtube = build('youtube', 'v3', developerKey=api_key)
        except Exception as e:
            logging.error(f"Failed to initialize YouTube API client: {e}")
            self.youtube = None

    def search_videos(self, query, max_results=10):
        """
        Search for videos using the YouTube Data API.
        Returns a list of dicts with 'title' and 'url'.
        """
        if not self.youtube:
            logging.error("YouTube API client not initialized.")
            return []
        try:
            request = self.youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_results
            )
            response = request.execute()
            results = []
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                url = f"https://www.youtube.com/watch?v={video_id}"
                results.append({'title': title, 'url': url})
            return results
        except Exception as e:
            logging.error(f"Error searching videos: {e}")
            return [] 