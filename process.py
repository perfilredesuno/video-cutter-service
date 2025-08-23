import os
import requests
import cloudinary.uploader
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def download_video(video_url, save_path):
    r = requests.get(video_url, stream=True)
    with open(save_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return save_path

def split_video(video_path, segment_length, output_dir):
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(video_path)
    duration = int(clip.duration)
    output_files = []
    for i in range(0, duration, segment_length):
        end = min(i + segment_length, duration)
        output_file = os.path.join(output_dir, f"clip_{i}_{end}.mp4")
        ffmpeg_extract_subclip(video_path, i, end, targetname=output_file)
        output_files.append(output_file)
    return output_files

def upload_to_cloudinary(file_path):
    response = cloudinary.uploader.upload(file_path, resource_type="video")
    return response.get("secure_url")

def process_video(data):
    video_url = data.get("video_url")
    duration = int(data.get("duracion_clips_seg", 120))
    temp_video = "temp_input.mp4"
    output_dir = "clips"
    os.makedirs(output_dir, exist_ok=True)

    # Config Cloudinary
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    # Download video
    download_video(video_url, temp_video)

    # Split into clips
    clips = split_video(temp_video, duration, output_dir)

    # Upload each to Cloudinary
    urls = [upload_to_cloudinary(c) for c in clips]

    return {"clips": urls}