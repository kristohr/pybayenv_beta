#!/local/bin/python
import sys, os

try:
    texfilename = sys.argv[1]
except:
    print "Usage: %s <tex-file> [reader]" % sys.argv[0]
    sys.exit(1)

# run latex
cmd = "latex %s" % texfilename
failure = os.system(cmd)
if failure:
    print "running latex failed";  sys.exit(1)

# run dvips
dvifilename = "%s.dvi" % texfilename[:-4]
psfilename = "%s.ps" % texfilename[:-4]
cmd = "dvips %s -o %s" % (dvifilename, psfilename)
failure = os.system(cmd)
if failure:
    print "running dvips failed";  sys.exit(1)

# converte from ps to pdf
cmd = "ps2pdf %s" % psfilename
failure = os.system(cmd)
if failure:
    print "running ps2pdf failed";  sys.exit(1)

# run acroread
try:
    reader = sys.argv[2]
except:
    # dont run acroread, just continue
    sys.exit(0)
    
cmd = "%s %s.pdf &" % (reader, texfilename[:-4])
failure = os.system(cmd)
if failure:
    print "running %s failed" % reader;  sys.exit(1)

