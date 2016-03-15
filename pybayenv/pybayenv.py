#!/local/bin/python

from locus import *
from run_bayenv import *
from standardize import *
from sec_diff import *
from plot_results import *
import random

import sys, string, re,  os, commands, time
from scipy import stats
import scipy as sp
import numpy as np

from sec_diff import *

try:
    import matplotlib as mpl
    from matplotlib import pyplot as plt
except:
    plt = None
    mpl = None

#from random import *

DEBUG = False
SKIP_COVAR = False #True if skipping building the null model
SKIP_TEST = False #True if tests are skipped
NULL_FILE = "" #Alternative Null file
DIFF_NULL = False #True if different null file

NUM_TESTS = 8 #Number of tests performed

NUM_POP = 0 #Number of populations in the file
NUM_ENV = 6 #Number of environmental variablessss

NULL_SIZE = 0
TEST_SIZE = 0
ITERATIONS = "5000" #Number of iterations for the tests
CUT_OFF = 0.0 #Default cut off value (no cut off)
EPSILON = 0.1 #Small constant

#Removing temporary files
def clean():
    
    print "Removing temporary files..."
    sys.stdout.flush()
    failure, output = commands.getstatusoutput("rm covar*")
    print "done."

def debug(locus_list):
        
        freqs_file = open("freqs.txt", 'w')
        freqs_str = "marker\tfreq\n"
        
        for i in range(0, len(locus_list)):
            locus_list[i].set_freqs()
            locus_list[i].set_max_freq_diff()
            freqs_list.append(locus_list[i].get_max_freq_diff())
            freqs_str += locus_list[i].get_name() + "\t" + str(abs(locus_list[i].get_max_freq_diff())) + "\n"
##            if (not locus_list[i].is_consensus_locus(max_diff)):
        freqs_file.write(freqs_str)
        freqs_file.close()
       
        freqs_data = np.array(freqs_list)
        mean = freqs_data.mean()
        cut_off = stats.scoreatpercentile(freqs_data, cut_off_percent)
               
        count = 0
        for i in range(0, len(locus_list)):
            if (not locus_list[i].is_consensus_locus(cut_off)):
                #print i
                #print locus_list[i].pop
                #print locus_list[i].get_freqs()
                #print locus_list[i].get_max_freq_diff()
                count += 1
        print "Cut off: " + str(cut_off)
        print "Total test snps = "+  str(count)

        sorted_freqs_data = np.sort(abs(freqs_data))
        if plt is not None:
            plt.plot(sorted_freqs_data, 'bo')
            plt.ylabel('Maximum frequency difference')
            plt.show()


#Separating the covariance matrices from bayenv output
def write_covars():

    covar_dict = {}
    
    covars = open("covars.txt", 'r')
    

    for i in range(0, 8):
        covars.readline()

    matrix_counter = 0
    for line in covars:
        if ("VAR-COVAR" in line):
            matrix_counter += 1
            covar_dict["covar"+str(matrix_counter)] = ""
        else:
            covar_dict["covar"+str(matrix_counter)] += line
    #"covar_iter" + str(i) + ".txt"

    for i in range(1, len(covar_dict)+1):
        covar_file = open("covar_iter" + str(i) + ".txt", 'w')
        covar_file.write(covar_dict["covar"+str(i)])
        covar_file.close()
    
    covars.close() 


#Separating the covariance matrices from bayenv2 output
def write_mean_covar_bayenv2():

    covars = open("covars.txt", 'r')    

    #Removing the first 15 lines
    for i in range(0, 15):
        covars.readline()

   # matrix_counter = 0
    #for line in covars:
     #   if ("VAR-COVAR" in line):
     #       matrix_counter += 1
      #      covar_dict["covar"+str(matrix_counter)] = ""
      #  else:
      #      covar_dict["covar"+str(matrix_counter)] += line
    #"covar_iter" + str(i) + ".txt"

    #for i in range(1, len(covar_dict)+1):
     #   covar_file = open("covar_iter" + str(i) + ".txt", 'w')
     #   covar_file.write(covar_dict["covar"+str(i)])
     #   covar_file.close()

    
    covar_lists = []
    cov = []

    matrix_counter = 0
    for line in covars:
        if ("VAR-COVAR" in line):
            matrix_counter += 1
            covar_lists.append(cov)
            cov = []
        elif line == "\n":
            continue
        else:
            line = line.strip("\t\n")
            cov.append(line.split("\t"))

    #print "The covar list: "
    #print covar_lists[0]

    num_cov_matrix = np.array(covar_lists, np.float64)
    
    #print len(num_cov_matrix)
    #print num_cov_matrix
    
    #print "length of num_cov_matrix: "
    #print len(num_cov_matrix)

    matrix_mean = np.average(num_cov_matrix, axis=0)

    #print "\nMean matrix:"

    #print matrix_mean

    #print len(matrix_mean)

    covar_string = ""

    for list in matrix_mean:
        for elem in list:
            covar_string += str(elem) + "\t"
        covar_string += "\n"
    
    #print covar_string
    f = open("covar-cmd.txt", "a")
    f.write(covar_string)
    f.close()

    covar_file = open("mean_covar.txt", 'w')
    covar_file.write(covar_string)
    covar_file.close() 
    covars.close() 


    

############### Generate commands for BAYENV2 #################

def gen_commands(env_file, no_env_var):

    global NUM_TESTS
    global ITERATIONS
    global NUM_POP

    cmds = []
    num_tests = NUM_TESTS
    rand_seeds = [int(random.uniform(1,99999)) for i in range(1, num_tests+1)]

    additional_cmds = "" #Change to " -c" if computing rho

    for i, rand_seed in enumerate(rand_seeds):
        cmd = "bayenv2 -i %s -m mean_covar.txt -e " + env_file + \
            " -p " + str(NUM_POP) + \
            " -k " + str(ITERATIONS) + \
            " -n " + str(no_env_var) + \
            " -t -r " + str(rand_seed) + " -o %s" + additional_cmds

        f = open("test-cmd.txt", "a")
        f.write("Test " + str(i+1) + ":\n")
        f.write(cmd)
        f.write("\n")
        f.close()
        cmds.append(cmd)

#    for i, rand_seed in enumerate(rand_seeds):
#        cmds.append("bayenv2 -i %s -m " + "covar_iter" + str(i+1) + ".txt" + \
#                    " -e " + env_file + \
#                    " -p 3 " + \
#                    "-k 10000 " + \
#                    " -n " + str(no_env_var) + \
#                    " -t -c -r " + str(rand_seed) + " -o %s"
#                    + additional_cmds)
    #print cmds[0]
    return cmds

def gen_loci(in_file, num_pops):

    locus_list = [] #List of locus names
    
    dataset = open(in_file, 'r')
    lines = dataset.readlines()
    
    new_lines = []
    test = ""
    for line in lines:
        if (len(line) > 2):
            new_lines.append(line)
    
    #strip = open("stripped.txt", 'w')
    #strip.write(test)
    #strip.close()

    file_info = new_lines[0] #File header
    #print file_info
    line = new_lines[1] #Locus names
    header = line.replace(" ", "") 
    all_snps = header.split(',')
    for snp in all_snps:
        #print snp
        locus = Locus(snp, int(num_pops))
        locus_list.append(locus)

    new_lines.pop(0) #Removing the two first lines 
    new_lines.pop(0)
    pop = -1 #Population in the
    for line in new_lines:
        if ("Pop" in line or "pop" in line):
            pop += 1
            #print pop
            #print "length:" + str(len(line))
            #print line
            continue
        data = line.split()
        alleles = data[1::] #The allele data for each population
        for i in range(0, len(alleles)):
            al_type = get_allele_type(alleles[i])
            locus_list[i].update_freqs(al_type, pop)
            #print "**************************************"
            #print locus_list[i].get_freqs()

    return locus_list

def convert_fileformat(in_file, testdata):
    #global NULL_FILE
    #global ITERATIONS
    #global NUM_POP
    #global NULL_SIZE
    global TEST_SIZE
    global CUT_OFF
    #global NUM_ENV
    #global NUM_TESTS

    out_file = in_file.split(".")[0] + ".bnv"
    num_pops = str(NUM_POP)
    #Generate loci objects
    locus_list = gen_loci(in_file, num_pops)

    #print "Length of locus list =" + str(len(locus_list))
            
    freqs_list = []

    print "Cut off = " + str(CUT_OFF)

#    if (NULL_SIZE == 0):
#        NULL_SIZE = len(locus_list) 
#    if (TEST_SIZE == 0):
    TEST_SIZE = len(locus_list)

    #print "Test size = " + str(TEST_SIZE)    
    if (DEBUG):
        debug(locus_list)       
    else:
        
        for i in range(0, len(locus_list)):
            locus_list[i].set_freqs()
            locus_list[i].set_max_freq_diff()
            locus_list[i].to_string()
            freqs_list.append(locus_list[i].get_max_freq_diff())
    
        freqs_data = np.array(freqs_list)

        #print freqs_data
            
        count = 0
        lines1 = ""
        for i in range(0, TEST_SIZE):
            lines1 += locus_list[i].freqs_to_lines()
            count += 1
            
        print "Total loci in null model = "+  str(count)

        count = 0
        lines2 = ""  
        print "########################################"
        print "TEST_SIZE = " + str(TEST_SIZE)
        print "########################################"
        if (CUT_OFF < EPSILON):   
            for i in range(0, TEST_SIZE):
                lines2 += locus_list[i].freqs_to_lines2()
                count += 1
            print "Total test snps = "+  str(count)
        elif (testdata):  
            print "Computing cutoff data.."
            cut_off = stats.scoreatpercentile(freqs_data, CUT_OFF)
            print "Maximum allele frequency cutoff: " + str(cut_off)
            for i in range(0, TEST_SIZE):
                if (locus_list[i].get_max_freq_diff() > cut_off):
                    lines2 += locus_list[i].freqs_to_lines2()
                    count += 1
            print "Total test snps = "+  str(count)
            print "Total excluded snps = "+  str(TEST_SIZE - count)
        else:  
            cut_off = stats.scoreatpercentile(freqs_data, CUT_OFF)
            for i in range(0, TEST_SIZE):
                if (not locus_list[i].is_consensus_locus(cut_off)):
                    lines2 += locus_list[i].freqs_to_lines2()
                    count += 1
            print "Total test snps = "+  str(count)

        FILE = open(out_file, 'w')
        FILE.write(lines1)
        FILE.close()

        new_out_file = "2"+out_file
        FILE = open(new_out_file, 'w')
        FILE.write(lines2)
        FILE.close()
        TEST_SIZE = count
        return out_file, new_out_file
    
####################### Main #############################
def main(in_file, var_file):

    global NULL_FILE
    global ITERATIONS
    global NUM_POP
    global NULL_SIZE
    global TEST_SIZE
    global CUT_OFF
    global NUM_ENV
    global NUM_TESTS
    global NULL_FILE

    #rand_seed = "-47123"
    #no_env_var = 6
    max_diff = 0.5
    test = 0
    cut_off_percent = 99.5 #Percent to cut of from testing.

    #Standardizing the env variables
    env_file, no_env_var  = standardize_env(var_file) 

    #Temporary measures
    no_env_var = NUM_ENV #Number of environment variables to compute...

    #convert to bayenv file format
    #convert_fileformat(in_file)

    #Generate the BAYENV command - IN USE!!!
    cmds = gen_commands(env_file, no_env_var)
    
    #Create the null modell
    #n_iter = int(ITERATIONS)/5000
    if (SKIP_COVAR and SKIP_TEST):
        print "Skipping null model and testing..."
        print NUM_TESTS
        print "Converting to bayenv format..."
        #convert to bayenv file format
        convert_fileformat(in_file, True)
        try:
            print "Computing significance..."
            compute_results(NUM_TESTS, no_env_var) 
        except:
            print "Could not perform significance analysis, no data available!"
        #Plot significance diagram
        #run_r_cmd(NUM_TESTS, NUM_ENV)

    elif (SKIP_COVAR):
        print "Skipping null model..."
        out_file, new_out_file = convert_fileformat(in_file, True)
        test_all_snps_multip(new_out_file, cmds, TEST_SIZE)
        try:
            compute_results(NUM_TESTS, no_env_var) 
        except:
            print "Could not perform significance analysis, no data available!"
    elif (SKIP_TEST):
        print "Skipping testing..."
        try:
            if DIFF_NULL:
                print "Computing different null = " + NULL_FILE
                out_file, new_out_file = convert_fileformat(NULL_FILE)
                compute_null_model_bayenv2(num_pops, ITERATIONS, out_file)
                write_mean_covar_bayenv2()
            else:
                print "Computing same null = " + in_file
                out_file, new_out_file = convert_fileformat(in_file)
                compute_null_model_bayenv2(num_pops, ITERATIONS, out_file)
                write_mean_covar_bayenv2()
                
        except:
            print "Could not perform tests, no covariance matrix available!"
        try:
            compute_results(NUM_TESTS, no_env_var) 
        except:
            print "Could not perform significance analysis, no data available!"
           
    else:
            #print "Creating " + str(n_iter) + " covariance-variance matrices..."
            #compute_null_hyp(num_pops, rand_seed, ITERATIONS, out_file)
            #Split the output covar file into one for each 5000 iteration.
        if DIFF_NULL:
            print "Computing different null = " + NULL_FILE
            out_file, not_out_file = convert_fileformat(NULL_FILE)
            print out_file
            compute_null_model_bayenv2(NUM_POP, ITERATIONS, out_file)
            print "Covar created..."
            write_mean_covar_bayenv2()
            #Run multiprocessing tests - THE ACTUAL TEST!!!
            out_file, new_out_file = convert_fileformat(in_file)
            #print new_out_file
            test_all_snps_multip(new_out_file, cmds, TEST_SIZE)
            #Test the results with sec diff
            compute_results(NUM_TESTS, no_env_var)
        else:
            print "Computing same null = " + in_file
            print "###################" + in_file
            out_file, new_out_file = convert_fileformat(in_file, True)
            print out_file
            compute_null_model_bayenv2(NUM_POP, ITERATIONS, out_file)
            print "Covar created..."
            write_mean_covar_bayenv2() 
            #Run multiprocessing tests - THE ACTUAL TEST!!!
            test_all_snps_multip(new_out_file, cmds, TEST_SIZE)
            #Test the results with sec diff
            compute_results(NUM_TESTS, no_env_var)    


        #Run the test.
        #test_all_snps(new_out_file, env_file, n_iter, no_env_var)
        #test_all_snps_multit(new_out_file, env_file, no_env_var)



        #test_all_snps_seq(new_out_file, env_file, no_env_var)

       #clean() #Removing temporary files

  

##     for i in range(0, len(locus_list)):
##         print locus_list[i].name + str(locus_list[i].allele1)
##         print locus_list[i].name + str(locus_list[i].allele2)                   
            
##     for line in dataset:
##         data = line.split()
##         locus_name = data[0] #Name of Locus
##         stats, snp_dict = get_stats(data[1::]) #The SNP data
##         new_line = convert_line(line, stats)
##         locus_name = Locus(data, stats, snp_dict, line, new_line)
##         locus_list.append(locus_name)
       

##     #is_consensus_or_gap = 0 #Counter for consensus lines
##     is_consensus = 0
##     counter = 0


  
if __name__ == '__main__':
    
    # Terminate if too few arguments
    if len(sys.argv) < 3:
        print 'usage: %s <infile> <varfile>' % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])
