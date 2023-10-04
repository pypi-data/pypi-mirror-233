# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from dataclasses import dataclass


@dataclass
class Soliloquium:
    """ A one entity text/speach template including the speech to itself.
    """
    topic: str
    text: str
    html: str

    def __init__(self, kwargs):
        if kwargs.get('html', None):
            self.html = kwargs['html']
        else:
            if kwargs.get('Answer', None):
                self.answer = kwargs['Answer']
                self.text = f"Answer: {self.answer} "
                self.html = f"<b>Answer:</b> {self.answer}<br>"
            if kwargs.get('Call to', None):
                self.call_to = kwargs['Call to']
                self.text += f"Call to: {self.call_to} "
                self.html += f"<b>Call to:</b> {self.call_to}<br>"
            if kwargs.get('Question', None):
                self.question = kwargs['Question']
                self.text += f"Question: {self.question} "
                self.html += f"<b><i>Question:</i></b> {self.question}<br>"
            if kwargs.get('Reason', None):
                self.reason = kwargs['Reason']
                self.text += f"Reason: {self.reason} "
                self.html += f"<b>Reason:</b> {self.reason}<br>"

    def __call__(self):
        return self.html


@dataclass
class Colloquium:
    """ A one entity text/speach directed at another entity.
    """
    topic: str
    text: str
    html: str

    def __init__(self, kwargs):
        if kwargs.get('html', None):
            self.html = kwargs['html']
        else:
            if kwargs.get('Answer', None):
                self.answer = kwargs['Answer']
                self.text = f"Answer: {self.answer} "
                self.html = f"<b>Answer:</b> {self.answer}<br>"
            if kwargs.get('Call to', None):
                self.call_to = kwargs['Call to']
                self.text += f"Call to: {self.call_to} "
                self.html += f"<b>Call to:</b> {self.call_to}<br>"
            if kwargs.get('Question', None):
                self.question = kwargs['Question']
                self.text += f"Question: {self.question} "
                self.html += f"<b><i>Question:</i></b> {self.question}<br>"
            if kwargs.get('Reason', None):
                self.reason = kwargs['Reason']
                self.text += f"Reason: {self.reason} "
                self.html += f"<b>Reason:</b> {self.reason}<br>"

    def __call__(self):
        return self.html


@dataclass
class Utterance:
    """ A one entity text/speach directed at another entity.
    """
    topic: str
    text: str
    html: str

    def __init__(self, kwargs):
        if kwargs.get('html', None):
            self.html = kwargs['html']
        else:
            if kwargs.get('Answer', None):
                self.answer = kwargs['Answer']
                self.text = f"Answer: {self.answer} "
                self.html = f"<b>Answer:</b> {self.answer}<br>"
            if kwargs.get('Call to', None):
                self.call_to = kwargs['Call to']
                self.text += f"Call to: {self.call_to} "
                self.html += f"<b>Call to:</b> {self.call_to}<br>"
            if kwargs.get('Question', None):
                self.question = kwargs['Question']
                self.text += f"Question: {self.question} "
                self.html += f"<b><i>Question:</i></b> {self.question}<br>"
            if kwargs.get('Reason', None):
                self.reason = kwargs['Reason']
                self.text += f"Reason: {self.reason} "
                self.html += f"<b>Reason:</b> {self.reason}<br>"

    def __call__(self):
        return self.html
