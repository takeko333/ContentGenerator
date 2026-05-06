import os
import subprocess

from dotenv import load_dotenv
from tqdm import tqdm
from pydub import AudioSegment
from moviepy import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips, concatenate_audioclips

load_dotenv()
audio_list_filename = os.getenv("AUDIO_LIST_FILENAME")

def concat_audios(audio_path_list, output_path, ffmpeg_path):
    with open(audio_list_filename, "w") as f:
        for audio_path in audio_path_list:
            x = os.path.abspath(audio_path).replace("\\", "/")
            f.write(f"file '{x}'\n")
    ffmpeg_cmd = [
        ffmpeg_path,
        "-f", "concat",
        "-safe", "0",
        "-i", audio_list_filename,
        "-c", "copy",
        output_path
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("FFmpegによる音声連結が完了しました。")
        os.remove(audio_list_filename)
    except subprocess.CalledProcessError as e:
        print(f"FFmpegエラー: {e}")

def concat_images(image_path_list, audio_path_list, output_path, fps=24, fade_duration=0.01):
    video_clips = []
    for image_path, audio_path in tqdm(zip(image_path_list, audio_path_list)):
        try:
            audio_clip_segment = AudioFileClip(audio_path)
            image_clip_segment = ImageClip(image_path).with_duration(audio_clip_segment.duration)
            video_clips.append(image_clip_segment)            
        except Exception as e:
            print(f"ファイル処理中にエラーが発生しました ({image_path}, {audio_path}): {e}")
            continue
    if not video_clips:
        print("エラー: 有効なクリップが作成されませんでした。")
        return
    final_video_clip = concatenate_videoclips(video_clips)
    try:
        final_video_clip.write_videofile(
            output_path, 
            fps=fps, 
            codec="libx264", 
            audio_codec="pcm_s16le" # 非圧縮PCMを使用
        )
        print("動画の生成が完了しました！")
    except Exception as e:
        print(f"動画生成中にエラーが発生しました: {e}")

def add_static_audio_to_video(audio_path, image_path, output_path):
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(image_path).with_duration(audio.duration)    
    final_clip = video.with_audio(audio)
    final_clip = final_clip.subclipped(0, audio.duration)
    final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
