#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:43:45 2021

@author: kuehbach
"""

import os, sys
import yaml
from lxml import etree

def read_user_appdef(fnm):
    with open(fnm) as stream:
        try:
            return yaml.safe_load(stream)
            #print(yml)
            #rt = etree.Element('description')
        except yaml.YAMLError as exc:
            print(exc)
    return None