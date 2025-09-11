import os
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory, SQLChatMessageHistory
from src.memory.memory import SummarizedHistoryWrapper  


class SessionManager:
    def __init__(self, memory_type="inmemory", storage_path="sessions.db", token_limit=500):
        self.memory_type = memory_type
        self.storage_path = storage_path
        self.token_limit = token_limit
        os.makedirs("session_history", exist_ok=True)

    def create_session(self, user_id: str):
        """Retourne l’historique correspondant à l’utilisateur, enveloppé avec le wrapper résumé"""
        if self.memory_type == "inmemory":
            base_history = InMemoryChatMessageHistory()
        elif self.memory_type == "file":
            base_history = FileChatMessageHistory(f"session_history/{user_id}.json")
        elif self.memory_type == "sql":
            base_history = SQLChatMessageHistory(
                session_id=user_id,
                connection_string=f"sqlite:///{self.storage_path}"
            )
        else:
            raise ValueError("Type de mémoire inconnu")

        return SummarizedHistoryWrapper(base_history, token_limit=self.token_limit)

    def reset_session(self, user_id: str):
        """Réinitialise la session en vidant l’historique"""
        if self.memory_type == "inmemory":
            base_history = InMemoryChatMessageHistory()
        elif self.memory_type == "file":
            filepath = f"session_history/{user_id}.json"
            if os.path.exists(filepath):
                os.remove(filepath)
            base_history = FileChatMessageHistory(filepath)
        elif self.memory_type == "sql":
            base_history = SQLChatMessageHistory(
                session_id=user_id,
                connection_string=f"sqlite:///{self.storage_path}"
            )
        else:
            raise ValueError("Type de mémoire inconnu")

        return SummarizedHistoryWrapper(base_history, token_limit=self.token_limit)

    def delete_session(self, user_id: str):
        """Supprime complètement la session"""
        if self.memory_type == "inmemory":
            return None
        elif self.memory_type == "file":
            filepath = f"session_history/{user_id}.json"
            if os.path.exists(filepath):
                os.remove(filepath)
            return f"Session {user_id} supprimée (fichier effacé)"
        elif self.memory_type == "sql":
            return f"Suppression manuelle requise pour {user_id} dans la base {self.storage_path}"
        else:
            raise ValueError("Type de mémoire inconnu")

    def read_session(self, user_id: str):
        """Affiche l’historique (brut ou résumé) pour un utilisateur"""
        memory = self.create_session(user_id)
        for msg in memory.messages:
            print(f"{msg.type.upper()} : {msg.content}")
