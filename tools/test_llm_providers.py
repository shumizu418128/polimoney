#!/usr/bin/env python3
"""Test script for LLM providers."""

import logging
import os
from pathlib import Path

from analyzer.config import LLMConfig, LLMProvider
from analyzer.file_io import FileIO
from analyzer.llm_client import LangChainLLMClient

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("test_llm_providers")


def test_provider(provider: str) -> None:
    """Test a specific LLM provider."""
    logger.info(f"\n{'=' * 50}")
    logger.info(f"Testing {provider.upper()} provider")
    logger.info(f"{'=' * 50}")

    try:
        # Create configuration
        config = LLMConfig(provider=LLMProvider(provider))
        logger.info("✓ Configuration created")
        logger.info(f"  - Model: {config.get_model_name()}")
        logger.info(f"  - Temperature: {config.temperature}")
        logger.info(f"  - Max tokens: {config.max_tokens}")

        # Check API key
        try:
            _ = config.get_api_key()
            logger.info("✓ API key found")
        except ValueError as e:
            logger.error(f"✗ API key error: {e}")
            return

        # Create client
        file_io = FileIO()
        client = LangChainLLMClient(config, image_loader=file_io, file_writer=file_io)
        logger.info("✓ Client created successfully")

        # Test with a sample image if provided
        test_image_path = os.getenv("TEST_IMAGE_PATH")
        if test_image_path:
            test_image = Path(test_image_path)
            if test_image.exists():
                logger.info(f"\nTesting with image: {test_image}")
                try:
                    result = client.analyze_image_with_llm(test_image)
                    logger.info("✓ Analysis completed successfully")
                    logger.info(f"  Result length: {len(result)} characters")
                    logger.info(f"  First 200 chars: {result[:200]}...")
                except Exception as e:
                    logger.error(f"✗ Analysis failed: {e}")
            else:
                logger.warning(f"Test image not found: {test_image}")
        else:
            logger.info("No test image specified (set TEST_IMAGE_PATH env var)")

    except Exception as e:
        logger.error(f"✗ Provider test failed: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Main test function."""
    logger.info("LLM Provider Test Script")
    logger.info("========================")

    # Test all providers
    providers = ["google", "anthropic", "openai"]

    for provider in providers:
        test_provider(provider)

    logger.info(f"\n{'=' * 50}")
    logger.info("Test Summary")
    logger.info(f"{'=' * 50}")
    logger.info("To use different providers with analyze_image.py:")
    logger.info("  python analyze_image.py -p google image.png")
    logger.info("  python analyze_image.py -p anthropic image.png")
    logger.info("  python analyze_image.py -p openai image.png")
    logger.info("\nMake sure to set the appropriate environment variables:")
    logger.info("  - GOOGLE_API_KEY for Google")
    logger.info("  - ANTHROPIC_API_KEY for Anthropic")
    logger.info("  - OPENAI_API_KEY for OpenAI")


if __name__ == "__main__":
    main()
