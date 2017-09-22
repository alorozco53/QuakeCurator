#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

def parse_extendeddata(extdata):
    """
    Parses a BeautifulSoup object with the structure:
        <ExtendedData>
          <Data name="k1">
            <value>v1</value>
          </Data>
          <Data name="k2">
            <value>v2</value>
            .
            .
            .
        </ExtendedData>
    and returns a dict containing all the found info.
    """
    data = extdata.find_all('data')
    data = [(d['name'], d.value.text) for d in data]
    return dict(data)
