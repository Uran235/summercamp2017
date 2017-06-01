#!/usr/bin/env 
#-*- coding: utf-8 -*-

import pandas as pd
import numpy as np 
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
from itertools import product


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('datascience.log','w','utf-8')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

files = {'pokemon': 'data/pokemon.csv', 'abilities':'data/abilities.csv'}

def main():
    logger.info('==START==')
    with open(files['pokemon'],'r') as f:
        logger.debug('Read file {0}'.format(files['pokemon']))
        pk = pd.read_csv(files['pokemon'])
    with open(files['abilities'],'r') as f:
        logger.debug('Read file {0}'.format(files['abilities']))
        ab = pd.read_csv(files['abilities'])
    logger.debug('Merge pokemon data with abilities info')
    merged_data = pd.merge(pk, ab, left_on = 'ability1_id', right_on='id')
    corr_threshold = 0.80
    
    # группы будем делать по атрибутам из group_col
    group_col = ['type1_id','ability1_id', 'color_id', 'species', 'abilitydream_id', 'gender_rate', 'base_happiness','hatch_counter','catch_rate','exp_yield']

    # а эти столбцы из drop_col будем выбрасывать
    drop_col = ['ndex','kdex','jdex','udex','sdex','hdex','legacy_id','generation_id_y','generation_id_x','evolution_parent_pokemon_id','evolution_method_id', 'jdex_old', 'id_x','pokemon_order','id_y','ability1_id','egg_group1_id','egg_group2_id','abilitydream_id','baby_breed_item_id', 'type1_id', 'type2_id', 'color_id', 'ability2_id']
    
    logger.debug('Columns to be grouped by: {0}'.format(group_col))
    for col in group_col:
        '''Найдем корреляцию среди атрибутов по всем группам
        '''
        logger.debug('{1}Group by {0}{1}'.format(col,5*'='))
        md = merged_data.groupby(col).agg(['count','mean','sum','max','min','std','median'])
        logger.debug('Norm data')
        for c in md:
            md[c[0]] = md[c[0]]/md[c[0]].sum(axis=0)
        logger.debug('Drop uninteresting cols (all kind of id)')
        dc = []
        for name in drop_col:
            if name != col: dc.append(name)
        dmd = md.drop(dc , axis=1)
        allkeys = set([x[0] for x in dmd.keys()])
        logger.debug('Looking for correlated items')
        for key in product(allkeys,allkeys):
            corr = md[key[0]]['mean'].corr(md[key[1]]['mean'])
            if abs(corr)>=corr_threshold and key[0]!=key[1]:
                logger.debug('{3}: {0} to {1} = {2}'.format(key[0],key[1],corr,col))

    '''Для примера график зависимости средних catch_rate и hatch_counter по type1_id
    '''
    md = merged_data.groupby('type1_id').agg(['count','mean','sum','max','min','std','median'])
    logger.debug('Norm data')
    for c in md:
        md[c[0]] = md[c[0]]/md[c[0]].sum(axis=0)
    md['catch_rate']['mean'].plot(kind='line', label='catch_rate mean', color='g', alpha=0.6)
    md['hatch_counter']['mean'].plot(kind='line', label='hatch_counter mean', logy=False, color='r', alpha=0.4)
 
    plt.axis('tight')
    plt.legend()
    plt.show()
    logger.info('==FINISH==')
if __name__ == '__main__':
    main()