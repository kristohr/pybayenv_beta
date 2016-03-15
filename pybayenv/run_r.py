    

#Sorting and plotting data in R
def run_r_cmd(data_file, n):

    cmd = "./plot_res.R %s %d" % (data_file, n)
    print "Runnig R-script..."
    sys.stdout.flush()
    failure, output = commands.getstatusoutput(cmd)
    print "R-script done."

    if failure:
        print output
        sys.exit(1)
