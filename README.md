# [NijiTrack](https://nijitracker.com/)

Historical subscriber count tracker for any subset of YouTube channels. Flask backend and NextJS frontend for visualization.

This was originally made with the intention of tracking the subscriber count of Virtual YouTubers in the Nijisanji organization, but can be used for any set of channels.


# Backend:
Below are the steps to set up the flask backend for data collection and serving data through a web server (`/backend` folder of repo)

### Dependencies
- MariaDB or MySQL
- Python 3.11+
- Flask 2.1.2+ (Optional)

```python
pip install -r requirements.txt
```
### Usage
a. Fill in `config.json` with required info for API keys and SQL connection info
#### For collection using a set of channels belonging to a Virtual YouTuber organization listed on Holodex
1. Edit main.py and edit `HOLODEX_ORG` to the organization name on Holodex and `ORG_MEMBER_COUNT` to the number of members that organization has
  - Overshooting the member count may lead to additional loop iterations, but in general there will be no problems
```
HOLODEX_ORG = "Phase%20Connect"
ORG_MEMBER_COUNT = 75
```
2. Add channels to be excluded from data collection in `data/excluded_channel.txt`
3. Execute with `python nijitrack.py`
#### For collection using a custom set of channels configured in `data/channels.txt`
1. Configure channels in data/channels.txt in the format `YOUTUBE_CHANNEL_ID,CHANNEL_NAME` for each line
2. Execute with `python nijitrack.py ytapi`

A basic graph will be created using plotly and saved to index.html in the root directory

You can use `app.py` to host your statistics through Flask or use any other services


Webpage design inspired by [TrackHololive](https://trackholo.live/)
