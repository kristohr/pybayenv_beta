import sys, string, os, commands, time


#Sorting and plotting data in R
def run_r_cmd(tau, num_env):

    for i in range(1,num_env+1):

        cmd = "./plot_res.R " + str(i) + "bin_dist.txt " + str(i) + "average_bf.txt " + str(i) + "median_bf.txt " +  str(tau) + " " + str(num_env)
        print cmd
        print "Runnig R-script..."
        sys.stdout.flush()
        failure, output = commands.getstatusoutput(cmd)
        print "R-script done."

        if failure:
            print output
            sys.exit(1)
