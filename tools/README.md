# PDF Image Analyzer with vLLM

このプロジェクトは、PDFファイルの各ページを画像に変換し、langchain を使用して画像の内容（特に政治資金収支報告書を想定）を解析し、結果をJSONファイルとして出力するツール群を提供します。

## 機能

*   **PDFから画像へ変換 (`pdf_to_images.py`)**:
    *   指定されたPDFファイルの各ページをPNG画像に変換します。
    *   出力ファイル名はゼロ埋めされたページ番号を含み、ソート時に正しい順序になります (例: `document_page_001.png`)。
    *   出力先ディレクトリを指定できます（デフォルト: `output_images`）。
*   **画像解析とJSON出力 (`analyze_image.py`)**:
    *   指定された画像ファイルまたはディレクトリ内の全PNG画像をLLMを使用して解析します。
    *   政治資金収支報告書の画像からテキスト情報を抽出し、構造化されたJSON形式で出力するように設計されたデフォルトプロンプトが含まれています。プロンプトは引数で変更可能です。
    *   解析結果は指定されたディレクトリ（デフォルト: `output_json`）にJSONファイルとして保存されます (例: `document_page_001.json`)。
    *   APIからの応答に含まれる可能性のあるマークダウン指示子 (` ```json ` など) は自動的に除去されます。
*  **画像ごとのJSONを一つにマージ（`merge_jsons.py`）**
    *  output_json のファイルを merged_files に結合します

```
[ワークフロー]

PDFファイル
↓ pdf_to_image.py
エクセルもしくはPDFのスクリーンショット群（output_images/*.png）
↓ analyze_image.py
パースされたJSONファイル群（output_json/*.json）
↓ merge_jsons.py
とりまとめられた単一のjsonとcsv

```


## 必要なもの

*   **Python**: 3.10 以上推奨
*   **Poppler**: `pdf2image` がPDFを処理するために必要です。
    *   **macOS**: `brew install poppler`
    *   **Debian/Ubuntu**: `sudo apt-get update && sudo apt-get install -y poppler-utils`
    *   **Windows**: [公式ドキュメント](https://pdf2image.readthedocs.io/en/latest/installation.html)に従ってインストールし、PATHを通すか、スクリプト内でパスを指定する必要があります。
*   **Google API Key**: Gemini API を利用するために必要です。Google AI Studio などで取得してください。

## セットアップ

1.  **リポジトリのクローン (もしあれば)**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **仮想環境の作成 (推奨)**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate  # Windows
    ```
3.  **依存関係のインストール**:
    *   `pyproject.toml` がある場合 (Poetry):
        ```bash
        pip install poetry
        poetry install
        ```
    *   手動の場合:
        ```bash
        pip install pdf2image google-generativeai Pillow python-dotenv
        ```
        (`python-dotenv` は `.env` ファイルからAPIキーを読み込む場合に便利です)

4.  **Google API Key の設定**:
    環境変数 `GOOGLE_API_KEY` に取得したAPIキーを設定します。
    ```bash
    export GOOGLE_API_KEY='YOUR_API_KEY'
    ```
    または、プロジェクトルートに `.env` ファイルを作成し、以下のように記述します:
    ```.env
    GOOGLE_API_KEY='YOUR_API_KEY'
    ```
    `.env` ファイルを使用する場合は、スクリプト実行前に `dotenv` を使って読み込むか、`analyze_image.py` 内で `load_dotenv()` を呼び出すように修正が必要です（現在のスクリプトには含まれていません）。

## lint, format

```bash
# lint
poetry run ruff check .
# lint 自動修正あり
poetry run ruff check --fix .
# format
poetry run ruff format .
# type check
poetry run pyright .
```

## 使い方

1.  **政治資金収支報告書をダウンロード**:

    ```bash
    python -m downloader.main -y R5
    ```

    詳しくは [downloader/README.md](downloader/README.md) を参照してください。


2.  **PDFを画像に変換**:
    ```bash
    python pdf_to_images.py <your_document.pdf> -o output_images --preprocess grayscale binarize
    ```
    これにより、`output_images` ディレクトリに `your_document_page_001.png`, `your_document_page_002.png`, ... が生成されます。  
    `--preprocess` オプションを指定すると、変換後に画像の前処理を行い、結果を `output_images/processed` に保存します。

3.  **画像を解析してJSONを生成**:
    *   **単一の画像ファイル**:
        ```bash
        python analyze_image.py output_images/your_document_page_001.png -o output_json
        ```
    *   **ディレクトリ内の全PNG画像**:
        ```bash
        python analyze_image.py -i output_images -o output_json
        ```
    これにより、`output_json` ディレクトリに `your_document_page_001.json`, `your_document_page_002.json`, ... が生成されます。

## 注意点

*   vLLM API の利用には料金が発生する場合があります。Google Cloud Platform の料金体系を確認してください。
*   解析結果の精度は、画像の品質、複雑さ、およびvLLMモデルの能力に依存します。
*   大量のページを処理する場合、APIのレート制限に達する可能性があります。必要に応じてスクリプトに待機処理などを追加してください。
