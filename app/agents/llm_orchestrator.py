"""LLM Orchestration for DeepScholar."""

from typing import Optional, Dict, Any
import logging

from config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


class LLMOrchestrator:
    """Orchestrate interactions with LLMs."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM orchestrator.

        Args:
            provider: LLM provider (openai, gemini)
            model: Model name
        """
        self.provider = provider or settings.llm_provider
        self.model = model or settings.openai_model
        self._initialize_client()

    def _initialize_client(self):
        """Initialize LLM client based on provider."""
        if self.provider == "openai":
            try:
                from openai import OpenAI

                self.client = OpenAI(api_key=settings.openai_api_key)
                logger.info(f"Initialized OpenAI LLM: {self.model}")
            except ImportError:
                raise ImportError("openai package required for OpenAI provider")

        elif self.provider == "gemini":
            try:
                import google.generativeai as genai

                genai.configure(api_key=settings.gemini_api_key)
                self.client = genai.GenerativeModel(settings.gemini_model)
                logger.info(f"Initialized Gemini LLM: {self.model}")
            except ImportError:
                raise ImportError("google-generativeai package required for Gemini")

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate(
        self,
        prompt: str,
        system_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs,
    ) -> str:
        """
        Generate response from LLM.

        Args:
            prompt: User prompt
            system_context: System context/instructions
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response
        """
        if self.provider == "openai":
            return self._generate_openai(prompt, system_context, temperature, max_tokens)
        elif self.provider == "gemini":
            return self._generate_gemini(prompt, system_context, temperature, max_tokens)

    def _generate_openai(
        self,
        prompt: str,
        system_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate using OpenAI API."""
        try:
            messages = []

            if system_context:
                messages.append({"role": "system", "content": system_context})

            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating with OpenAI: {str(e)}")
            raise

    def _generate_gemini(
        self,
        prompt: str,
        system_context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate using Gemini API."""
        try:
            full_prompt = f"{system_context}\n\n{prompt}" if system_context else prompt

            response = self.client.generate_content(
                full_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )

            return response.text

        except Exception as e:
            logger.error(f"Error generating with Gemini: {str(e)}")
            raise

    def stream_generate(
        self,
        prompt: str,
        system_context: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs,
    ):
        """
        Stream generation from LLM.

        Args:
            prompt: User prompt
            system_context: System context
            temperature: Temperature for generation

        Yields:
            Response chunks
        """
        if self.provider == "openai":
            yield from self._stream_openai(prompt, system_context, temperature)
        elif self.provider == "gemini":
            yield from self._stream_gemini(prompt, system_context, temperature)

    def _stream_openai(
        self, prompt: str, system_context: Optional[str], temperature: float
    ):
        """Stream from OpenAI."""
        try:
            messages = []

            if system_context:
                messages.append({"role": "system", "content": system_context})

            messages.append({"role": "user", "content": prompt})

            with self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            ) as stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Error streaming from OpenAI: {str(e)}")
            raise

    def _stream_gemini(
        self, prompt: str, system_context: Optional[str], temperature: float
    ):
        """Stream from Gemini."""
        try:
            full_prompt = f"{system_context}\n\n{prompt}" if system_context else prompt

            response = self.client.generate_content(
                full_prompt,
                stream=True,
                generation_config={"temperature": temperature},
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Error streaming from Gemini: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        """Estimate token count."""
        # Rough approximation
        return max(len(text) // 4, len(text.split()) // 1.3)
