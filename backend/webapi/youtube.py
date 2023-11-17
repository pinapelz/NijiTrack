from webapi.web_api import WebAPI


class YouTubeAPI(WebAPI):
    """
    Class for interacting with the YouTube API
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/"

    def _search_matching_id(self, id: str, data: list) -> dict:
        """
        Searches for a info matching a given ID
        param:
            id: str - the ID to search for
        """
        for entry in data:
            if entry['id'] == id:
                return entry
        return None

    def get_data_all_channels(self, channel_tuples: list) -> list:
        data = []
        members = len(channel_tuples)
        request_chunks = [channel_tuples[i:i + 50] for i in range(0, members, 50)]
        for chunk in request_chunks:
            channel_ids = [x[0] for x in chunk]
            channel_names = [x[1] for x in chunk]
            request_string = ",".join(channel_ids)
            stats = self._download_url(
                f"channels?part=statistics&id={request_string}&key={self.api_key}")
            snippet = self._download_url(
                f"channels?part=snippet&id={request_string}&key={self.api_key}")
            stats_list = stats['items']
            snippet_list = snippet['items']
            for i in range(len(stats_list)):
                try:
                    data_entry = {'english_name': channel_names[i], 'id': channel_ids[i],
                                  'subscriber_count':
                                      self._search_matching_id(channel_ids[i], stats_list)[
                                          'statistics']['subscriberCount'], 'view_count':
                                      self._search_matching_id(channel_ids[i], stats_list)[
                                          'statistics']['viewCount'], 'photo':
                                      self._search_matching_id(channel_ids[i], snippet_list)[
                                          'snippet']['thumbnails']['default']['url'], 'description':
                                      self._search_matching_id(channel_ids[i], snippet_list)[
                                          'snippet']['description']}
                    data.append(data_entry)
                except TypeError:
                    print("Error NoneType: " + str(channel_ids[i]))
                except KeyError:
                    print("Error KeyError: " + str(channel_ids[i]))
        return data
