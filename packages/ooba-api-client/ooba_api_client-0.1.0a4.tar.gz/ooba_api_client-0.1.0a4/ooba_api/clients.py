import json
import logging
from multiprocessing import Lock

import requests

from ooba_api.model_info import OobaModelInfo, OobaModelNotLoaded
from ooba_api.parameters import DEFAULT_PARAMETERS, Parameters
from ooba_api.prompts import Prompt

logger = logging.getLogger("ooba_api")
prompt_logger = logging.getLogger("ooba_api.prompt")

# global lock
_one_at_a_time_lock = Lock()


class OobaApiClient:
    """
    Client for the Ooba Booga text generation web UI
    """

    # full URL to chat endpoint
    _chat_url: str

    # full URL to generate endpoint
    _generate_url: str

    # full URL to model endpoint
    _model_url: str

    # API Key, not yet used
    api_key: str | None

    # Enforce one request at a time to avoid overwhelming the server
    one_at_a_time: bool

    def __init__(
        self,
        url: str | None = None,
        *,
        host: str = "http://localhost",
        port: int = 5000,
        api_key: str | None = None,
        one_at_a_time: bool = True,
    ):
        if url:
            self.url = url
        else:
            self.url = f"{host}:{port}"
        self._chat_url = f"{self.url}/api/v1/chat"
        self._generate_url = f"{self.url}/api/v1/generate"
        self._model_url = f"{self.url}/api/v1/model"
        self.api_key = api_key
        self.one_at_a_time = one_at_a_time

        if self.api_key:
            logger.warning("API keys are not yet supported")

    def _post(self, target_url: str, timeout: float, data: dict) -> requests.Response:
        with _one_at_a_time_lock:
            return requests.post(target_url, timeout=timeout, json=data)

    def instruct(
        self,
        prompt: Prompt,
        parameters: Parameters = DEFAULT_PARAMETERS,
        timeout: int | float = 500,
        print_prompt: bool = False,
    ) -> str:
        """
        Provide an instruction, get a response

        :param messages: Message to provide an instruction
        :param max_tokens: Maximum tokens to generate
        :param timeout: When to timeout
        :param print_prompt: Print the prompt being used. Use case is debugging
        """
        prompt_to_use = prompt.full_prompt()
        if print_prompt:
            print(prompt_to_use)
        prompt_logger.info(prompt_to_use)

        # pydantic compatibility. dict -> model_dump
        if hasattr(parameters, "model_dump"):
            param_dict = parameters.model_dump()
        else:
            param_dict = parameters.dict()

        response = self._post(
            self._generate_url,
            timeout=timeout,
            data=(
                {"prompt": prompt_to_use, "negative_prompt": prompt.negative_prompt or ""}
                | param_dict
            ),
        )
        response.raise_for_status()
        data = response.json()
        if __debug__:
            logger.debug(json.dumps(data, indent=2))

        return data["results"][0]["text"]

    def _model_api(self, request: dict, timeout: int | float = 500) -> dict:
        response = self._post(self._model_url, timeout, request)
        response.raise_for_status()
        data = response.json()
        if __debug__:
            logger.debug(json.dumps(data, indent=2))

        return data["result"]

    def model_info(self) -> OobaModelInfo:
        result = self._model_api({"action": "info"}, timeout=5)
        model_name = result["model_name"]
        if model_name == "None":
            return OobaModelNotLoaded(
                shared_settings=result["shared.settings"], shared_args=result["shared.args"]
            )
        return OobaModelInfo(
            model_name=result["model_name"],
            lora_names=result["lora_names"],
            shared_settings=result["shared.settings"],
            shared_args=result["shared.args"],
        )

    def load_model(self, model_name: str, *, args_dict: dict) -> OobaModelInfo:
        result = self._model_api({"action": "load", "model_name": model_name, "args": args_dict}, timeout=5000)
        return OobaModelInfo(
            model_name=result["model_name"],
            lora_names=result["lora_names"],
            shared_settings=result["shared.settings"],
            shared_args=result["shared.args"],
        )
