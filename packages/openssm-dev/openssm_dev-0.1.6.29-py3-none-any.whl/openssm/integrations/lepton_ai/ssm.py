"""SSM with Lepton-fine-tuned frontend."""


import os
from typing import Optional
from openssm.integrations.openai.ssm import SLM as OpenAISLM
from openssm.core.adapter.abstract_adapter import AbstractAdapter
from openssm.utils.config import Config
from openssm.core.ssm.base_ssm import BaseSSM
from openssm.core.backend.abstract_backend import AbstractBackend
from openssm.core.ssm.rag_ssm import RAGSSM as BaseRAGSSM, AbstractRAGBackend
from openssm.integrations.llama_index.backend import Backend as LlamaIndexBackend
from openssm.integrations.openai.ssm import APIContext as OpenAIAPIContext


Config.LEPTONAI_API_KEY: Optional[str] = os.environ.get('LEPTONAI_API_KEY') or None
Config.LEPTONAI_API_URL: Optional[str] = os.environ.get('LEPTONAI_API_URL') or None


# pylint: disable=too-many-instance-attributes
class APIContext(OpenAIAPIContext):
    """API Context."""

    @classmethod
    def from_defaults(cls):
        return APIContext.gpt3_defaults()

    @classmethod
    def gpt3_defaults(cls):
        api_context = OpenAIAPIContext.gpt3_defaults()
        api_context.key = Config.LEPTONAI_API_KEY
        api_context.base = Config.LEPTONAI_API_URL
        return api_context

    @classmethod
    def gpt4_defaults(cls):
        raise NotImplementedError("GPT-4 is not yet supported by Lepton.")


class SLM(OpenAISLM):
    """Lepton-fine-tuned SLM."""

    def __init__(self, api_context: APIContext = None, adapter: AbstractAdapter = None):
        """Initialize Lepton-fine-tuned SLM."""
        if api_context is None:
            api_context = APIContext.from_defaults()

        super().__init__(api_context, adapter)


class SSM(BaseSSM):
    """SSM with Lepton-fine-tuned frontend."""

    def __init__(self,
                 adapter: AbstractAdapter = None,
                 backends: list[AbstractBackend] = None,
                 name: str = None):
        """Initialize SSM with Lepton-fine-tuned frontend."""
        super().__init__(slm=SLM(), adapter=adapter, backends=backends, name=name)


class RAGSSM(BaseRAGSSM):
    """RAG SSM with Lepton-fine-tuned frontend."""

    def __init__(self,
                 rag_backend: AbstractRAGBackend = None,
                 name: str = None,
                 storage_dir: str = None):
        """Initialize RAG SSM with Lepton-fine-tuned frontend."""
        if rag_backend is None:
            rag_backend = LlamaIndexBackend()

        super().__init__(slm=SLM(), rag_backend=rag_backend, name=name, storage_dir=storage_dir)
