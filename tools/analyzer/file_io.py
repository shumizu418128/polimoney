"""ファイル入出力操作を行うモジュール"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Protocol

import PIL.Image

if TYPE_CHECKING:
    from pathlib import Path

# ロガーの設定
logger = logging.getLogger("analyzer")


class ImageLoader(Protocol):
    """画像ローダーのインターフェース"""

    def load_image(self, image_path: Path) -> PIL.Image.Image:
        """
        画像ファイルを読み込みます。

        Args:
            image_path: 画像ファイルのパス

        Returns:
            読み込まれた画像オブジェクト

        Raises:
            FileNotFoundError: 画像ファイルが見つからない場合
            PIL.UnidentifiedImageError: 画像形式が認識できない場合
            OSError: その他のI/Oエラーが発生した場合

        """
        ...


class FileWriter(Protocol):
    """ファイル書き込みのインターフェース"""

    def write_file(self, path: Path, content: str) -> None:
        """
        ファイルに内容を書き込みます。

        Args:
            path: 書き込み先のファイルパス
            content: 書き込む内容

        Raises:
            OSError: ファイル書き込みエラーが発生した場合

        """
        ...


class FileIO:
    """ファイル入出力操作を行うクラス"""

    @staticmethod
    def load_image(image_path: Path) -> PIL.Image.Image:
        """
        画像ファイルを読み込みます。

        Args:
            image_path: 画像ファイルのパス

        Returns:
            読み込まれた画像オブジェクト

        Raises:
            FileNotFoundError: 画像ファイルが見つからない場合
            PIL.UnidentifiedImageError: 画像形式が認識できない場合
            OSError: その他のI/Oエラーが発生した場合

        """
        return PIL.Image.open(image_path)

    @staticmethod
    def write_file(path: Path, content: str) -> None:
        """
        ファイルに内容を書き込みます。

        Args:
            path: 書き込み先のファイルパス
            content: 書き込む内容

        Raises:
            OSError: ファイル書き込みエラーが発生した場合

        """
        with path.open("w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def write_json(path: Path, data: dict) -> None:
        """
        JSONデータをファイルに書き込みます。

        Args:
            path: 書き込み先のファイルパス
            data: 書き込むJSONデータ

        Raises:
            OSError: ファイル書き込みエラーが発生した場合

        """
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """
        ディレクトリが存在することを確認し、存在しない場合は作成します。

        Args:
            directory: 確認/作成するディレクトリのパス

        Raises:
            OSError: ディレクトリ作成エラーが発生した場合

        """
        directory.mkdir(parents=True, exist_ok=True)
