from fastapi import APIRouter, HTTPException
from ..schemas.chat import ChatCompletionRequest, Message, ChatCompletionResponse, Choice, Usage
from random import choice

router = APIRouter()

@router.post("/v1/chat/completions", summary="ChatGPT互換エンドポイント")
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
