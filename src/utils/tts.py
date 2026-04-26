import os
import io
import re
import time
import requests
import subprocess

from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

def text_to_audio(text, speaker=13, speed=1.0, pitch=0.0, timeout=15, url="http://localhost:50021/", buffer_duration=500):
    """
    VOICEVOX APIを使ってテキストを音声に変換し、話速と音高を調整する関数。
    Args:
        text (str): 変換するテキスト
        speaker (int): スピーカーID
        speed (float): 話速調整。1.0が標準で、値を大きくすると速く、小さくすると遅くなる。
        pitch (float): 音高調整。0.0が標準で、値を大きくすると高く、小さくすると低くなる。
        timeout (int): タイムアウト秒数
        url (str): VOICEVOX APIのURL
        buffer_duration (int): 音声の最後に付加する無音の長さ（ミリ秒）
    Returns:
        AudioSegment: 生成された音声データ
    """
    # audio_queryリクエスト
    params = {"text": cleaning_input_text(text), "speaker": speaker}
    query_synthesis_response = requests.post(url + "audio_query", params=params, timeout=timeout)
    query_synthesis_json = query_synthesis_response.json()
    # 話速と音高のパラメータをJSONに設定
    query_synthesis_json["speedScale"] = speed
    query_synthesis_json["pitchScale"] = pitch
    # synthesisリクエスト
    synthesis_response = requests.post(url + "synthesis", params=params, json=query_synthesis_json)
    # レスポンスから音声データを取得
    audio_segment = AudioSegment.from_file(io.BytesIO(synthesis_response.content), format="wav")
    # 無音バッファを追加
    silent_buffer = AudioSegment.silent(duration=buffer_duration, frame_rate=audio_segment.frame_rate)
    return audio_segment + silent_buffer

def cleaning_input_text(text):
    text = re.sub("[「・」]", "", text)
    text = re.sub("、", ",", text)
    text = re.sub("。", ".", text)
    return text

class VoicevoxController:
    def __init__(self):
        self.process = None
        # 環境変数からパスを取得
        self.app_path = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'VOICEVOX', 'VOICEVOX.exe')

    def start(self, timeout=30):
        """VOICEVOXを起動し、APIが準備OKになるまで待機する"""
        if not os.path.exists(self.app_path):
            print(f"エラー: {self.app_path} が見つかりません。")
            return False
        
        # すでにプロセスがあるか確認
        if self.process is None or self.process.poll() is not None:
            print("VOICEVOXを起動しています...")
            self.process = subprocess.Popen(
                [self.app_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # --- 起動完了の待機処理を追加 ---
            start_time = time.time()
            while True:
                try:
                    # APIのヘルスチェック（エンジンが生きているか確認）
                    response = requests.get("http://localhost:50021/version", timeout=1)
                    if response.status_code == 200:
                        print("VOICEVOXの準備が完了しました。")
                        return True
                except requests.exceptions.ConnectionError:
                    # まだ起動していない場合は待機
                    pass
                
                if time.time() - start_time > timeout:
                    print("エラー: 起動タイムアウトです。")
                    return False
                
                time.sleep(1) # 1秒おきにチェック
            # -------------------------------
        return True

    def stop(self):
        if self.process and self.process.poll() is None:
            print("VOICEVOXを終了しています...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def __del__(self):
        self.stop()

vc = VoicevoxController()
vc.start()
    
