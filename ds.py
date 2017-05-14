#!/usr/bin/env 
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np 
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('datascience.log','w','utf-8')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

files = {'pokemon': 'data/pokemon.csv'}

def main():
    logger.debug('==START==')
    with open(files['pokemon'],'r') as f:
        logger.debug('Read {0}'.format(files['pokemon']))
        pk = pd.read_csv('data/pokemon.csv')
        print(pk.count)
        print(pk.name)
        for name in pk.name:
            logger.debug(name)

if __name__ == '__main__':
    main()