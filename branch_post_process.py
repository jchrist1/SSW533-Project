# TODO parse arguments for branch names
# TODO pull data from files
# TODO read config .json file
# TODO evaluate conditions from .json on data from files

import argparse

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

def get_file_length_warnings(base_data, other_data):
    TODO_MAX_LENGTH=500
    over_length_files=[]
    for file_data in other_data.items():
        length = 0
        for function_data in file_data[1]:
            length += function_data['num_lines']
        if length > TODO_MAX_LENGTH:
            over_length_files.append(file_data[0])
    for file_name in over_length_files:
        if file_name in base_data.keys():
            length=0
            for function_data in base_data[file_name]:
                length += function_data['num_lines']
            if length > TODO_MAX_LENGTH:
                over_length_files.remove(file_name)
    return over_length_files


def get_file_num_functions_warnings(base_data, other_data):
    TODO_MAX_FUNCTIONS=30
    over_max_fn_files=[]
    for file_data in other_data.items():
        num_fn = len(file_data[1])
        if num_fn > TODO_MAX_FUNCTIONS:
            over_max_fn_files.append(file_data[0])
    for file_name in over_max_fn_files:
        if file_name in base_data.keys():
            num_fn = len(base_data[file_name])
            if num_fn > TODO_MAX_FUNCTIONS:
                over_max_fn_files.remove(file_name)
    return over_max_fn_files

def get_file_total_ccn_warnings(base_data, other_data, use_modified=False):
    TODO_MAX_CCN = 100
    over_max_ccn_files=[]
    for file_data in other_data.items():
        ccn = 0
        for function_data in file_data[1]:
            if use_modified:
                ccn += function_data['mod_cc']
            else:
                ccn += function_data['trad_cc']
        if ccn > TODO_MAX_CCN:
            over_max_ccn_files.append(file_data[0])
    for file_name in over_max_ccn_files:
        if file_name in base_data.keys():
            ccn = 0
            for function_data in base_data[file_name]:
                if use_modified:
                    ccn += function_data['mod_cc']
                else:
                    ccn += function_data['trad_cc']
            if ccn > TODO_MAX_CCN:
                over_max_ccn_files.remove(file_name)
    return over_max_ccn_files

def get_function_ccn_warnings(base_data, other_data, use_modified=False):
    TODO_MAX_CCN=20
    over_max_ccn_fns=[]
    lookup_key = 'trad_cc'
    if use_modified:
        lookup_key = 'mod_cc'
    for file_data in other_data.items():
        for function_data in file_data[1]:
            if function_data[lookup_key] > TODO_MAX_CCN:
                file_fn_tup = (file_data[0], function_data['fn'])
                if file_fn_tup not in over_max_ccn_fns: 
                    over_max_ccn_fns.append(file_fn_tup)
    for file_name_fn_tup in over_max_ccn_fns:
        if file_name_fn_tup[0] in base_data.keys():
            for function in base_data[file_name_fn_tup[0]]:
                if function['fn'] == file_name_fn_tup[1]:
                    if function[lookup_key] > TODO_MAX_CCN:
                        over_max_ccn_fns.remove(file_name_fn_tup)
                    break
    return over_max_ccn_fns

def get_function_length_warnings(base_data, other_data):
    TODO_MAX_FN_LENGTH=300
    over_max_len_fns=[]
    for file_data in other_data.items():
        for function_data in file_data[1]:
            if function_data['num_lines'] > TODO_MAX_FN_LENGTH:
                file_fn_tup = (file_data[0], function_data['fn'])
                if file_fn_tup not in over_max_len_fns:
                    over_max_len_fns.append(file_fn_tup)
    for file_name_fn_tup in over_max_len_fns:
        if file_name_fn_tup[0] in base_data.keys():
            for function in base_data[file_name_fn_tup[0]]:
                if function['fn'] == file_name_fn_tup[1]:
                    if function['num_lines'] > TODO_MAX_FN_LENGTH:
                        over_max_len_fns.remove(file_name_fn_tup)
    return over_max_len_fns

def main():
    parser = argparse.ArgumentParser(description='Process results of branch comparison')
    parser.add_argument('base', help='name of base branch')
    parser.add_argument('other', help='name of branch merging to base branch')
    parser.add_argument('--config', help='location of configuration for comparison criteria')
    args = parser.parse_args()

    base_file = './branch_output_files/pmccabe_' + args.base.replace('/', '-')  + '.txt'
    other_file = './branch_output_files/pmccabe_' + args.other.replace('/', '-') + '.txt'
    
    base_data = extract_data(base_file)
    other_data = extract_data(other_file)
    print( get_file_length_warnings(base_data, other_data) )
    print('')
    print( get_file_num_functions_warnings(base_data, other_data) )
    print('')
    print( get_file_total_ccn_warnings(base_data, other_data) )
    print('')
    print( get_function_ccn_warnings(base_data, other_data) )
    print('')
    print( get_function_length_warnings(base_data, other_data) )
    

if __name__ == "__main__":
    main()
