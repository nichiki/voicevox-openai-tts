from pydantic import BaseModel

class SpeechRequest(BaseModel):
    """
    OpenAI TTS API互換のリクエストモデル
    
    Attributes:
        model: 使用するモデル（現在は"voicevox-v1"のみサポート）
        input: 読み上げるテキスト
        voice: 音声指定（音声名またはVOICEVOXのスピーカーID）
               音声名: "alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"
               または直接スピーカーIDを指定（例: "1"）
        response_format: 出力フォーマット（現在は"mp3"のみサポート）
        speed: 読み上げ速度（1.0がデフォルト）
    """
    model: str
    input: str
    voice: str
    response_format: str = "mp3"
    speed: float = 1.0
