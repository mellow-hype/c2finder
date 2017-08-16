#!/usr/bin/env python3
# Author: @_hyperlogic
from subprocess import Popen, PIPE
from sys import argv
from sys import exit
from os import makedirs
from os.path import isdir
from time import strftime
import urllib.request
prompt = '[+++] '

def get_c2_ips():
    c2_list = []
    print("{}Downloading updated list of C2 IPs...".format(prompt))
    url = 'http://osint.bambenekconsulting.com/feeds/c2-ipmasterlist.txt'
    response = urllib.request.urlopen(url)
    data = response.readlines()
    
    for line in data:
        line_decoded = line.decode('utf-8')
        if line_decoded[0] is '#':
            continue
        else:
            c2_list.append(line_decoded.split(','))

    print("{}List of C2s has been updated.".format(prompt))
    return c2_list


def logger(logline, output_dir):
    logfile = output_dir + '/c2finder_' + strftime("%Y-%m-%d") + '.log'
    with open(logfile, 'a') as log_file:
        log_file.write(logline + '\n')
    log_file.close()


if __name__ == "__main__":

    # Bro-cut queries for different Bro logs to get the most relevant information 
    BROCUT = {
        "dns": 'bro-cut -d ts uid id.orig_h id.resp_h query rcode_name answers',
        "http": 'bro-cut -d ts uid id.orig_h id.resp_h method host uri',
        "conn": 'bro-cut -d ts uid id.orig_h id.orig_p id.resp_h id.resp_p',
        "files": 'bro-cut -d ts uid id.orig_h id.resp_h mime_type'
    }

    # Check argument length is valid and assign args to variables
    if len(argv) != 2:
        print("Usage: {} /path/to/log_dir/<name_of_log>".format(argv[0]))
        print("Example: {} bro/logs/current/dns".format(argv[0]))
        exit()
    target_log = argv[1]

    # If split and reference to index -1 fails, the target_log value passed was not a full path
    # so we keep whatever was originally there.
    try:
        log = target_log.split('/')[-1]
    except IndexError:
        log = target_log

    # Iterate through the list of C2 IP addresses and pass them to grepper.sh 
    c2list = get_c2_ips()
    output_dir = 'c2finder_' + strftime("%Y-%m-%d")

    print("{}Searching in {} log...\n".format(prompt, log))

    try:
        for entry in c2list:
            grepper = ['./grepper.sh', entry[0], target_log, BROCUT[log]]
            grepopen = Popen(grepper, stdout=PIPE, universal_newlines=True)
            grepopen.wait()
    
            if len(grepopen.stdout.readline()) < 1:
                continue
            else:
                if not isdir(output_dir):
                    makedirs(output_dir)
                log_line = "[+]: {} seen in {} log [{} ({})]".format(entry[0], log, entry[1], entry[2])
                print(log_line)
                logger(log_line, output_dir)
                ofile_path = output_dir + '/' + log + '_' + entry[0] +  '.txt'
                with open(ofile_path, 'w') as outfile:
                    for line in grepopen.stdout:
                        outfile.write(line)
                outfile.close()
    except KeyboardInterrupt:
        print("\n{}Output written to files in directory {}/".format(prompt, output_dir))
        exit()
    
