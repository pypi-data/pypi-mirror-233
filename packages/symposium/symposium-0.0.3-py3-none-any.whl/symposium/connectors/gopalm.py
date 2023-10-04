# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from typing import List, Dict
import requests


palm_key                = environ.get("PALM_KEY", "")
palm_api_base           = "https://generativelanguage.googleapis.com/v1beta3"
palm_completion_model   = environ.get("PALM_DEFAULT_TEXT_MODEL", "models/text-bison-001")
palm_chat_model         = environ.get("PALM_DEFAULT_CHAT_MODEL", "models/chat-bison-001")
palm_embedding_model    = environ.get("PALM_DEFAULT_EMBEDDING_MODEL", "models/embedding-gecko-001")


def palm_answer(context: str,
                examples,
                messages,
                model=palm_chat_model,
                **kwargs):

    """A simple requests call to Palm message generation endpoint.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
    """
    responses = []
    json_data = {
        "prompt": {
            "context": context,
            "examples": examples,
            "messages": messages
        },
        "temperature": kwargs.get("temperature", 0.5),
        "candidateCount": kwargs.get("n", 1),
        "topP": kwargs.get("top_p", 0.1),
        "topK": kwargs.get("top_k", None)
        }
    try:
        response = requests.post(
            url=f"{palm_api_base}/{model}:generateMessage",
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            for count, candidate in enumerate(response.json()['candidates']):
                item = {"index": count,
                        "author": candidate['author'],
                        "content": candidate['content']}
                responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
            print(response.json()['content'])
        return responses

    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return responses


def palm_continuations(text_before,
                       model=palm_completion_model,
                       **kwargs) -> List:

    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 to 8 # number of candidates
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    garbage = [{"category": "HARM_CATEGORY_UNSPECIFIED",    "threshold": "BLOCK_NONE"},  # 0-th category
               {"category": "HARM_CATEGORY_DEROGATORY",     "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_TOXICITY",       "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_VIOLENCE",       "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_SEXUAL",         "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_MEDICAL",        "threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_DANGEROUS",      "threshold": "BLOCK_NONE"},
    ]

    responses = []
    json_data = {"prompt": {"text": text_before},
                 "temperature":     kwargs.get("temperature", 0.5),
                 "candidateCount":  kwargs.get("n", 1),
                 "safetySettings":  garbage,
                 "maxOutputTokens": kwargs.get("max_tokens", 100),
                 "topP":            kwargs.get("top_p", 0.1),
                 "topK":            kwargs.get("top_k", None)}
    try:
        response = requests.post(
            f"{palm_api_base}/{model}:generateText",
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                for count, candidate in enumerate(response.json()['candidates']):
                    item = {"index": count,
                            "text": candidate['output'],
                            "finish_reason": 'stop'}
                    responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return responses


def palm_embeddings(input_list: List[str],
                    model=palm_embedding_model, **kwargs) -> List[Dict]:
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {"texts": input_list} | kwargs
    try:
        response = requests.post(
            f"{palm_api_base}/{model}:batchEmbedText",
            params=f"key={palm_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            # embeddings_list = response.json()['embeddings']
            for count, candidate in enumerate(response.json()['embeddings']):
                item = {"index": count, "embedding": candidate['value']}
                embeddings_list.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return embeddings_list
    except Exception as e:
        print("Unable to generate Embeddings response")
        print(f"Exception: {e}")
        return embeddings_list


if __name__ == '__main__':
    # context = "This conversation will be happening between Albert and Niels"
    # examples = [
    #         {
    #             "input": {"author": "Albert", "content": "We didn't talk about the quantum mechanics lately..."},
    #             "output": {"author": "Niels", "content": "Yes indeed."}
    #         }
    #     ]
    # messages = [
    #         {
    #             "author": "Albert",
    #             "content": "Can we change human nature?"
    #         }, {
    #             "author": "Niels",
    #             "content": "Not clear..."
    #         }, {
    #             "author": "Albert",
    #             "content": "Seriously, can we?"
    #         }
    #     ]
    kwa = {
        "n": 1,
        "top_k": 100
    }
    # a = palm_answer(context, examples, messages, **kwa)
    # e = palm_embeddings(["Can you distinguish an idiot from a human?",
    #                     "Can you distinguish an stupid from a human?"]
    #                    )
    #
    a = palm_continuations(text_before="Can human nature be changed?", **kwa)
    print('ok')

