import sys, string, re,  os, commands, time

#from scipy import stats

#import scipy as sp

import numpy as np

#import matplotlib as mpl

#from matplotlib import pyplot as plt


class Locus_diff:
    
    def __init__(self, name, num_files):

        self.name = name.strip()
        self.is_in_run = [[0 for x in xrange(1)] for x in xrange(num_files)] 
        self.sum_bf = 0
        self.num_runs = 0
        self.bf_list = []

    def get_name(self):
        return self.name

    def set_in_run(self, run):
        self.is_in_run[run] = 1
        self.num_runs += 1

    def get_in_run(self):
        return self.is_in_run

    def add_bf(self, bf):
        self.sum_bf += bf
        
    def add_to_list(self, bf):
        self.bf_list.append(bf)
        
    def get_sum_bf(self):
        return self.sum_bf
    
    def get_num_runs(self):
        return self.num_runs

    def get_median_bf(self):
        factors = np.array(self.bf_list)
        median = np.median(factors)
        return median
        
    def get_average_bf(self):
        factors = np.array(self.bf_list)
        avg = np.average(factors)
        return avg

    def get_bf_list(self):
        return self.bf_list
        

def create_bin_matrix(in_files, n):

    num_files = len(in_files)
    out_file = "results/" + str(n) + "bin_dist.txt"
    avg_file = "results/" + str(n) + "average_bf.txt"
    median_file = "results/" + str(n) + "median_bf.txt"

    locus_list = [] #List of locus names

    in_list = {}
    locus_dict = {}

    for i in range(0, num_files):
        #print in_files[i]
        dataset = open(in_files[i], 'r')
        lines = dataset.readlines()
        for line in lines:
            data = line.split("\t")
            name = data[0]
            if i < 10:
                name = name[:-2] #Removing last two chars from marker name
            else:
                name = name[:-3] #Removing last three chars from marker name
            res = data[1]
            if (not name in in_list):
                locus = Locus_diff(name, num_files)
                locus_list.append(locus)
                locus.set_in_run(i)
                locus.add_bf(float(res))
                in_list[name] = locus
                locus.add_to_list(float(res))
            else:
                in_list[name].set_in_run(i)
                in_list[name].add_bf(float(res))
                in_list[name].add_to_list(float(res))
            
                
        #print "New file ..............................................."

    #all_data = "Marker\t5000_Iterations\t10000_Iterations\t15000_Iterations\t20000_Iterations\t25000_Iterations\t30000_Iterations\n"
    all_data = ""
    for i in range(0, len(locus_list)):
        data_line = "" + locus_list[i].get_name() + "\t"
        data = locus_list[i].get_in_run()
        for j in range(0, len(data)):
            data_line += str(data[j]) + "\t"
        #data_line += "0" #dummy for random var.
        data_line += str(locus_list[i].get_num_runs()) + "\t"
##         bf_list = locus_list[i].get_bf_list()
##         for j in range(0, len(bf_list)):
##             data_line += str(bf_list[j]) + "\t"
        all_data += data_line + "\n"

    all_data =  all_data.replace("[", "")
    all_data =  all_data.replace("]", "")

    #print all_data
    
    print "Total significant SNPs for var " + str(n) + " is " + str(len(in_list))

    FILE = open(out_file, 'w')
    FILE.write(all_data)
    FILE.close()

    average_bf = ""
    median_bf = ""
    for i in range(0, len(locus_list)):
        average_bf += locus_list[i].get_name() + "\t"
        #average_bf += str(locus_list[i].get_sum_bf()/num_files) + "\n"
        average_bf += str(locus_list[i].get_average_bf()) + "\n"
        median_bf += locus_list[i].get_name() + "\t"
        median_bf += str(locus_list[i].get_median_bf()) + "\n"

    

    FILE = open(avg_file, 'w')
    FILE.write(average_bf)
    FILE.close()
    
    FILE = open(median_file, 'w')
    FILE.write(median_bf)
    FILE.close()
