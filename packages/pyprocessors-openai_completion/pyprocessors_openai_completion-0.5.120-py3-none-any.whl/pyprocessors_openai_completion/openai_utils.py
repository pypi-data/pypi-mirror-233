import os
from logging import Logger
from urllib.parse import urlparse

import openai
import requests
from black import Enum

from .retry_limit import api_retry

logger = Logger("pymultirole")


@api_retry(max_call_number=3500, max_call_number_interval=60)
def openai_chat_completion(prefix, **kwargs):
    set_openai(prefix)
    response = openai.ChatCompletion.create(**kwargs)
    return response


def openai_list_models(prefix, **kwargs):
    def sort_by_created(x):
        if 'created' in x:
            return x['created']
        elif 'created_at' in x:
            return x['created_at']
        else:
            return x.id

    models = []
    set_openai(prefix)
    if prefix.startswith("DEEPINFRA"):
        deepinfra_url = urlparse(openai.api_base)
        deploy_list_url = f"{deepinfra_url.scheme}://{deepinfra_url.hostname}/deploy/list/"
        response = requests.get(deploy_list_url,
                                headers={'Accept': "application/json", 'Authorization': f"Bearer {openai.api_key}"})
        if response.ok:
            deploys = response.json()
            models = sorted(deploys, key=sort_by_created, reverse=True)
            models = list({m['model_name'] for m in models if m['task'] == 'text-generation'})
    else:
        response = openai.Model.list(**kwargs)
        if 'data' in response:
            models = sorted(response['data'], key=sort_by_created, reverse=True)
            models = [m.id for m in models]
    return models


def set_openai(prefix):
    openai.api_key = os.getenv(prefix + "OPENAI_API_KEY")
    OPENAI_API_TYPE = os.getenv(prefix + "OPENAI_API_TYPE", None)
    if OPENAI_API_TYPE is not None:
        openai.api_type = OPENAI_API_TYPE
    else:
        openai.api_type = "open_ai"
    OPENAI_API_BASE = os.getenv(prefix + "OPENAI_API_BASE", None)
    if OPENAI_API_BASE is not None:
        openai.api_base = OPENAI_API_BASE
    elif prefix == "":
        openai.api_base = "https://api.openai.com/v1"
    OPENAI_API_VERSION = os.getenv(prefix + "OPENAI_API_VERSION", None)
    if OPENAI_API_VERSION is not None:
        openai.api_version = OPENAI_API_VERSION
    elif prefix == "":
        openai.api_version = None


def gpt_filter(m: str):
    return m.startswith('gpt') and not m.startswith('gpt-3.5-turbo-instruct')


def create_openai_model_enum(name, prefix="", key=lambda m: m):
    chat_gpt_models = []
    default_chat_gpt_model = None
    try:
        chat_gpt_models = [m for m in openai_list_models(prefix) if key(m)]
        if chat_gpt_models:
            default_chat_gpt_model = "gpt-3.5-turbo" if "gpt-3.5-turbo" in chat_gpt_models else \
                chat_gpt_models[0]
    except BaseException:
        logger.warning(f"Can't list models from endpoint {openai.api_base}", exc_info=True)

    model_enum = Enum(name,
                      dict([("".join([c if c.isalnum() else "_" for c in m]), m) for m in chat_gpt_models]))
    default_chat_gpt_model = model_enum(default_chat_gpt_model) if default_chat_gpt_model is not None else None
    return model_enum, default_chat_gpt_model
