import subprocess, sys, os

import Default

TIMEOUT_DEF = Default.TIMEOUT_DEF

def run(source, funcname, args):
    #Remove files
    if os.path.exists(Default.modify):
        os.remove(Default.modify)
    
    f = open(Default.modify, 'w')
    f.close()
    
    str_args = ''
    if (len(args) > 0):
        str_args = ",".join([str(elem) for elem in args])
    process = subprocess.Popen(["python3", "-c", "{0} \n{1}({2})".format(source, funcname, str_args)], 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE)
    try: 
        bouts, berrors = process.communicate(timeout=TIMEOUT_DEF)
    except subprocess.TimeoutExpired:    
        process.kill()
        print("The function {0} timed out".format(funcname))
        sys.exit(3)
    outs, errors = bouts.decode('utf-8'), berrors.decode('utf-8')
    
    ret_proc = process.poll()
    if (ret_proc < 0):
        print("The function {0} ended with exit value {1}".format(funcname, str(-ret_proc)))
        sys.exit(3)    
    if (len(errors) > 0):
        print("The function {0} ended with errors \n {1}".format(funcname, errors))
        sys.exit(3)    
    
    assert os.path.exists(Default.modify)
    
    return True