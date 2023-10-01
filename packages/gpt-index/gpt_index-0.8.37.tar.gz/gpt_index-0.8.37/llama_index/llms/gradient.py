from typing import Any, Optional

from typing_extensions import override

from llama_index.bridge.pydantic import Field, PrivateAttr
from llama_index.callbacks import CallbackManager
from llama_index.llms import (
    CompletionResponse,
    CompletionResponseGen,
    CustomLLM,
    LLMMetadata,
)
from llama_index.llms.base import llm_completion_callback


class _BaseGradientLLM(CustomLLM):
    _gradient = PrivateAttr()
    _model = PrivateAttr()

    # Config
    max_tokens: Optional[int] = Field(
        description="The number of tokens to generate.",
        gt=0,
        lt=512,
    )

    # Gradient client config
    access_token: Optional[str] = Field(
        description="The Gradient access token to use.",
    )
    host: Optional[str] = Field(
        description="The url of the Gradient service to access."
    )
    workspace_id: Optional[str] = Field(
        description="The Gradient workspace id to use.",
    )

    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        host: Optional[str] = None,
        max_tokens: Optional[int] = None,
        workspace_id: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            max_tokens=max_tokens,
            access_token=access_token,
            host=host,
            workspace_id=workspace_id,
            callback_manager=callback_manager,
            **kwargs,
        )
        try:
            from gradientai import Gradient

            self._gradient = Gradient(
                access_token=access_token, host=host, workspace_id=workspace_id
            )
        except ImportError as e:
            raise ImportError(
                "Could not import Gradient Python package. "
                "Please install it with `pip install gradientai`."
            ) from e

    def close(self) -> None:
        self._gradient.close()

    @llm_completion_callback()
    @override
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        return CompletionResponse(
            text=self._model.complete(
                query=prompt,
                max_generated_token_count=self.max_tokens,
                **kwargs,
            ).generated_output
        )

    @override
    def stream_complete(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> CompletionResponseGen:
        raise NotImplementedError()

    @property
    @override
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=1024,
            num_output=self.max_tokens or 20,
            is_chat_model=False,
            is_function_calling_model=False,
            model_name=self._model.id,
        )


class GradientBaseModelLLM(_BaseGradientLLM):
    base_model_slug: str = Field(
        description="The slug of the base model to use.",
    )

    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        base_model_slug: str,
        host: Optional[str] = None,
        max_tokens: Optional[int] = None,
        workspace_id: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        super().__init__(
            access_token=access_token,
            base_model_slug=base_model_slug,
            host=host,
            max_tokens=max_tokens,
            workspace_id=workspace_id,
            callback_manager=callback_manager,
        )

        self._model = self._gradient.get_base_model(
            base_model_slug=base_model_slug,
        )


class GradientModelAdapterLLM(_BaseGradientLLM):
    model_adapter_id: str = Field(
        description="The id of the model adapter to use.",
    )

    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        host: Optional[str] = None,
        max_tokens: Optional[int] = None,
        model_adapter_id: str,
        workspace_id: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
    ) -> None:
        super().__init__(
            access_token=access_token,
            host=host,
            max_tokens=max_tokens,
            model_adapter_id=model_adapter_id,
            workspace_id=workspace_id,
            callback_manager=callback_manager,
        )
        self._model = self._gradient.get_model_adapter(
            model_adapter_id=model_adapter_id
        )
