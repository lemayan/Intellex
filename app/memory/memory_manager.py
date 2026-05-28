"""Memory manager for DeepScholar."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

from app.utils.logger import get_logger
from .conversation_memory import ConversationMemory

logger = get_logger(__name__)


class MemoryManager:
    """Manage both session and persistent memory."""

    def __init__(self, memory_dir: str = "./data/memory"):
        """
        Initialize memory manager.

        Args:
            memory_dir: Directory for storing memory files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.session_dir = self.memory_dir / "sessions"
        self.persistent_dir = self.memory_dir / "persistent"
        self.session_dir.mkdir(exist_ok=True)
        self.persistent_dir.mkdir(exist_ok=True)

        # In-memory conversation
        self.current_conversation = ConversationMemory()
        self.session_id = None

    def start_session(self, session_id: Optional[str] = None) -> str:
        """
        Start a new memory session.

        Args:
            session_id: Optional custom session ID

        Returns:
            Session ID
        """
        import uuid
        from datetime import datetime

        self.session_id = session_id or str(uuid.uuid4())
        self.current_conversation = ConversationMemory()

        logger.info(f"Started new session: {self.session_id}")
        return self.session_id

    def save_session(self) -> Path:
        """
        Save current session to disk.

        Returns:
            Path to saved session file
        """
        if not self.session_id:
            logger.warning("No active session to save")
            return None

        session_data = self.current_conversation.export_conversation()
        session_file = self.session_dir / f"{self.session_id}.json"

        try:
            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2)
            logger.info(f"Saved session: {session_file}")
            return session_file
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            return None

    def load_session(self, session_id: str) -> bool:
        """
        Load a previous session.

        Args:
            session_id: Session ID to load

        Returns:
            True if successful, False otherwise
        """
        session_file = self.session_dir / f"{session_id}.json"

        if not session_file.exists():
            logger.warning(f"Session file not found: {session_file}")
            return False

        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)

            self.session_id = session_id
            self.current_conversation = ConversationMemory()

            # Load messages from session data
            for msg_data in session_data.get("messages", []):
                self.current_conversation.add_message(
                    role=msg_data["role"],
                    content=msg_data["content"],
                    tokens=msg_data.get("tokens", 0),
                    sources=msg_data.get("sources"),
                )

            logger.info(f"Loaded session: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error loading session: {str(e)}")
            return False

    def list_sessions(self) -> List[str]:
        """
        List all available sessions.

        Returns:
            List of session IDs
        """
        sessions = [f.stem for f in self.session_dir.glob("*.json")]
        return sorted(sessions, reverse=True)

    def save_memory(self, memory_key: str, data: Any):
        """
        Save persistent memory data.

        Args:
            memory_key: Key for the memory
            data: Data to save
        """
        try:
            file_path = self.persistent_dir / f"{memory_key}.json"
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved memory: {memory_key}")
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")

    def load_memory(self, memory_key: str) -> Optional[Any]:
        """
        Load persistent memory data.

        Args:
            memory_key: Key for the memory

        Returns:
            Loaded data or None if not found
        """
        try:
            file_path = self.persistent_dir / f"{memory_key}.json"
            if file_path.exists():
                with open(file_path, "r") as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error loading memory: {str(e)}")
            return None

    def get_conversation(self) -> ConversationMemory:
        """Get current conversation memory."""
        return self.current_conversation
