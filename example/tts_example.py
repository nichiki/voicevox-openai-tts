from pathlib import Path
import os
from openai import OpenAI
from loguru import logger
import sys

# ログの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "issue_creator.log",
    rotation="500 MB",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# カスタムベースURLを持つOpenAIクライアントを作成
client = OpenAI(base_url="http://localhost:8000", api_key="sk-1234")

def main():
    # 音声ファイルの保存パス
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    logger.info(f"出力ディレクトリを確認: {output_dir}")

    # テストケース
    test_cases = [
        {
            "text": "こんにちは。VOICEVOXのOpenAI TTSフォーマットのテストです。",
            "voice": "1",
            "description": "標準設定"
        },
        {
            "text": "スピードを変えて話すテストです。",
            "voice": "1",
            "speed": 1.5,
            "description": "高速読み上げ"
        },
        {
            "text": "別の話者での読み上げテストです。",
            "voice": "2",
            "description": "別の話者"
        }
    ]

    logger.info("VOICEVOXのOpenAI TTSフォーマットテストを開始")
    logger.debug("テストケース数: {}", len(test_cases))

    for i, test in enumerate(test_cases, 1):
        logger.info("テストケース {}: {}", i, test['description'])
        logger.debug("テストパラメータ - テキスト: {}, 話者ID: {}", test['text'], test['voice'])
        if 'speed' in test:
            logger.debug("速度パラメータ: {}", test['speed'])

        try:
            # 音声を生成
            response = client.audio.speech.create(
                model="voicevox-v1",
                voice=test['voice'],
                input=test['text'],
                speed=test.get('speed', 1.0)
            )

            # ファイル名を生成
            speech_file_path = output_dir / f"test_{i}.mp3"
            
            # 音声ファイルを保存
            with open(speech_file_path, "wb") as file:
                file.write(response.content)
            logger.success("音声ファイルを保存しました: {}", speech_file_path)

        except Exception as e:
            logger.error("音声生成中にエラーが発生: {} - テストケース: {}", str(e), test)
            continue

    logger.info("全てのテストケースの処理が完了しました")

if __name__ == "__main__":
    main()
