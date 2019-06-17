#!/usr/bin/env python3

"""

This program takes a file of GMS build status summary out put of work order IDs (obtained
by running genome model status project.id --summary-only) and output the GMS build statuses
in a tab-delimited file.  Work orders that have successfully completed all builds,
as well as work orders that do not have any models will be summarized in the terminal


Usage:  python3 gms_iprocessor.py <file containing GMS build status summary output>

"""

import sys
import os
import csv
import datetime


if len(sys.argv) !=2:
    sys.exit(__doc__)

if not os.path.isfile(sys.argv[1]):
    print('{} file not found'.format(sys.argv[1]))
    exit()
date_time = datetime.datetime.now().strftime("%m%d%y")
#hour_min = datetime.datetime.now().strftime("%H%M")

outfile = 'issue.status.date.tsv'
outfile_final = f'issue.status.{date_time}.tsv'
results = {}
#results_no={}
build_state ={}
yes_counter = 0
zero_counter = 0

def make_header(dictionary):
    # declare an empty header list
    header_list = []
    # then iterate over all of my subdict
    for key in dictionary:
        for key2 in dictionary[key]:
    # if the key is not in my header list, add to header list
            if key2 not in header_list:
                header_list.append(key2)
    # return a sorted header list
    return header_list



with open(sys.argv[1],'r') as myfile:
    for line in myfile:
        line = line.strip().split()
        build_state = {}
        if 'Resolving' in line:
            id = line[6].split('=')
            id_ss = id[1][:-4]
            next_line = next(myfile).strip().split()
            if 'none' in line:
                id = line[6].split('=')
                id_ss = id[1][:-4]
                if id_ss not in results:
                        results[id_ss] = {'Total': 0, 'Work Order ID': id_ss}

                        zero_counter += 1
            if 'Total:' in next_line and 'none' not in next_line:
                for l in next_line:
                    if ':' in l:
                        index_l= next_line.index(l)
                        #if l not in build_state:
                        build_state[l.split(':')[0]] = next_line[index_l + 1]
                        build_state['Work Order ID'] = id_ss

                    if id_ss not in results:
                        results[id_ss] = build_state

                yes_counter += 1


print("GMS work orders with no models: ", zero_counter)
print("GMS work orders with models: ", yes_counter)
print("total GMS work orders in QC queue: ", yes_counter + zero_counter)
print()

results_header = sorted(make_header(results),reverse=True)
results_header.insert(0,"Date")



with open(outfile, 'w') as of:
    outfile_dict = csv.DictWriter(of,fieldnames=results_header,delimiter='\t',extrasaction="ignore")
    outfile_dict.writeheader()

    for k in results:

        results[k]['Date'] = date_time

        outfile_dict.writerow(results[k])
        if 'Succeeded' in results[k] and int(results[k]['Total']) == int(results[k]['Succeeded']):
            print(f'{k} GMS work order with all succeeded builds ')
        if int(results[k]['Total'])== 0:
            print(f'{k} GMS work order with no models ')

with open(outfile, 'r') as fh, open(outfile_final,'w') as oh:
    fh_dict = csv.DictReader(fh,delimiter='\t')
    f_names = fh_dict.fieldnames
    oh_dict = csv.DictWriter(oh,fieldnames=f_names,delimiter='\t')
    oh_dict.writeheader()
    out_dict ={}
    for line in fh_dict:
        for l in line:
            if not line[l]:
                out_dict[l]= 0
            else:
                out_dict[l]= line[l]
        oh_dict.writerow(out_dict)

os.remove(outfile)







