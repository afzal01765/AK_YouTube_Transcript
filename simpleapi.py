
from flask import  Flask, request,jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from googleapiclient.discovery import build

app = Flask(__name__)
@app.route('/api/youtube-to-text',methods = ["GET"])

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def get_video_language(video_id):
    """
    Detect the language of the YouTube video using the YouTube Data API.
    """
    try:
        video_request = youtube.videos().list(part="snippet", id=video_id)
        video_response = video_request.execute()

        # Extract the default audio language
        language = video_response['items'][0]['snippet'].get('defaultAudioLanguage', 'en')
        return language
    except Exception as e:
        return None  # Return None if language detection fails

def youtube_to_text():
    video_id = request.args.get("video_id")   #for get video id
    if not  video_id:
        return jsonify({"error": "Missing required parameter: video_id"})
    try:
        transcript =YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(value ["text"] for value in transcript)
        return jsonify("transcript:",transcript_text)
    except TranscriptsDisabled:
        return jsonify({"Error": "Transcripts are disabled for this video."})
    except VideoUnavailable:
        return jsonify({"Error" : "The requested video is unavailable or does not exist."})
    except NoTranscriptFound:
        return  jsonify({"error": "No transcript found for this video."})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"})

if __name__ =="__main__":

    app.run()
