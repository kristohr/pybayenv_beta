from create_bin_dist import *

import sys, string, re,  os, commands, time

import numpy as np

EPSILON2 = 0.5
ALPHA = 10

def gen_delta(num_sign_bfs, highest_bf, epsilon):

    if num_sign_bfs < 1:
        num_sign_bfs = 1

    delta_hat = epsilon + np.log10(num_sign_bfs)*np.log10(highest_bf)

    return delta_hat

####################### RUN SDM ON THE RESULTS #############################
def compute_results(n, a):
    #DELTA = float(d)

    global EPSILON2
    global ALPHA
    
    N = int(n) #Number of runs
    A = int(a) #Number of environmental vars

    epsilon = EPSILON2
    alpha = ALPHA

    if epsilon > 1:
        epsilon = 1
    if epsilon <= 0:
        epsilon = 0.001

    for i in range(1, N+1):
        data = open("results/bf_results_t" + str(i-1) + ".bf", 'r')
        lines = data.readlines()

        #header = lines[0]
        #lines.pop(0)

        for j in range(1, A+1):
        
            res = int(j)
        
            v = [] #Bayes Factor for
            w = []
            for line in lines:
                v.append(float(line.split()[res]))
                w.append((float(line.split()[res]), line.split()[0]))

            sec_diff = []

            sorted_data = sorted(w, reverse=True)

            #print "i = "+ str(i)
            #print "j = " +str(j)

            out_filename = "results/" + str(i) + str(j) + "data.txt"
            out_filename2 = "results/" + str(i) + str(j) + "-diff_abs.txt"
            out_filename3 = "results/" + str(i) + str(j) + "-diff.txt"
    
            f = open(out_filename, 'w')
    
            f2 = open(out_filename2, 'w')
            f3 = open(out_filename3, 'w')

            bf = np.sort(np.array(v))

            print "*** var " + str(j) + " test " + str(i) + " ***"

            nbf = len(bf[bf>alpha]) #Number of bf > alpha=10

            bfh = bf[len(bf)-1] #Highest value in the distribution

            DELTA = gen_delta(nbf, bfh, epsilon)

            print "alpha = " + str(alpha)
            print "epsilon = "  + str(epsilon)
            print "N_alpha: " + str(nbf)
            print "A: " + str(bfh)
            print "delta_hat: " + str(DELTA)


            k = 0 #cut off value

            di = np.diff(bf,n=2)
            x2 = np.arange(len(di))+1

            found_delta = False
            for x in range(0, len(di)):
                diff = di[x]
                f2.write(str(abs(di[x]))+"\n")
                f3.write(str(di[x])+"\n")
                if (diff > DELTA):
                    if not found_delta:
                        print "Second difference = " + str(diff)
                        print "Lowest sign BF: " + str(bf[x+2])
                        print "Highest not sign BF: " + str(bf[x+1])
                        #print "Cutoff difference:"
                        #print "i-2=" + str(bf[x]) + " i-1=" + str(bf[x+1]) + " i=" + str(bf[x+2]),
                        print "Excluded SNPs = " + str(x+2)
                        k = x+2
                        found_delta = True
                        #Continue checking sec diff
                    #break
                
            #print "k=" + str(k)
            
            if k == 0:
                print "No SD larger than DELTA!. Defining the highest ranking SNP as significant."
                bf = bf[(len(bf))-1:]
            else:         
                bf = bf[k:]
            #print bf
            sorted_data = sorted_data[0:len(bf)]

            to_file = ""
            for d in sorted_data:
                to_file +=  d[1] + "\t" + str(d[0]) + "\n"

            f.write(to_file)
            f.close()
            f2.close()
            
            print "Total significant snps for var " + str(j) + " test " + str(i) + " is " + str(len(bf))
            print "________________________________"



##     log_bf = np.log(bf)

##     plt.plot(bf, 'bo')
##     plt.ylabel('some numbers')
##     plt.show()

    for i in range(1, A+1):
        l = []
        for j in range(1, N+1):
            file_name = "results/" + str(j) + str(i) + "data.txt"
            l.append(file_name)
        create_bin_matrix(l, i)


  
if __name__ == '__main__':
    
    # Terminate if too few arguments
    if len(sys.argv) < 3:
        print 'usage: %s <number of runs> <number of vars>' % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])
