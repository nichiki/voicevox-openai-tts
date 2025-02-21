# 🎤 VOICEVOX OpenAI TTS API

VOICEVOXエンジンをOpenAIの音声合成APIフォーマットに変換するためのAPIサーバーです。

## 🌟 特徴

- OpenAIのTTS APIと同じフォーマットでリクエストを受け付け
- VOICEVOXエンジンを使用した高品質な日本語音声合成
- Dockerで簡単にデプロイ可能

## 🚀 使用方法

### 🐳 起動方法

```bash
docker-compose up -d
```

### 📝 APIエンドポイント

```bash
POST http://localhost:8000/audio/speech
```

### リクエスト形式（OpenAI互換）

```json
{
  "model": "voicevox-v1",
  "input": "こんにちは、音声合成のテストです。",
  "voice": "1",
  "response_format": "mp3",
  "speed": 1.0
}
```

### パラメータ説明

- `model`: 使用するモデル（現在は"voicevox-v1"のみ）
- `input`: 読み上げるテキスト
- `voice`: VOICEVOXのスピーカーID
- `response_format`: 出力フォーマット（現在は"mp3"のみ）
- `speed`: 読み上げ速度（デフォルト: 1.0）

### レスポンス形式

- Content-Type: `audio/mpeg`
- Body: MP3形式の音声データ（バイナリ）

### Pythonでの使用例

```python
from openai import OpenAI

# カスタムベースURLを持つOpenAIクライアントを作成
client = OpenAI(base_url="http://localhost:8000", api_key="sk-1234")

# 音声を生成
response = client.audio.speech.create(
    model="voicevox-v1",
    voice="1",
    input="こんにちは、音声合成のテストです。",
    speed=1.0
)

# 音声ファイルを保存（ストリーミングレスポンスを使用）
with response.with_streaming_response.stream_to_file("output.mp3"):
    pass
```

## 📁 プロジェクト構造

```
.
├── docker-compose.yml    # Docker構成ファイル
├── Dockerfile           # APIサーバーのビルド設定
├── voicevox_tts_api/   # OpenAI互換APIの実装
│   ├── tts_api.py      # メインAPIコード
│   └── requirements.txt # Python依存パッケージ
└── example/            # 使用例とテストスクリプト
    ├── tts_example.py  # サンプルスクリプト
    └── README.md       # サンプルの説明
```

## 🔧 システム要件

- Docker
- Docker Compose

## 🎯 サンプルコード

`example`ディレクトリに、APIの使用例とテストスクリプトが用意されています。
詳しい使い方は[example/README.md](example/README.md)を参照してください。

## 🛠️ アーキテクチャ

```
                                  ┌─────────────┐
HTTP Request (OpenAI Format) ──▶  │  TTS API    │
                                  │  (FastAPI)   │
                                  └──────┬──────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │  VOICEVOX   │
                                  │   Engine    │
                                  └─────────────┘
```

## 🔒 ライセンス

MITライセンス
