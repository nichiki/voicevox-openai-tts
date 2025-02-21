from pydantic import BaseModel
from typing import List, Optional


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
