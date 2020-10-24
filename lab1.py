#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:19:53 2020

@author: diego
"""

# -*- coding: utf-8 -*-
import matplotlib.pyplot  as plt
import numpy as np
import math
 
static_wheel = "files/static/"
spinning_wheel = "files/spinning/"



def read_txt(basepath, number):
    file = basepath + f"Part_{number}.txt"
    list_ = []
    with open(file,"r") as f:
        for line in f:
            list_.append(int(line.split(',')[0]))
    return list_

def all_list(type_wheel, max_number ):
    #max_number is the last number that are in the files
    list_ = []
    for number in range(0,max_number+1):
        sublist = read_txt(type_wheel, number)
        list_.append(sublist)
    return list_

#gets the elapsed time between two tags
def get_difference(list_of_tags):
    list_diff = [1]
    tag_before = -1
    for i in list_of_tags:
        diff = i - tag_before
        list_diff.append(diff/400)
        tag_before = i
    return list_diff


def static_spinning_lists():
    load_files_static = all_list(static_wheel, 9 )
    load_files_spinning = all_list(spinning_wheel, 9 )  
    return load_files_static, load_files_spinning


def draw_plot(x_axis, data_sample, plot_title):
    fig, ax = plt.subplots()
    ax.plot(x_axis , data_sample, marker='*')
    ax.set(xlabel='tag', ylabel='time diff', title=plot_title)
    ax.grid()
    fig.savefig(plot_title)   
    

#For quick example, first 80
def plot_sample_lineal(list_static, list_spinning):
    #plot sample static 
    data_sample_static = get_difference(list_static[0][0:80])
    x_axis = range(1,len(data_sample_static)+1)
    title_static = "Difference for static wheel"
    draw_plot(x_axis, data_sample_static, title_static)
    #plot sample spinning 
    data_sample_spinning = get_difference(list_spinning[0][0:80])
    x_axis = range(1,len(data_sample_spinning)+1)
    title_spinning  = "Difference for spinning wheel"
    draw_plot(x_axis, data_sample_spinning, title_spinning)

def plot_hist(list_data, title):
    plt.figure()
    fig, ax = plt.subplots()
    counts, bins, bars = ax.hist(list_data)
    ax.set(xlabel='', ylabel='Number of events', title=title)
    ax.grid()
    plt.draw()
    fig.savefig(title+'.png')
    return counts, bins, bars
def plot_hist2(x,y, title):
    plt.figure()
    fig, ax = plt.subplots()
    ysum = sum(y)
    y_percentage = []
    [y_percentage.append(i/ysum) for i in y]
    ax.bar(x,y_percentage)
    print(sum(y_percentage))
    ax.set(xlabel='', ylabel='Number of events', title=title)
    ax.grid()
    plt.draw()
    fig.savefig(title+'.png')

from matplotlib.ticker import PercentFormatter

def plot_hist_percentage(list_data, title):
    plt.figure()
    fig, ax = plt.subplots()
    counts, bins, bars = ax.hist(list_data, weights=np.ones(len(list_data)) / len(list_data))
    ax.set(xlabel='', ylabel='Percentage of events', title=title)
    ax.grid()
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.draw()
    fig.savefig(title+'.png')
    return counts, bins, bars

def merge_files_per_experiment(list_d):
    newlist = [num for elem in list_d for num in elem]
    t = get_difference(newlist)
    new_np = np.array(t)
    return new_np

def get_average_stdev(static, spinning):
    x = f'mean and standart deviation of standing wheel {static.mean()} --- {static.std()} =={static.var()}'
    y = f'mean and standart deviation of spinning wheel {spinning.mean()} --- {spinning.std()}'
    snr_static = static.mean()**2/static.var()
    snr_spinning = spinning.mean()/spinning.mean()+1
    print(x)
    print(y)
    print(f"SNR of standing source = {snr_static} , SNR of spinning source = {snr_spinning}")

def divide_by_timebin(dataset,interval=800000):
    maxtag = max(dataset)
    left,right = 0, interval
    ranges = []
    data_ranged = []
    histogram_data = []
    for i in range(1,(-(-maxtag // interval))+1):
        left = left*(i-1)
        ranges.append((right*i-interval,right*i))
        data_ranged.append([])
    print(len(data_ranged))
    for i in dataset:
        pos = int(i//interval)
        data_ranged[pos].append(i)
    for t in data_ranged:
        histogram_data.append(len(t))
    return histogram_data
            
def hist_data_for_each_exp(list_txt):
    out_list = []
    for i in list_txt:
        tmp = divide_by_timebin(i)
        out_list.extend(tmp)
    return out_list

def hist_data_for_each_exp_percentage(list_txt):
    cant_photons = len(list_txt)
    out_list = []
    for i in list_txt:
        tmp = divide_by_timebin(i)
        out_list.extend(tmp)
    return [x/cant_photons for x in out_list]

def mean_list(list_intervals):
    return sum(list_intervals)/len(list_intervals)

def poisson_distribution(n, t):
    print(math.e**(-n))
    x =((n**t)*(math.e**(-n)))/math.factorial(t)
    print(x)
    return x
from collections import Counter

def counter_ilist(list_count):
    dict_from_list = dict(Counter(list_count))
    y,x = [],[]
    for i in dict_from_list:
        y.append(dict_from_list[i])
        x.append(i)
    return y,x
        
    
def bose_ein_distribution(n, t):
    x = (1/(n+1))*((n/n+1)**t)
    print(x)
    return x
def moment_generator(interval_list):
    return mu
if __name__ == "__main__":
    #sample plots
    list_static, list_spinning = static_spinning_lists()
    plot_sample_lineal(list_static, list_spinning)
    #histogram
    flatten_spinning = merge_files_per_experiment(list_spinning)
    flatten_static = merge_files_per_experiment(list_static)
    get_average_stdev(flatten_static, flatten_spinning)
    data_hist_static = hist_data_for_each_exp(list_static)
    data_hist_spinning = hist_data_for_each_exp(list_spinning)
    
    plot_hist(data_hist_static, 'static wheel histogram')
    plot_hist(data_hist_spinning, 'spinning wheel histogram')
    #plot percentage
    static_sum = sum(data_hist_static)
    spinning_sum = sum(data_hist_spinning)
    mean_static = mean_list(data_hist_static)   
    mean_spinning = mean_list(data_hist_spinning) 
    plot_hist_percentage(data_hist_static, 'static wheel histogram percentage')
    plot_hist_percentage(data_hist_spinning, 'spinning wheel histogram percentage')
    pp = poisson_distribution(mean_static, 20)
    print(f'poisson {pp*100}%')
    bb = bose_ein_distribution(mean_spinning,20)
    print(f'bose {bb*100}%')
    x,y =counter_ilist(data_hist_static)
    plot_hist2(y,x,'static')
    x,y =counter_ilist(data_hist_spinning)
    plot_hist2(y,x,'spinning')
