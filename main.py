from youtube_api import YoutubeDataApi
import os,json,subprocess,shutil
import youtube_dl
video_ids = []
with open('api_key.txt') as f:
    api_key = f.read() 
yt = YoutubeDataApi(api_key)
if not yt.verify_key():
    print("Invalid API key! Exiting...")
    exit()
channelName = input('What is the name of the channel you want to download? ')
result = yt.search(channelName)[0]
isCorrect = input("Is '" + result.get('channel_title') + "' with video title '" + result.get('video_title') +  "' the correct channel? ")
if isCorrect.lower() == 'false' or isCorrect.lower() == 'no':
    print("Falling back to channel id directly from username!")
    try:
        channelId = yt.get_channel_id_from_user(channelName)
    except:
        print("Failed! Exiting...")
        exit()
elif isCorrect.lower() == 'yes':
    channelId = result.get('channel_id')
channelMetadata = yt.get_channel_metadata(channelId)
rawChannelMetadata = yt.get_channel_metadata(channelId, parser=None)
print(channelMetadata)
os.makedirs(channelId, exist_ok=True)
with open(channelId + '/metadata.json', 'w') as f:
    f.write(json.dumps(rawChannelMetadata, sort_keys=True, indent=4))
uploaded = yt.get_videos_from_playlist_id(channelMetadata.get('playlist_id_uploads'))
for i in uploaded:
    print(i.get('video_id'))
    video_ids.append(i.get('video_id'))
wantsDownloads = input("Would you like to download all YouTube videos on this channel? [Y/N] ")
if wantsDownloads.lower() == 'y':
    ydl = youtube_dl.YoutubeDL({'outtmpl': channelId + '/%(title)s.%(ext)s'})
    print(video_ids)
    with ydl:
        ydl.download(video_ids)