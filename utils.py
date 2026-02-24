from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&]+)", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    if not video_id:
        raise Exception("Invalid YouTube link")

    api = YouTubeTranscriptApi()

    try:
        transcript_list = api.fetch(video_id, languages=["en"])
    except:
        try:
            transcript_list = api.fetch(video_id, languages=["hi"])
        except:
            raise Exception("No transcript available")

    return " ".join([t.text for t in transcript_list])