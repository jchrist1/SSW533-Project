# TODO parse arguments for branch names
# TODO pull data from files
# TODO read config .json file
# TODO evaluate conditions from .json on data from files

import argparse
import json

def extract_data(data_file):
    data={}
    with open( data_file, 'r' ) as fdata:
        for line in fdata:
            fields = line.split("\t")
            mod_cc = int(fields[0])
            trad_cc = int(fields[1])
            num_statements = int(fields[2])
            num_lines = int(fields[4])
            file_name = fields[5].split("(")[0]
            function_name = fields[5].split(":")[1].strip()
            line_data = {'mod_cc':mod_cc, 'trad_cc':trad_cc, 'num_lines':num_lines, 'fn':function_name}
            if file_name not in data:
                data[file_name]=[line_data]
            else:
                data[file_name].append(line_data)
    return data

def get_file_length_warnings(base_data, other_data, max_len):
    over_length_files=[]
    for file_data in other_data.items():
        length = 0
        for function_data in file_data[1]:
            length += function_data['num_lines']
        if length > max_len:
            over_length_files.append(file_data[0])
    for file_name in over_length_files:
        if file_name in base_data.keys():
            length=0
            for function_data in base_data[file_name]:
                length += function_data['num_lines']
            if length > max_len:
                over_length_files.remove(file_name)
    return over_length_files


def get_file_num_functions_warnings(base_data, other_data, max_fn):
    over_max_fn_files=[]
    for file_data in other_data.items():
        num_fn = len(file_data[1])
        if num_fn > max_fn:
            over_max_fn_files.append(file_data[0])
    for file_name in over_max_fn_files:
        if file_name in base_data.keys():
            num_fn = len(base_data[file_name])
            if num_fn > max_fn:
                over_max_fn_files.remove(file_name)
    return over_max_fn_files

def get_file_total_ccn_warnings(base_data, other_data, max_ccn, use_modified):
    over_max_ccn_files=[]
    for file_data in other_data.items():
        ccn = 0
        for function_data in file_data[1]:
            if use_modified:
                ccn += function_data['mod_cc']
            else:
                ccn += function_data['trad_cc']
        if ccn > max_ccn:
            over_max_ccn_files.append(file_data[0])
    for file_name in over_max_ccn_files:
        if file_name in base_data.keys():
            ccn = 0
            for function_data in base_data[file_name]:
                if use_modified:
                    ccn += function_data['mod_cc']
                else:
                    ccn += function_data['trad_cc']
            if ccn > max_ccn:
                over_max_ccn_files.remove(file_name)
    return over_max_ccn_files

def get_function_ccn_warnings(base_data, other_data, max_ccn, use_modified):
    over_max_ccn_fns=[]
    lookup_key = 'trad_cc'
    if use_modified:
        lookup_key = 'mod_cc'
    for file_data in other_data.items():
        for function_data in file_data[1]:
            if function_data[lookup_key] > max_ccn:
                file_fn_tup = (file_data[0], function_data['fn'])
                if file_fn_tup not in over_max_ccn_fns: 
                    over_max_ccn_fns.append(file_fn_tup)
    for file_name_fn_tup in over_max_ccn_fns:
        if file_name_fn_tup[0] in base_data.keys():
            for function in base_data[file_name_fn_tup[0]]:
                if function['fn'] == file_name_fn_tup[1]:
                    if function[lookup_key] > max_ccn:
                        over_max_ccn_fns.remove(file_name_fn_tup)
                    break
    return over_max_ccn_fns

def get_function_length_warnings(base_data, other_data, max_len):
    over_max_len_fns=[]
    for file_data in other_data.items():
        for function_data in file_data[1]:
            if function_data['num_lines'] > max_len:
                file_fn_tup = (file_data[0], function_data['fn'])
                if file_fn_tup not in over_max_len_fns:
                    over_max_len_fns.append(file_fn_tup)
    for file_name_fn_tup in over_max_len_fns:
        if file_name_fn_tup[0] in base_data.keys():
            for function in base_data[file_name_fn_tup[0]]:
                if function['fn'] == file_name_fn_tup[1]:
                    if function['num_lines'] > max_len:
                        over_max_len_fns.remove(file_name_fn_tup)
    return over_max_len_fns

def main():
    config={'file_len':{'enabled':True,'max':500},
            'file_ccn':{'enabled':True,'max':100,'use_modified':False},
            'file_fns':{'enabled':True,'max':30},
            'function_len':{'enabled':True,'max':300},
            'function_ccn':{'enabled':True,'max':20,'use_modified':False}}
    parser = argparse.ArgumentParser(description='Process results of branch comparison')
    parser.add_argument('base', help='name of base branch')
    parser.add_argument('other', help='name of branch merging to base branch')
    parser.add_argument('--config', help='location of configuration for comparison criteria')
    args = parser.parse_args()
    if args.config is not None:
        with open( args.config, 'r') as config_file:
            config = json.loads(config_file.read())
    
    base_file = './branch_output_files/pmccabe_' + args.base.replace('/', '-')  + '.txt'
    other_file = './branch_output_files/pmccabe_' + args.other.replace('/', '-') + '.txt'
    
    base_data = extract_data(base_file)
    other_data = extract_data(other_file)
    if config['file_len']['enabled']:
        files = get_file_length_warnings(base_data, other_data, config['file_len']['max'])
        with open('branch_output_files/file_length_warnings.txt', 'w') as result:
            for fname in files:
                result.write(fname + '\n')
    if config['file_ccn']['enabled']:
        files = get_file_total_ccn_warnings(base_data, other_data, config['file_ccn']['max'], config['file_ccn']['use_modified'])
        with open('branch_output_files/file_ccn_warnings.txt', 'w') as result:
            for fname in files:
                result.write(fname + '\n')
    if config['file_fns']['enabled']:
        files = get_file_num_functions_warnings(base_data, other_data, config['file_fns']['max'])
        with open('branch_output_files/file_num_fns_warnings.txt', 'w') as result:
            for fname in files:
                result.write(fname + '\n')
    if config['function_len']['enabled']:
        filefns = get_function_length_warnings(base_data, other_data, config['function_len']['max'])
        with open('branch_output_files/fn_len_warnings.txt', 'w') as result:
            for filefn in filefns:
                result.write(filefn[0] + ':' + filefn[1] + '\n')
    if config['function_ccn']['enabled']:
        filefns = get_function_ccn_warnings(base_data, other_data, config['function_ccn']['max'], config['function_ccn']['use_modified'])
        with open('branch_output_files/fn_ccn_warnings.txt', 'w') as result:
            for filefn in filefns:
                result.write(filefn[0] + ':' + filefn[1] + '\n')


if __name__ == "__main__":
    main()
