from fastapi import APIRouter, HTTPException, Response
import requests
import json
import os
from ..schemas.speech import SpeechRequest

router = APIRouter()

# voice_mappings.jsonの読み込み
DEFAULT_MAPPING_PATH = "/app/voice_mappings.json"
VOICE_MAPPINGS_PATH = os.getenv("VOICE_MAPPINGS_PATH", DEFAULT_MAPPING_PATH)

def load_voice_mappings():
    """音声IDマッピングを読み込む"""
    try:
        with open(VOICE_MAPPINGS_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load voice mappings: {e}")
        return {}

def get_speaker_id(voice: str) -> int:
    """
    音声名またはIDからスピーカーIDを取得
    
    Args:
        voice: 音声名または音声ID
        
    Returns:
        int: スピーカーID
    """
    mappings = load_voice_mappings()
    
    # マッピングに存在する場合はマッピングされたIDを返す
    if voice in mappings:
        return int(mappings[voice])
    
    # 直接数値が指定された場合はそのまま返す
    try:
        return int(voice)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid voice: {voice}. Available voices: {', '.join(mappings.keys())}"
        )

@router.post("/v1/audio/speech", summary="テキストを音声に変換")
async def create_speech(request: SpeechRequest):
    """
    テキストを音声に変換するエンドポイント（OpenAI TTS API互換）
    
    Args:
        request: 音声合成リクエスト
        
    Returns:
        dict: 音声データとフォーマット情報
        
    Raises:
        HTTPException: VOICEVOXエンジンとの通信に失敗した場合
    """
    # VOICEVOXのAPIエンドポイント
    voicevox_url = os.getenv("VOICEVOX_ENGINE_URL", "http://voicevox_engine:50021")
    audio_query_url = f"{voicevox_url}/audio_query"
    synthesis_url = f"{voicevox_url}/synthesis"

    # スピーカーIDを取得（voiceパラメータから）
    speaker_id = get_speaker_id(request.voice)

    try:
        # VOICEVOXのクエリを作成
        query_response = requests.post(
            audio_query_url,
            params={"text": request.input, "speaker": speaker_id}
        )
        query_response.raise_for_status()
        query_data = query_response.json()

        # 読み上げ速度を設定
        query_data["speedScale"] = request.speed

        # 音声合成を実行
        synthesis_response = requests.post(
            synthesis_url,
            params={"speaker": speaker_id},
            json=query_data
        )
        synthesis_response.raise_for_status()

        # レスポンスを返す
        return Response(
            content=synthesis_response.content,
            media_type="audio/mpeg"
        )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"VOICEVOXエンジンとの通信に失敗しました: {str(e)}"
        )
