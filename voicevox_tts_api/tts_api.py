from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import requests
from typing import List, Optional, Union
from typing import Optional

app = FastAPI(
    title="VOICEVOX OpenAI TTS API",
    description="VOICEVOXエンジンをOpenAIの音声合成APIフォーマットで利用するためのAPI",
    version="1.0.0"
)

class Message(BaseModel):
    """
    チャットメッセージモデル
    """
    role: str
    content: str
    name: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    """
    Chat Completion APIリクエストモデル
    """
    model: str
    messages: List[Message]
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    user: Optional[str] = None

class Choice(BaseModel):
    """
    Chat Completion APIレスポンスの選択肢モデル
    """
    index: int
    message: Message
    finish_reason: str = "stop"

class Usage(BaseModel):
    """
    APIの使用状況モデル
    """
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    choices: List[Choice]
    usage: Usage

class SpeechRequest(BaseModel):
    """
    OpenAI TTS API互換のリクエストモデル
    
    Attributes:
        model: 使用するモデル（現在は"voicevox-v1"のみサポート）
        input: 読み上げるテキスト
        voice: VOICEVOXのスピーカーID
        response_format: 出力フォーマット（現在は"mp3"のみサポート）
        speed: 読み上げ速度（1.0がデフォルト）
    """
    model: str
    input: str
    voice: str
    response_format: str = "mp3"
    speed: float = 1.0

@app.post("/v1/chat/completions", summary="ChatGPT互換エンドポイント")
async def create_chat_completion(request: ChatCompletionRequest):
    """
    ChatGPT互換のエンドポイント。
    現在は簡易的な応答のみを返します。
    
    Args:
        request: ChatGPT APIリクエスト
        
    Returns:
        ChatCompletionResponse: ChatGPT API互換のレスポンス
    """
    # メッセージの最後のユーザー入力を取得
    user_message = next(
        (msg for msg in reversed(request.messages) if msg.role == "user"),
        None
    )
    
    if not user_message:
        raise HTTPException(
            status_code=400,
            detail="ユーザーメッセージが見つかりません"
        )

    # ダミーレスポンスのテンプレート
    dummy_responses = [
        "はい、承知しました。ご要望についてお答えいたします。",
        "ご質問ありがとうございます。",
        "なるほど、興味深い質問ですね。",
        "ご指摘の点について、詳しく説明させていただきます。",
        "はい、それは素晴らしいアイデアですね。"
    ]
    
    # ユーザーのメッセージに基づいて、適切なダミーレスポンスを選択
    from random import choice
    base_response = choice(dummy_responses)
    
    # ユーザーのメッセージの一部を引用してレスポンスを作成
    user_content = user_message.content[:50]  # 最初の50文字を使用
    if len(user_message.content) > 50:
        user_content += "..."

    # レスポンスを組み立て
    response_content = f"{base_response}\n\n{user_content}について、詳細な分析と提案をご提供できます。具体的なアクションプランを立てて進めていきましょう。"

    response_message = Message(
        role="assistant",
        content=response_content
    )

    return ChatCompletionResponse(
        id="chatcmpl-voicevox",
        choices=[
            Choice(index=0, message=response_message)
        ],
        usage=Usage(
            prompt_tokens=len(user_message.content.split()),
            completion_tokens=len(response_message.content.split()),
            total_tokens=len(user_message.content.split()) + len(response_message.content.split())
        )
    )

@app.post("/audio/speech", summary="テキストを音声に変換")
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
