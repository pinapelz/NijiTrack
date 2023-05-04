from webapi.web_api import WebAPI


class HolodexAPI(WebAPI):
    """
    Class for interacting with the Holodex API
    """

    def __init__(self, api_key: str = None, member_count: int = 300,
                 organization: str = "Nijisanji"):
        super().__init__(api_key = api_key, base_url = "https://holodex.net/api/v2/")
        self.member_count = member_count
        self.organization = organization
        self._inactive_channels = []

    def get_data_all_channels(self) -> list:
        """
        Gets data for all channels in a particular organization
        """
        members = self.member_count
        data = []
        filtered_data = []
        offset = 0
        while members > 0:
            data += self._download_url(
                f"channels?type=vtuber&offset={offset}&limit=100&org={self.organization}")
            members -= 100
            offset += 100
        for channel in data:
            if channel['inactive'] is False:
                channel['description'] = self.get_channel_description(channel['id'])
                filtered_data.append(channel)
            else:
                self._inactive_channels.append(channel['id'])
        return filtered_data

    def get_exclude_channels(self) -> list:
        """
        Gets the list of excluded channels
        """
        return self._inactive_channels

    def get_view_count(self, channel_id: str) -> int:
        """
        Gets the view count for a particular channel
        """
        data = self._download_url(f"channels/{channel_id}")
        return data['view_count']

    def get_channel_description(self, channel_id: str) -> str:
        """
        Gets the description for a particular channel
        """
        data = self._download_url(f"channels/{channel_id}")
        return data['description']
