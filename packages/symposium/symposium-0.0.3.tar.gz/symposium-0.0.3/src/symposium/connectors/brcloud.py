# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import List, Dict
import boto3
import json
import re
from os import environ


claud_completion_model   = environ.get("CLAUD_DEFAULT_TEXT_MODEL", "anthropic.claude-v1")


def extract_between_tags(tag: str, string: str, strip: bool = True, alt=True) -> list[str]:
    # Helper function for parsing Claude's output
    try:
        ext_list = re.findall(f"<{tag}\s?>(.+?){tag}\s?>", string, re.DOTALL)
        if strip:
            ext_list = [e.strip() for e in ext_list]
        if alt and not ext_list:
            ext_list = re.findall(f"<{tag}\s?>(.+?)<{tag}\s?>", string, re.DOTALL)
            if strip:
                ext_list = [e.strip() for e in ext_list]
        return ext_list
    except:
        return extract_between_tags(tag, string+'' + tag + '>', strip, alt)


def extract_tags(text: str, tags: List[str], strip: bool = True, alt=True) -> Dict[str, List[str]]:
    """ Extract all the texts between tags and return them as a dictionary
    """
    output = {}
    for tag in tags:
        try:
            ext_list = re.findall(f"<{tag}\s?>(.+?){tag}\s?>", text, re.DOTALL)
            if strip:
                ext_list = [e.strip() for e in ext_list]
            if alt and not ext_list:
                ext_list = re.findall(f"<{tag}\s?>(.+?)<{tag}\s?>", text, re.DOTALL)
                if strip:
                    ext_list = [e.strip() for e in ext_list]
            output[tag] = ext_list
        except Exception:
            completed_text = text+'' + tag + '>'  # it probably doesn't close tags sometimes.
            output[tag] = extract_between_tags(tag, completed_text, strip, alt)

    return output


def cloud_continuations(text_before,
                        model=claud_completion_model,
                        **kwargs) -> List:
    """A completions endpoint call through boto3.
        kwargs:
            max_tokens_to_sample    <= 4096
            temperature             = 0 to 1.0
            top_p                   = 0.0 to 1.0
            top_k                   = 1 to ...
    """
    bedrock = boto3.client(service_name='bedrock-runtime')

    json_data = {"prompt": text_before} | kwargs

    try:
        response = bedrock.invoke_model(body=json.dumps(json_data),
                                        modelId=model,
                                        accept='application/json',
                                        contentType='application/json')

        response_body = json.loads(response.get('body').read())

        return [{"index": 0,
                 "text": response_body['completion'],
                 "finish_reason": response_body['stop_reason']}]

    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return [{"index": 0,"text": ''}]


if __name__ == "__main__":
    completion_model = 'anthropic.claude-v1'
    kwa = {
        "max_tokens_to_sample": 100,
        "temperature": 0.9999,
        "top_p": 0.9999,
        "top_k": 50,
        # "stop_sequences":["\n\nHuman:"]
    }
    text = "\n\nHuman:Can we change human nature\n\nAssistant:"
    a = cloud_continuations(text_before=text, model=completion_model, **kwa)
    print('ok')