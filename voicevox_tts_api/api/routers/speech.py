from fastapi import APIRouter, HTTPException, Response
import requests
from ..schemas.speech import SpeechRequest

router = APIRouter()

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
    voicevox_url = "http://voicevox_engine:50021"
    audio_query_url = f"{voicevox_url}/audio_query"
    synthesis_url = f"{voicevox_url}/synthesis"

    # スピーカーIDを取得（voiceパラメータから）
    speaker_id = int(request.voice)

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
