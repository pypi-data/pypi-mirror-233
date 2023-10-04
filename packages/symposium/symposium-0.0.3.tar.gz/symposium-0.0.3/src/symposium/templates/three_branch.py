# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from typing import Union, Optional
from dataclasses import dataclass
from symposium.templates.sentence import Soliloquium, Colloquium, Utterance


three_branch_template = """
<table width="100%">
    <tr>
        <th style="text-align: right; width:25%">Branch 1</th>
        <th colspan="2" style="text-align: center; width: 50%">Branch 2</th>
        <th style="text-align: left; width:25%">Branch 3</th>
    </tr>
    <tr>
        <td colspan="4" style="width: 100%"> </td>
    </tr>
    <tr>
        <td colspan="2" style="width: 50%;">{branch1}</td>
        <td style="width: 25%"> </td>
        <td style="width: 25%"> </td>
    </tr>
    <tr>
        <td colspan="4" style="width: 100%"> </td>
    </tr>
    <tr>
        <td colspan="1" width="25%"></td>
        <td  colspan="2" style="width: 50%;">{branch2}</td>
        <td width="25%"></td>
    </tr>
    <tr>
        <td colspan="4" style="width: 100%"> </td>
    </tr>
    <tr>
        <td width="25%"></td>
        <td width="25%"></td>
        <td colspan="2" style="width: 50%;">{branch3}</td>
    </tr>
    <tr>
        <td colspan="4" style="background-color: lightgrey; width: 100%"> </td>
    </tr>
</table>"""


@dataclass
class ThreeBranch:
    """ A three branch template
        kwargs:
            topic:      str
            sentence:   str
            first:      Union[Soliloquium, Colloquium, Utterance]
            second:     Union[Soliloquium, Colloquium, Utterance]
    """
    topic:      str
    sentence:   str
    first:      Union[Soliloquium, Colloquium]
    second:     Union[Soliloquium, Colloquium]
    third:      Union[Soliloquium, Colloquium]

    def __call__(self):
        self._markdown = f"###{self.topic}\n**Facilitator:** {self.sentence}"
        self._markdown += three_branch_template.format(branch1=self.first.html,
                                                 branch2=self.second.html,
                                                 branch3=self.third.html, )
        return self._markdown


if __name__ == '__main__':

    bra1 = {
        "topic": "Human Nature",
        "Answer": "Yes it can be changed",
    }
    bran1 = Soliloquium(bra1)
    bra2 = {
        "topic": "Human Nature",
        "Answer": "No it cannot be changed",
    }
    bran2 = Soliloquium(bra2)
    bra3 = {
        "topic": "Human Nature",
        "Answer": "Maybe it can be changed",
    }
    bran3 = Soliloquium(bra3)
    human_nature = ThreeBranch(
        topic='Human Nature',
        sentence='Can human nature be changed?',
        first   =bran1,
        second  =bran2,
        third   =bran3
    )
    markdown = human_nature()
    print('ok')