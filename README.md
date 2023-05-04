# [NijiTrack](https://nijitracker.com/)
NijiTrack is a set of Python scripts that allows for the visualization and collection of historical subscriber count data for any set of YouTube Channels.

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
3. Execute with `python main.py`
#### For collection using a custom set of channels configured in `data/channels.txt`
1. Configure channels in data/channels.txt in the format `YOUTUBE_CHANNEL_ID,CHANNEL_NAME` for each line
2. Execute with `python main.py ytapi`

An `index.html` is created in your root directory and channel individual pages is created in `stats/*`
You can use `app.py` to host your statics through Flask or use any other services

### Homepage Subscriber Ranking
# <img src="https://user-images.githubusercontent.com/21994085/229314684-af00962a-b363-4337-9ab1-9f41ed7cc7e1.png" alt="image" width="50%" height="50%">

### Individual Page Infocards
# <img src="https://user-images.githubusercontent.com/21994085/229314672-0aa5471a-6991-4018-b684-66e19e0bb34e.png" alt="image" width="50%" height="50%">

### General Trend Graph
# <img src="https://user-images.githubusercontent.com/21994085/229314680-0fce8104-f369-4a4c-9c3e-f982a277f03e.png" alt="image" width="50%" height="50%">

### 7 Day Trend (Data point is recorded each time program is ran)
# <img src="https://user-images.githubusercontent.com/21994085/229314728-fe62ee87-9b8c-4995-8745-f194995d9efd.png" alt="image" width="50%" height="50%">

### Individual daily subscriber data
# <img src="https://user-images.githubusercontent.com/21994085/229314763-eeb94642-32a3-49d3-862e-375280f0d6fb.png" alt="image" width="50%" height="50%">


Webpage design inspired by [TrackHololive](https://trackholo.live/)
