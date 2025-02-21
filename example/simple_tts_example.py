from openai import OpenAI
from loguru import logger
import sys


def main():
    """
    VOICEVOXのOpenAI TTS APIフォーマットを使用した
    シンプルな音声合成のサンプルスクリプト
    """
    # カスタムベースURLを持つOpenAIクライアントを作成
    client = OpenAI(base_url="http://localhost:8000", api_key="sk-1234")
    
    # 音声合成のリクエストパラメータを設定
    text = "こんにちは。VOICEVOXのOpenAI TTSフォーマットのテストです。"
    voice_id = "1"  # VOICEVOXの話者ID
    
    logger.info("音声合成を開始します")
    logger.debug(f"テキスト: {text}")
    logger.debug(f"話者ID: {voice_id}")
    
    try:
        # 音声を生成
        response = client.audio.speech.create(
            model="voicevox-v1",
            voice=voice_id,
            input=text
        )

        # 音声ファイルを保存
        output_file = "output/simple_test.mp3"
        with open(output_file, "wb") as file:
            file.write(response.content)
            
        logger.success(f"音声ファイルを保存しました: {output_file}")

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main()
