import os
import io
import re
import requests

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
    params = {"text": text, "speaker": speaker}
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
