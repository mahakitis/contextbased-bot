from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.strip("/")
    return None

def get_youtube_subtitle_text(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL provided.")
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item['text'] for item in transcript])
        if not full_text.strip():
            raise ValueError("Transcript is empty.")
        return full_text
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {e}")
