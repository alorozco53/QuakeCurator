#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

from geopy.distance import great_circle

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

def children(tree, name=False):
    """
    Returns a list of the immediate children below the given
    tree's root.
    If name == True, then it returns a list that contains only
    the children's names
    """
    child = tree.findNext()
    children = [child] + list(child.findNextSiblings())
    if name:
        return [c.name for c in children]
    else:
        return children

def get_location(tree):
    """
    Returns a dict of the form
    {
      'lat': <latitude>,
      'lon': <longitude>
    }
    given a location encoded in a bs4 object.
    """
    # check if 'point' is a children of the root
    if tree.point:
        try:
            lon, lat = tree.point.coordinates.text.strip().split(',')[:-1]
            return {
                'lat': lat,
                'lon': lon}
        except:
            pass

    # check if there is an extended data frame
    if tree.extendeddata:
        data_frame = tree.find('extendeddata')
        indices = [('lat', 'lon'),
                   ('latitud', 'longitud'),
                   ('latitude', 'longitude')]
        for ilat, ilon in indices:
            try:
                lat, lon = data_frame[ilat], data_frame[ilon]
                return {
                    'lat': lat,
                    'lon': lon}
            except:
                continue

    # try another option
    placemarks = tree.find_all('placemark')
    for p in placemarks:
        if p:
            try:
                lon, lat = tree.address.text.strip().split()
                return {
                    'lat': lat,
                    'lon': lon}
            except:
                continue

    return None

def distance(loc1, loc2):
    """
    Computes the distance (in km) between the given locations.
    """
    l1 = (loc1['lat'], loc1['lon'])
    l2 = (loc2['lat'], loc2['lon'])
    return great_circle(l1, l2).kilometers
