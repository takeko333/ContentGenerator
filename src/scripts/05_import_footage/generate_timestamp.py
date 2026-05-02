import os
import glob
from moviepy import VideoFileClip
from datetime import timedelta

def create_mp4_timestamps(folder_path):
    mp4_files = glob.glob(os.path.join(folder_path, '*.mp4'))
    sorted_files = sorted(mp4_files)    
    total_duration_sec = 0
    timestamps = []
    
    print(f"フォルダ '{folder_path}' のMP4ファイルからタイムスタンプを作成します...")
    i = 1
    for file_path in sorted_files:
        try:
            with VideoFileClip(file_path) as video:
                duration_sec = video.duration
            ts_obj = timedelta(seconds=int(total_duration_sec))
            timestamp = str(ts_obj)
            file_name = os.path.basename(file_path)
            entry = f"{timestamp} {os.path.basename(file_path)}"
            timestamps.append(entry)
            total_duration_sec += duration_sec
            i += 1            
        except Exception as e:
            print(f"エラー: '{file_path}' の処理中に問題が発生しました - {e}")
    if timestamps:
        with open(folder_path + "timestamp.txt", "w", encoding="utf-8") as f:
            for ts in timestamps:
                f.write(ts + "\n")
        print(f"\n完了！ 'timestamp_mp4.txt' に保存されました。")
    else:
        print("\n指定されたフォルダにMP4ファイルが見つかりませんでした。")

if __name__ == "__main__":

    target_folder = "outputs/"

    if os.path.exists(target_folder):
        create_mp4_timestamps(target_folder)
    else:
        print(f"エラー: フォルダ '{target_folder}' が見つかりません。")