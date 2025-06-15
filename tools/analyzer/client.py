"""LLMクライアントのファクトリー関数を提供するモジュール。

このモジュールは、LLMプロバイダーに応じた適切なクライアントインスタンスを
生成するためのファクトリー関数を提供します。

主な機能:
- LLMプロバイダーの設定に基づいてクライアントを生成
- 画像読み込みとファイル書き込みの依存性注入をサポート
- エラーハンドリングとロギングの統合

使用例:
    config = LLMConfig(provider=LLMProvider.GOOGLE)
    client = create_llm_client(config)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from analyzer.config import LLMConfig
from analyzer.file_io import FileWriter, ImageLoader
from analyzer.llm_client import LangChainLLMClient

if TYPE_CHECKING:
    pass

# 出力ディレクトリ名を定数化
ERROR_LOG_FILE = "error_log.json"

# ロガーの設定
logger = logging.getLogger("analyzer")


class AnalysisError(Exception):
    """分析エラーを表す例外。"""

    def __init__(self, message: str, details: dict[str, Any]) -> None:
        """
        AnalysisErrorを初期化します。

        Args:
            message: エラーメッセージ。
            details: エラーの詳細情報。

        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """エラーメッセージと詳細を文字列として返します。"""
        return f"{self.message}: {self.details}"


def create_llm_client(
    provider: str = "google",
    image_loader: ImageLoader | None = None,
    file_writer: FileWriter | None = None,
) -> LangChainLLMClient:
    """LLMクライアントを作成するファクトリー関数。

    Args:
        provider: プロバイダー名 ("google", "anthropic", "openai")
        image_loader: 画像読み込みのためのローダー
        file_writer: ファイル書き込みのためのライター

    Returns:
        LLMクライアントのインスタンス
    """
    # 新しいLangChainベースのクライアントを使用
    from analyzer.config import LLMProvider

    config = LLMConfig(provider=LLMProvider(provider))
    return LangChainLLMClient(config, image_loader, file_writer)
