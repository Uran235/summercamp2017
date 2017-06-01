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
        cols = ['name', 'ability1_id','id', 'type1_id', 'exp_yield','catch_rate', 'hatch_counter', \
        'name_jp', 'base_happiness','height','weight']
        scattercols = ['type1_id','ability1_id','exp_yield','catch_rate', 'base_happiness', 'hatch_counter','height','weight']
        logger.debug('Read file {0}'.format(files['pokemon']))
        pk = pd.read_csv(files['pokemon'])
    with open(files['abilities'],'r') as f:
        logger.debug('Read file {0}'.format(files['abilities']))
        ab = pd.read_csv(files['abilities'])
    logger.debug('Merge pokemon data with abilities info')
    merged_data = pd.merge(pk, ab, left_on = 'ability1_id', right_on='id')
    # merged_data.to_excel('task.xls')
    # merged_data.drop(['color_id','ability1_id','generation_id','exp_yield','catch_rate', 'id', 'hatch_counter'], axis=1, inplace=True)
    # logger.debug('Catch_rate/Happiness corr: {0}'.format(merged_data.catch_rate.corr(merged_data.base_happiness)))
    corr_threshold = 0.80
    group_col = ['type1_id','ability1_id', 'color_id', 'species', 'abilitydream_id', 'gender_rate', 'base_happiness','hatch_counter','catch_rate','exp_yield']
    drop_col = ['ndex','kdex','jdex','udex','sdex','hdex','legacy_id','generation_id_y','generation_id_x','evolution_parent_pokemon_id','evolution_method_id', 'jdex_old', 'id_x','pokemon_order','id_y','ability1_id','egg_group1_id','egg_group2_id','abilitydream_id','baby_breed_item_id', 'type1_id', 'type2_id', 'color_id', 'ability2_id']
    logger.debug('Columns to be grouped by: {0}'.format(group_col))
    for col in group_col:
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
    # ============ 
    md = merged_data.groupby('type1_id').agg(['count','mean','sum','max','min','std','median'])
    logger.debug('Norm data')
    for c in md:
        md[c[0]] = md[c[0]]/md[c[0]].sum(axis=0)
    md['catch_rate']['mean'].plot(kind='line', label='catch_rate mean', color='g', alpha=0.6)
    md['hatch_counter']['mean'].plot(kind='line', label='hatch_counter mean', logy=False, color='r', alpha=0.4)
    # md['exp_yield']['median'].plot(kind='line', label='hatch_counter median')
    
    # for key in md.keys():
    #     for key2 in md.keys():
    #         corr = md[key[0]]['mean'].corr(md[key2[0]]['mean'])
    #         if corr>=0.88 and key[0]!=key2[0]:
    #             logger.debug('{0} to {1} = {2}'.format(key[0],key2[0],corr))

    # plt.scatter(md['catch_rate']['mean'],md['exp_yield']['mean'])
    # md['weight']['mean'].plot(kind='bar', label='weight mean',alpha=0.7, color='r')
    # md['hatch_counter']['count'].plot(kind='line', label='Hatch counter count')
    # print(md['weight'])
    # weight_baby = merged_data[merged_data.is_baby==1].groupby(group_col).agg(['count','min','max','mean','median'])
    # weight = merged_data[merged_data.is_baby==0].groupby(group_col).agg(['count','min','max','mean','median'])
    # weight['weight'].plot()
    # weight_baby['weight'].plot()
    # corr = md.corr(method='pearson')
    # md.to_excel('minmax.xls')

    # logger.debug('mean base_happiness/hatch_counter corr: {0}'.format(md['hatch_counter']['mean'].corr(md['base_happiness']['mean'])))
    # md['hatch_counter']['mean'].plot(label='hatch_counter mean')
    # md['base_happiness']['mean'].plot(label='base_happiness')
    
    # logger.debug(md.catch_rate.corr(md.exp_yield))
    #============================================#
    # ptd = pd.pivot_table(merged_data, index = group_col, aggfunc=[np.mean,len])
    # print(ptd.describe())
    #============================================#
    # group_col = ['type1_id']
    # md = merged_data.groupby(group_col).count()
    # md.rename(columns=lambda x:x+'_count',inplace = True)
    # md['name_x_count'].plot(kind='hist')

    # md['exp_yield_count'].plot(kind='line')
    # md2 = merged_data.groupby(group_col).std()
    # md2.rename(columns= lambda x:x+'_std',inplace = True)
    # md2['exp_yield_std'].plot(color='r',kind='line',alpha=0.6)
    # md3 = merged_data.groupby(group_col).mean()
    # md3.rename(columns=lambda x:x+'_mean',inplace = True)
    # md3['catch_rate_mean'].plot(color='g',kind='line',alpha=0.3)
    # md4 = merged_data.groupby(group_col).max()
    # md4.rename(columns=lambda x:x+'_max',inplace = True)
    # md4['exp_yield_max'].plot(color='m')
    # md5 = merged_data.groupby(group_col).min()
    # md5.rename(columns=lambda x:x+'_min',inplace = True)
    # md5['exp_yield_min'].plot(color='y')
    # print(md2.T.keys())
    # print(md.loc[17])
    # print(md2.loc[18])
    # print(md.head(5))
    # pd.scatter_matrix(md,alpha=0.5, figsize=(12, 6), diagonal='kde');
    # plt.hist(md['type1_id'])
    # sns.clustermap(md,method='single',z_score=0)
    # md['catch_rate'].plot()
    # md['base_happiness'].plot()
    # md['hatch_counter'].plot()
    # md['exp_yield'].plot()
    # corr = md.corr(method='pearson')
    # corr = corr[(corr.height>=0.5)]
    # print(corr)
    # corr.to_excel('corr_type_std.xls')
    # corr.plot(kind='barh')
    # corr['exp_yield'].plot()
    # corr['base_happiness'].plot()
    # pd.scatter_matrix(corr, alpha = 0.3, figsize = (14,8))
    # plt.matshow(corr)
    # md['lvl_100_exp'].plot(logy=True)
    # md['gender_rate'].plot()
    plt.axis('tight')
    plt.legend()
    plt.show()
    logger.info('==FINISH==')
if __name__ == '__main__':
    main()