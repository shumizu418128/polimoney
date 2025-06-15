"""画像の内容を解析し、結果をJSONファイルとして保存するスクリプト。"""

from __future__ import annotations

import argparse
import concurrent.futures
import logging
import os
import sys
from pathlib import Path

from analyzer.client import create_llm_client
from analyzer.file_io import FileIO
from analyzer.image_processor import OUTPUT_JSON_DIR, ImageProcessor

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("analyzer")


def main() -> None:
    """
    スクリプトのエントリーポイント。

    コマンドライン引数をパースし、指定されたPNG画像ファイルまたは
    ディレクトリ内の全PNGファイルを解析し、
    その結果をJSONファイルとして保存します。

    Args:
        なし (コマンドライン引数で指定)

    Returns:
        なし (標準出力・標準エラー出力、およびファイル出力)

    Raises:
        SystemExit: 必要な環境変数が未設定、またはファイル/ディレクトリが
                    存在しない場合。

    注意:
        - GOOGLE_API_KEY環境変数が必要です。
        - 画像ファイルはPNG形式のみ対応しています。
        - 解析結果は指定した出力ディレクトリにJSONファイルとして保存されます。

    """
    parser = argparse.ArgumentParser(
        description=(
            "画像の内容を解析し、"
            "結果をJSONファイルとして保存します。"
            " 単一ファイルまたはディレクトリ内の全PNGファイルを処理できます。"
        ),
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "image_file",
        nargs="?",
        default=None,
        help="解析する単一の画像ファイルのパス。",
    )
    input_group.add_argument(
        "-i",
        "--input",
        help="解析するPNG画像が含まれるディレクトリのパス。",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        default=OUTPUT_JSON_DIR,
        help=(f"解析結果のJSONファイルを保存するディレクトリ。\nデフォルト: '{OUTPUT_JSON_DIR}'"),
    )

    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=min(32, os.cpu_count() or 1 * 2),
        help="並列処理を行うスレッド数。",
    )

    parser.add_argument(
        "-p",
        "--provider",
        default="google",
        choices=["google", "anthropic", "openai"],
        help="使用するLLMプロバイダー。デフォルト: 'google'",
    )

    parser.add_argument(
        "-s",
        "--skip-if-exists",
        action="store_true",
        help="出力先のJSONファイルが既に存在する場合は処理をスキップする。",
    )

    args = parser.parse_args()

    # プロバイダーに応じた環境変数のチェック
    if args.provider == "google":
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("エラー: 環境変数 GOOGLE_API_KEY が設定されていません。")
            sys.exit(1)
    elif args.provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("エラー: 環境変数 ANTHROPIC_API_KEY が設定されていません。")
            sys.exit(1)
    elif args.provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("エラー: 環境変数 OPENAI_API_KEY が設定されていません。")
            sys.exit(1)
    else:
        api_key = None

    # ファイルI/Oハンドラの作成
    file_io = FileIO()

    # LLMクライアントの作成
    llm_client = create_llm_client(
        provider=args.provider,
        image_loader=file_io,
        file_writer=file_io,
    )
    logger.info("LLMモデル: %s", llm_client.config.get_model_name())

    # 画像プロセッサの作成
    image_processor = ImageProcessor(llm_client, skip_if_exists=args.skip_if_exists)

    output_dir = Path(args.output_dir)

    try:
        FileIO.ensure_directory(output_dir)
        logger.info("出力ディレクトリ: %s", output_dir)
    except OSError:
        logger.exception(
            "エラー: 出力ディレクトリ '%s' の作成に失敗しました。",
            output_dir,
        )
        sys.exit(1)

    # 処理対象のPNGファイルを取得
    try:
        directory = Path(args.input) if args.input else None
        image_file = Path(args.image_file) if args.image_file else None
        png_files = ImageProcessor.get_png_files_to_process(directory, image_file)
    except ValueError:
        logger.exception("PNG処理ファイルの取得中にエラーが発生しました")
        sys.exit(1)

    total_files = len(png_files)

    if total_files == 0:
        logger.error("エラー: 処理対象のPNGファイルが見つかりませんでした。")
        sys.exit(1)

    logger.info("%s 個のPNGファイルを処理します。", total_files)

    def process_with_index(
        args_tuple: tuple[int, Path],
    ) -> tuple[Path, bool]:
        i, png_file_path = args_tuple
        logger.info("--- Processing file %s/%s ---", i + 1, total_files)
        success = image_processor.process_single_image(
            png_file_path,
            output_dir,
        )
        return png_file_path, success

    max_workers = args.workers
    logger.info("並列処理を開始します (最大 %s スレッド)", max_workers)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        indexed_files = list(enumerate(png_files))
        results = list(executor.map(process_with_index, indexed_files))

        success_count = sum(1 for _, success in results if success)
        failed_count = total_files - success_count

        llm_client.save_error_log(output_dir)

    logger.info("--- 全 %s ファイルの処理が完了しました ---", total_files)
    logger.info("成功: %s ファイル, 失敗: %s ファイル", success_count, failed_count)

    if failed_count > 0:
        logger.error(
            "エラーログは %s に保存されました",
            output_dir / "error_log.json",
        )


if __name__ == "__main__":
    main()
