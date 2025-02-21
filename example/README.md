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

### シンプルな実装
基本的な機能を試す場合：
```bash
python simple_tts_example.py
```

このスクリプトは基本的な音声合成のみを実行し、output/simple_test.mp3に保存します。
コードはシンプルで理解しやすく、ログ出力機能も備えています。

### 詳細な実装
複数のテストケースを実行する場合：
```bash
python tts_example.py
```

このスクリプトは以下のテストケースを実行します：
1. 標準設定での音声生成
2. 高速読み上げテスト
3. 異なる話者での読み上げテスト

生成された音声ファイルは`output`ディレクトリに保存されます。

## 🎯 カスタマイズ

### シンプルな実装（simple_tts_example.py）
以下の変数を編集することで、基本的な設定を変更できます：
- `text`: 読み上げるテキスト
- `voice_id`: VOICEVOXの話者ID（1, 2, 3, ...）

### 詳細な実装（tts_example.py）
`test_cases`配列を編集することで、異なるテキストや設定でテストを行うことができます。

設定可能なパラメータ：
- `text`: 読み上げるテキスト
- `speaker_id`: VOICEVOXの話者ID（1, 2, 3, ...）
- `speed`: 読み上げ速度（1.0が標準）
