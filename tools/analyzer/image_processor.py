"""画像処理と解析を行うモジュール"""

from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING

from analyzer.client import AnalysisError
from analyzer.llm_client import LangChainLLMClient

if TYPE_CHECKING:
    from pathlib import Path

# ロガーの設定
logger = logging.getLogger("analyzer")

# 出力ディレクトリ名を定数化
OUTPUT_JSON_DIR = "output_json"


class ImageProcessor:
    """画像処理と解析を行うクラス"""

    def __init__(self, llm_client: LangChainLLMClient, skip_if_exists: bool = False) -> None:
        """
        ImageProcessorを初期化します。

        Args:
            llm_client: LLMクライアント
            skip_if_exists: 既存のJSONファイルをスキップするかどうか

        """
        self.llm_client = llm_client
        self.skip_if_exists = skip_if_exists

    def process_single_image(
        self,
        image_path: Path,
        output_dir: Path,
    ) -> bool:
        """
        単一の画像ファイルを処理し、結果をJSONファイルに保存します。

        Args:
            image_path: 処理する画像ファイルのパス
            output_dir: 出力ディレクトリのパス

        Returns:
            処理が成功した場合はTrue、失敗した場合はFalse

        """
        image_filename = image_path.name
        output_filename = output_dir / f"{image_path.stem}.json"

        # skip_if_existsが有効で、出力ファイルが既に存在する場合はスキップ
        if self.skip_if_exists and output_filename.exists():
            logger.info("スキップ: %s (出力ファイルが既に存在します)", image_filename)
            return True

        logger.info("画像を解析中: %s", image_filename)
        try:
            # クライアントの種類に応じて適切なメソッドを呼び出す
            result = self.llm_client.analyze_image_with_llm(image_path)
        except AnalysisError as e:
            logger.exception("エラー: %s", e.message)
            return False

        try:
            json.loads(result)
        except json.JSONDecodeError as json_err:
            logger.warning(
                "警告 (%s): vLLMからの応答は有効なJSONではありません。エラー: %s",
                image_filename,
                json_err,
            )
            logger.warning("応答内容(最初の200文字): %s...", result[:200])

        try:
            with output_filename.open("w", encoding="utf-8") as f:
                f.write(result)
        except OSError as e:
            error_info = {
                "file": image_filename,
                "error_type": "IOError",
                "error_message": (f"解析結果のファイル書き込みに失敗しました: {output_filename} - {e}"),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.llm_client.error_items.append(error_info)
            logger.exception(
                "エラー: %s 解析結果のファイル書き込みに失敗しました: %s",
                image_filename,
                output_filename,
            )
            return False  # 処理失敗を示す
        else:
            logger.info("解析結果を保存しました: %s", output_filename)
            return True  # 処理成功を示す

    @staticmethod
    def get_png_files_to_process(directory: Path | None = None, image_file: Path | None = None) -> list[Path]:
        """
        ディレクトリまたは単一ファイルから処理対象のPNGファイルリストを取得します。

        Args:
            directory: 処理対象のディレクトリ(オプション)
            image_file: 処理対象の単一ファイル(オプション)

        Returns:
            処理対象のPNGファイルパスのリスト

        Raises:
            ValueError: ディレクトリやファイルが存在しない場合、または両方とも指定されていない場合

        """
        png_files: list[Path] = []

        if directory:
            if not directory.is_dir():
                error_message = f"指定されたディレクトリが見つかりません: {directory}"
                raise ValueError(error_message)

            logger.info("ディレクトリ '%s' 内のPNGファイルを処理します...", directory)
            png_files = sorted(directory.glob("*.png"))

            if not png_files:
                logger.warning(
                    "警告: ディレクトリ '%s' 内にPNGファイルが見つかりませんでした。",
                    directory,
                )
            return png_files

        if image_file:
            if not image_file.is_file():
                error_message = f"指定されたファイルが見つかりません: {image_file}"
                raise ValueError(error_message)
            return [image_file]

        error_message = "解析対象のファイルまたはディレクトリを指定してください。"
        raise ValueError(error_message)
