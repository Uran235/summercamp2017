#!/usr/bin/env 
#-*- coding: utf-8 -*-

from itertools import product
from matplotlib import pyplot as plt

start_position = 2
prob_frw = 1/3

def calc_prob(steps, frw):
    '''
    Функция вычисляет вероятность для определенного варианта развития событий
    :param: steps - количество шагов
    :param: frw - вероятность шагнуть вперед
    '''
    res = 1
    for step in steps:
        if step == -1:
            res *= frw
        elif step == 1:
            res *= 1-frw    
    return res

def walk(n):
    prob = 0
    # Сгенерируем все возможные исходы
    variations = product([1,-1], repeat=n)
    # Отфильтруем только нужные (где мы падаем)
    good_vars = filter(lambda x: sum(x)<=-start_position, variations)
    for a in good_vars:
        prob += calc_prob(a, prob_frw)
    return 1-prob

def show_graph():
    x = []
    y = []
    for i, n in enumerate(range(0,20)):
        x.append(i)
        y.append(walk(n))
    plt.plot(x,y,'.r-')
    plt.scatter(x,y)
    plt.show()

def main():
    show_graph()

if __name__ == '__main__':
    main()