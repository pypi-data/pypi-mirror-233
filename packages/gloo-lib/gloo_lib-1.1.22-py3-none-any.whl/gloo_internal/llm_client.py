import re
import typing
import abc
import openai

from .api import API
from .api_types import (
    LLMEventSchema,
    LLMOutputModel,
    LLMOutputModelMetadata,
    LLMEventInput,
    LLMEventInputPrompt,
)
from .logging import logger
from .tracer import set_llm_metadata, update_trace_tags
from . import api_types


def safe_format(s: str, kwargs: typing.Dict[str, str]) -> str:
    for key, value in kwargs.items():
        s = s.replace("{@" + key + "}", value)
    # Throw error if there are any remaining placeholders of the form {@key}
    if re.search("{@.*?}", s):
        raise ValueError(f"Invalid template: {s}")
    return s


def hide_secret(kwargs: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    copied = kwargs.copy()
    for x in ["api_key", "secret_key", "token"]:
        if x in copied:
            copied[x] = copied[x][:4] + "*" * 4
    return copied


class LLMClient:
    def __init__(self, provider: str, **kwargs: typing.Any) -> None:
        self.__provider = provider
        self.__type = str(kwargs.pop("__type", "chat"))
        self.__kwargs = kwargs

    @property
    def provider(self) -> str:
        return self.__provider

    @property
    def kwargs(self) -> typing.Dict[str, typing.Any]:
        return self.__kwargs

    @property
    def type(self) -> str:
        return self.__type

    @abc.abstractmethod
    def get_model_name(self) -> str:
        raise NotImplementedError

    async def run(self, prompt_template: str, vars: typing.Dict[str, str]) -> str:
        event = LLMEventSchema(
            provider=self.provider,
            model_name=self.get_model_name(),
            input=LLMEventInput(
                prompt=LLMEventInputPrompt(
                    template=prompt_template, template_args=vars
                ),
                invocation_params=hide_secret(self.kwargs),
            ),
            output=None,
        )
        set_llm_metadata(event)
        prompt = safe_format(prompt_template, vars)
        logger.info(f"Running {self.provider} with prompt:\n{prompt}")

        cached = await API.check_cache(
            payload=api_types.CacheRequest(
                prompt=prompt_template,
                prompt_vars=vars,
                invocation_params=event.input.invocation_params,
            )
        )

        if cached:
            model_name = cached.mdl_name
            response = cached.llm_output
            update_trace_tags(__cached="1", __cached_latency_ms=str(cached.latency_ms))
        else:
            model_name, response = await self._run(prompt)
        logger.info(f"RESPONSE:\n{response.raw_text}")
        # Update event with output
        event.output = response
        event.mdl_name = model_name
        return response.raw_text

    @abc.abstractmethod
    async def _run(self, prompt: str) -> typing.Tuple[str, LLMOutputModel]:
        raise NotImplementedError("Client must implement _run method")


class OpenAILLMClient(LLMClient):
    def __init__(self, provider: str, **kwargs: typing.Any) -> None:
        super().__init__(provider=provider, **kwargs)

    def get_model_name(self) -> str:
        # Try some well known keys
        for key in ["model_name", "model", "engine"]:
            if key in self.kwargs:
                val = self.kwargs[key]
                if isinstance(val, str):
                    return val.lower()
        return "unknown"

    def is_chat(self) -> bool:
        return self.type == "chat"

    async def _run(self, prompt: str) -> typing.Tuple[str, LLMOutputModel]:
        # Guess is its a chatcompletions
        if self.is_chat():
            response = await openai.ChatCompletion.acreate(messages=[{"role": "user", "content": prompt}], **self.kwargs)  # type: ignore
            text = response["choices"][0]["message"]["content"]
            usage = response["usage"]
            model = response["model"]
            return model, LLMOutputModel(
                raw_text=text,
                metadata=LLMOutputModelMetadata(
                    logprobs=None,
                    prompt_tokens=usage.get("prompt_tokens", None),
                    output_tokens=usage.get("completion_tokens", None),
                    total_tokens=usage.get("total_tokens", None),
                ),
            )
        else:
            response = await openai.Completion.acreate(prompt=prompt, **self.kwargs)  # type: ignore
            text = response["choices"][0]["text"]
            usage = response["usage"]
            model = response["model"]
            return model, LLMOutputModel(
                raw_text=text,
                metadata=LLMOutputModelMetadata(
                    logprobs=response["choices"][0]["logprobs"],
                    prompt_tokens=usage.get("prompt_tokens", None),
                    output_tokens=usage.get("completion_tokens", None),
                    total_tokens=usage.get("total_tokens", None),
                ),
            )
