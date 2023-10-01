"""LLM predictor tests."""
from typing import Any
from unittest.mock import patch

from llama_index.llm_predictor.structured import LLMPredictor, StructuredLLMPredictor
from llama_index.prompts import BasePromptTemplate
from llama_index.prompts.base import PromptTemplate
from llama_index.types import BaseOutputParser

try:
    gptcache_installed = True
except ImportError:
    gptcache_installed = False


class MockOutputParser(BaseOutputParser):
    """Mock output parser."""

    def parse(self, output: str) -> str:
        """Parse output."""
        return output + "\n" + output

    def format(self, output: str) -> str:
        """Format output."""
        return output


def mock_llmpredictor_predict(prompt: BasePromptTemplate, **prompt_args: Any) -> str:
    """Mock LLMPredictor predict."""
    return prompt_args["query_str"]


@patch.object(LLMPredictor, "predict", side_effect=mock_llmpredictor_predict)
@patch.object(LLMPredictor, "__init__", return_value=None)
def test_struct_llm_predictor(mock_init: Any, mock_predict: Any) -> None:
    """Test LLM predictor."""
    llm_predictor = StructuredLLMPredictor()
    output_parser = MockOutputParser()
    prompt = PromptTemplate("{query_str}", output_parser=output_parser)
    llm_prediction = llm_predictor.predict(prompt, query_str="hello world")
    assert llm_prediction == "hello world\nhello world"

    # no change
    prompt = PromptTemplate("{query_str}")
    llm_prediction = llm_predictor.predict(prompt, query_str="hello world")
    assert llm_prediction == "hello world"


# TODO: bring back gptcache tests
# @pytest.mark.skipif(not gptcache_installed, reason="gptcache not installed")
# def test_struct_llm_predictor_with_cache() -> None:
#     """Test LLM predictor."""
#     from gptcache.processor.pre import get_prompt
#     from gptcache.manager.factory import get_data_manager
#     from llama_index.bridge.langchain import GPTCache

#     def init_gptcache_map(cache_obj: Cache) -> None:
#         cache_path = "test"
#         if os.path.isfile(cache_path):
#             os.remove(cache_path)
#         cache_obj.init(
#             pre_embedding_func=get_prompt,
#             data_manager=get_data_manager(data_path=cache_path),
#         )

#     responses = ["helloworld", "helloworld2"]

#     llm = FakeListLLM(responses=responses)
#     predictor = LLMPredictor(llm, False, GPTCache(init_gptcache_map))

#     prompt = DEFAULT_SIMPLE_INPUT_PROMPT
#     llm_prediction = predictor.predict(prompt, query_str="hello world")
#     assert llm_prediction == "helloworld"

#     # due to cached result, faked llm is called only once
#     llm_prediction = predictor.predict(prompt, query_str="hello world")
#     assert llm_prediction == "helloworld"

#     # no cache, return sequence
#     llm.cache = False
#     llm_prediction = predictor.predict(prompt, query_str="hello world")
#     assert llm_prediction == "helloworld2"
