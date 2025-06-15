"""LangChain-based LLM client supporting multiple providers."""

from __future__ import annotations

import json
import logging
import re
import time
from typing import TYPE_CHECKING, Any, NoReturn

import PIL.Image
from langchain.schema import BaseMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from analyzer.config import LLMConfig, LLMProvider
from analyzer.file_io import FileWriter, ImageLoader
from analyzer.prompt import prompt, prompt_first_page

if TYPE_CHECKING:
    from pathlib import Path

# ロガーの設定
logger = logging.getLogger("analyzer")

# 出力ディレクトリ名を定数化
ERROR_LOG_FILE = "error_log.json"

# リトライ可能なエラーの定義
RETRYABLE_EXCEPTIONS = (
    Exception,  # 一般的な例外をリトライ対象にする
)


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


class ImageAnalysisResult(BaseModel):
    """画像分析結果のスキーマ。"""

    categories: list[dict[str, Any]] | None = None
    transactions: list[dict[str, Any]] | None = None
    year: int | None = None
    basic_info: dict[str, Any] | None = None


class LangChainLLMClient:
    """LangChain-based LLM client supporting multiple providers."""

    def __init__(
        self,
        config: LLMConfig,
        image_loader: ImageLoader | None = None,
        file_writer: FileWriter | None = None,
    ) -> None:
        """
        LangChainLLMClientを初期化します。

        Args:
            config: LLM設定
            image_loader: 画像読み込みのためのローダー(テスト用)
            file_writer: ファイル書き込みのためのライター（テスト用）

        """
        self.config = config
        self.model = self._create_model()
        self.error_items: list[dict[str, Any]] = []
        self.image_loader = image_loader
        self.file_writer = file_writer
        self.rate_limit_error_additional_wait_time = 30

    def _create_model(self) -> BaseChatModel:
        """設定に基づいてLLMモデルを作成します。"""
        provider = self.config.provider
        api_key = self.config.get_api_key()
        model_name = self.config.get_model_name()
        model_config = self.config.get_model_config()

        if provider == LLMProvider.GOOGLE:
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=model_config["temperature"] or 0.0,
                max_output_tokens=model_config["max_tokens"],
                generation_config={
                    "response_mime_type": "application/json",
                },
            )
        elif provider == LLMProvider.ANTHROPIC:
            return ChatAnthropic(
                model_name=model_name,
                api_key=SecretStr(api_key),
                temperature=model_config["temperature"],
                max_tokens_to_sample=model_config["max_tokens"],
                timeout=None,
                stop=None,
            )
        elif provider == LLMProvider.OPENAI:
            return ChatOpenAI(
                model=model_name,
                api_key=SecretStr(api_key),
                temperature=model_config["temperature"],
                max_tokens=model_config["max_tokens"],  # type: ignore
            )

        raise ValueError(f"Unsupported provider: {provider}")

    def _handle_analysis_error(
        self,
        image_filename: str,
        error_type: str,
        error_message_detail: str,
        original_exception: Exception | None = None,
    ) -> NoReturn:
        """エラー情報を記録し、AnalysisErrorを送出するヘルパーメソッド。"""
        error_info = {
            "file": image_filename,
            "error_type": error_type,
            "error_message": error_message_detail,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.error_items.append(error_info)
        log_message = f"{error_type} ({image_filename}): {error_message_detail}"
        if original_exception:
            logger.exception(log_message, exc_info=original_exception)
            raise AnalysisError(log_message, error_info) from original_exception
        # original_exception が None の場合
        logger.error(log_message)
        raise AnalysisError(log_message, error_info)

    def clean_response(self, text: str) -> str:
        """LLM応答からマークダウンコードブロック指示子を削除する。"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[len("```json") :].strip()
        elif text.startswith("```"):
            text = text[len("```") :].strip()

        if text.endswith("```"):
            text = text[: -len("```")].strip()

        return text

    def _create_message_with_image(self, prompt_text: str, image: PIL.Image.Image) -> list[BaseMessage]:
        """画像付きのメッセージを作成します。"""
        import base64
        from io import BytesIO

        # 画像をbase64にエンコード
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # すべてのプロバイダーで同じ形式を使用
        content = [
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}", "detail": "high"}},
        ]
        return [HumanMessage(content=content)]

    @retry(
        retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
        stop=stop_after_attempt(5),  # 最大5回リトライ
        wait=wait_exponential(
            multiplier=1,
            min=2,
            max=60,
        ),  # 指数バックオフ: 2秒、4秒、8秒、16秒、32秒
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _generate_content_with_retry(
        self,
        prompt_text: str,
        img: PIL.Image.Image,
    ) -> str:
        """
        リトライロジックを実装したLLM API呼び出し。

        Args:
            prompt_text: プロンプト。
            img: 画像。

        Returns:
            LLM APIからのレスポンス。

        """
        try:
            messages = self._create_message_with_image(prompt_text, img)

            # プロンプトにJSON出力の指示を追加
            json_instruction = (
                "\n\nIMPORTANT: You must respond with valid JSON only. "
                "Do not include any text outside of the JSON structure."
            )

            # 最初のメッセージのテキストに指示を追加
            if messages and isinstance(messages[0], HumanMessage):
                if isinstance(messages[0].content, list):
                    for item in messages[0].content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            item["text"] += json_instruction
                            break
                elif isinstance(messages[0].content, str):
                    messages[0].content += json_instruction

            response = self.model.invoke(
                messages,
            )

            # response.contentを文字列に変換
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list):
                # リストの場合、テキスト部分を結合
                text_parts = []
                for part in response.content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                    elif isinstance(part, str):
                        text_parts.append(part)
                return "".join(text_parts)
            else:
                return str(response.content)
        except Exception as e:
            logger.warning(
                "API呼び出しエラー: %s: %s. リトライします...",
                type(e).__name__,
                e,
            )
            # レート制限エラーの場合は追加の待機時間
            if "rate_limit" in str(e).lower() or "429" in str(e):
                time.sleep(self.rate_limit_error_additional_wait_time)
            raise

    def _process_llm_response(
        self,
        response: str,
        image_filename: str,
    ) -> str:
        """LLM APIの応答を処理し、テキスト結果またはエラーを処理します。"""
        if response:
            cleaned_response = self.clean_response(response)
            # JSON検証
            try:
                json.loads(cleaned_response)
                return cleaned_response
            except json.JSONDecodeError:
                # JSON検証に失敗した場合も一旦返す（後続の処理で警告を出す）
                return cleaned_response

        # 有効なテキスト応答がない場合のエラー処理
        error_message_detail = "LLM APIから有効なテキスト応答を取得できませんでした。"
        self._handle_analysis_error(
            image_filename,
            "LLMAPIResponseError",
            error_message_detail,
        )
        return ""  # この行は実際には実行されません

    def analyze_image_with_llm(self, image_path: Path) -> str:
        """
        指定した画像ファイルをLLM APIで解析し、JSON形式でテキスト情報を返します。

        Args:
            image_path: 解析対象の画像ファイルのパス。

        Returns:
            LLMからの解析結果 (JSON文字列を想定)。
            エラーの場合は AnalysisError を送出します。

        Raises:
            AnalysisError: 解析エラーが発生した場合。

        """
        image_filename = image_path.name

        # ページ番号を特定
        page_match = re.search(r"_page_(\d+)\.png$", image_filename)
        page_number_str = page_match.group(1) if page_match else "0"

        # int型に変換
        page_number = int(page_number_str)

        try:
            # 依存性注入されたimage_loaderがあれば使用、なければデフォルトの動作
            img = self.image_loader.load_image(image_path) if self.image_loader else PIL.Image.open(image_path)

            # 1ページ目の場合はprompt_first_pageを使用
            if image_path.name.endswith("_page_01.png"):
                selected_prompt = prompt_first_page
            # idの重複を防ぐため、ページ数に応じたidを生成
            else:
                selected_prompt = prompt.replace("__num__", str(page_number * 1000))

            try:
                response = self._generate_content_with_retry(selected_prompt, img)
                return self._process_llm_response(response, image_filename)
            except Exception as e:
                self._handle_analysis_error(
                    image_filename,
                    type(e).__name__,
                    f"最大リトライ回数を超えました: {e}",
                    original_exception=e,
                )

        except AnalysisError:  # _handle_analysis_error で処理済のため再raise
            raise
        except FileNotFoundError as e:
            self._handle_analysis_error(
                image_filename,
                "FileNotFoundError",
                f"画像ファイルが見つかりません: {image_path}",
                original_exception=e,
            )
        except (PIL.UnidentifiedImageError, OSError, RuntimeError) as e:
            self._handle_analysis_error(
                image_filename,
                type(e).__name__,
                f"予期せぬエラー発生 ({type(e).__name__}): {e}",
                original_exception=e,
            )

        return ""  # この行は実際には実行されません

    def save_error_log(self, output_dir: Path) -> None:
        """
        エラー項目をJSONファイルとして保存します。

        Args:
            output_dir: 出力ディレクトリ。

        """
        if not self.error_items:
            return

        error_log_path = output_dir / ERROR_LOG_FILE
        try:
            # 依存性注入されたfile_writerがあれば使用、なければデフォルトの動作
            if self.file_writer:
                self.file_writer.write_file(
                    error_log_path,
                    json.dumps({"errors": self.error_items}, ensure_ascii=False, indent=2),
                )
            else:
                with error_log_path.open("w", encoding="utf-8") as f:
                    json.dump({"errors": self.error_items}, f, ensure_ascii=False, indent=2)
            logger.info("エラーログを保存しました: %s", error_log_path)
        except OSError:
            logger.exception("エラーログの保存に失敗しました:")
