import numpy as np
import getopt
import vars.utils as utils
import glob
import sys

def parse_logs(files):

    marginal_likelihood = []
    for file in files:
        handle = open(file,'r')
        for line in handle:
            if 'Marginal Likelihood' in line:
                m = float(line.strip().split('=')[1])
                marginal_likelihood.append(m)
                break
        handle.close()

    return marginal_likelihood

def parse_varQs(files):

    bestKs = []
    for file in files:
        handle = open(file,'r')
        Q = np.array([map(float,line.strip().split()) for line in handle])
        Q = Q/utils.insum(Q,[1])
        handle.close()

        N = Q.shape[0]
        C = np.cumsum(np.sort(Q.sum(0))[::-1])
        bestKs.append(np.sum(C>=N-1))

    return bestKs

def parseopts(opts):

    """
    parses the command-line flags and options passed to the script
    """

    for opt, arg in opts:

        if opt in ["--input"]:
            filetag = arg

    return filetag

def usage():

    """
    brief description of various flags and options for this script
    """

    print "\nHere is how you can use this script\n"
    print "Usage: python %s"%sys.argv[0]
    print "\t --input=<file>"

if __name__=="__main__":

    # parse command-line options
    argv = sys.argv[1:]
    bigflags = ["input="]
    try:
        opts, args = getopt.getopt(argv, bigflags)
        if not opts:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        print "Incorrect options passed"
        usage()
        sys.exit(2)

    filetag = parseopts(opts)

    files = glob.glob('%s.*.log'%filetag)
    Ks = np.array([int(file.split('.')[1]) for file in files])
    marginal_likelihoods = parse_logs(files)

    files = glob.glob('%s.*.meanQ'%filetag)
    bestKs = parse_varQs(files)

    print "Model complexity that maximizes marginal likelihood = %d"%Ks[np.argmax(marginal_likelihoods)]
    print "Model components used to explain structure in data = %d"%np.mode(bestKs) 