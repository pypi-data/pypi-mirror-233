# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from .chatgpt import (gpt_answer,
                      gpt_fill_in,
                      gpt_continuations,
                      gpt_embeddings)
from .gopalm import (palm_answer,
                     palm_continuations,
                     palm_embeddings)


__all__ = [
    "gpt_answer",
    "gpt_fill_in",
    "gpt_continuations",
    "gpt_embeddings",
    "palm_answer",
    "palm_continuations",
    "palm_embeddings"
]
