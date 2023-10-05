"""Text backend."""


from openssm.core.inferencer.abstract_inferencer import AbstractInferencer
from openssm.core.backend.base_backend import BaseBackend
from openssm.utils.logs import Logs


class TextBackend(BaseBackend):
    """Text backend."""

    def __init__(self):
        """Initialize text backend."""
        super().__init__()
        self.texts = []

    # pylint: disable=unused-argument
    @Logs.do_log_entry_and_exit()
    def query(self, user_input: list[dict], conversation: list[dict] = None) -> dict:
        response = {"response": self.texts}
        return response

    def all_texts(self):
        return self.texts

    def add_fact(self, fact: str):
        super().add_fact(fact)
        self.texts.append(f"fact: {fact}")

    def add_inferencer(self, inferencer: AbstractInferencer):
        super().add_inferencer(inferencer)
        self.texts.append(f"inferencer: {inferencer}")

    def add_heuristic(self, heuristic: str):
        super().add_heuristic(heuristic)
        self.texts.append(f"heuristic: {heuristic}")
