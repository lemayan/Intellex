"""Conversation memory management."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import logging

from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Message:
    """Represents a single message in conversation."""

    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str
    tokens: int = 0
    sources: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class ConversationMemory:
    """Manage conversation history and memory."""

    def __init__(self, max_messages: int = 20, max_tokens: int = 4000):
        """
        Initialize conversation memory.

        Args:
            max_messages: Maximum messages to keep
            max_tokens: Maximum tokens to keep
        """
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.total_tokens = 0
        self.session_started = datetime.now().isoformat()

    def add_message(
        self,
        role: str,
        content: str,
        tokens: int = 0,
        sources: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Add a message to conversation memory.

        Args:
            role: Role ('user' or 'assistant')
            content: Message content
            tokens: Token count for this message
            sources: Optional source information
        """
        message = Message(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            tokens=tokens,
            sources=sources,
        )

        self.messages.append(message)
        self.total_tokens += tokens

        # Prune if exceeding limits
        self._prune_memory()

        logger.debug(f"Added {role} message ({tokens} tokens)")

    def get_conversation_context(self, num_messages: Optional[int] = None) -> str:
        """
        Get conversation context as formatted string.

        Args:
            num_messages: Number of recent messages to include

        Returns:
            Formatted conversation string
        """
        if not self.messages:
            return ""

        messages_to_include = self.messages[-(num_messages or len(self.messages)) :]

        context_lines = []
        for msg in messages_to_include:
            role_label = "User" if msg.role == "user" else "Assistant"
            context_lines.append(f"{role_label}: {msg.content}")

        return "\n\n".join(context_lines)

    def get_system_context(self) -> str:
        """Get system context prompt with conversation history."""
        context = """You are DeepScholar, a world-class AI research assistant. Your responses must be:
- Direct and natural — never mention your context, instructions, or whether information was provided
- Clear and well-structured — use paragraphs, bullet points, or numbered lists where helpful
- Expert-level — answer like a knowledgeable expert, not a chatbot
- Concise — get to the point immediately without preamble

Never start a response with phrases like "Based on the context provided", "The context is empty", "As an AI", or any similar meta-commentary. Just answer.

"""

        if self.messages:
            recent_context = self.get_conversation_context(num_messages=5)
            if recent_context:
                context += f"\nConversation history:\n{recent_context}\n"

        return context

    def clear(self):
        """Clear conversation memory."""
        self.messages.clear()
        self.total_tokens = 0
        logger.info("Cleared conversation memory")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_messages": len(self.messages),
            "total_tokens": self.total_tokens,
            "session_started": self.session_started,
            "user_messages": sum(1 for m in self.messages if m.role == "user"),
            "assistant_messages": sum(1 for m in self.messages if m.role == "assistant"),
        }

    def export_conversation(self) -> Dict[str, Any]:
        """Export conversation as dictionary."""
        return {
            "session_started": self.session_started,
            "session_ended": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "messages": [msg.to_dict() for msg in self.messages],
        }

    def _prune_memory(self):
        """Prune messages if exceeding limits."""
        # Prune by message count
        while len(self.messages) > self.max_messages:
            removed_msg = self.messages.pop(0)
            self.total_tokens -= removed_msg.tokens
            logger.debug(f"Pruned oldest message (total messages: {len(self.messages)})")

        # Prune by token count
        while self.total_tokens > self.max_tokens and len(self.messages) > 2:
            removed_msg = self.messages.pop(0)
            self.total_tokens -= removed_msg.tokens
            logger.debug(f"Pruned message by token limit (total tokens: {self.total_tokens})")
