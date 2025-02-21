# OpenAI TTS API フォーマットのVOICEVOXテスト例

このディレクトリには、VOICEVOXをOpenAI TTSフォーマットで利用するためのサンプルスクリプトが含まれています。

## 🚀 セットアップ

1. 依存パッケージのインストール:
```bash
pip install -r requirements.txt
```

2. VOICEVOXサービスの起動:
プロジェクトのルートディレクトリで以下のコマンドを実行：
```bash
docker-compose up -d
```

## 📝 使用方法

サンプルスクリプトを実行：
```bash
python tts_example.py
```

このスクリプトは以下のテストケースを実行します：
1. 標準設定での音声生成
2. 高速読み上げテスト
3. 異なる話者での読み上げテスト

生成された音声ファイルは`output`ディレクトリに保存されます。

## 🎯 カスタマイズ

`tts_example.py`の`test_cases`配列を編集することで、異なるテキストや設定でテストを行うことができます。

設定可能なパラメータ：
- `text`: 読み上げるテキスト
- `speaker_id`: VOICEVOXの話者ID（1, 2, 3, ...）
- `speed`: 読み上げ速度（1.0が標準）
