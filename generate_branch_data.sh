#!/bin/bash

git clone $1 cloned_repo
base_branch=$2
other_branch=$3
cd cloned_repo
mkdir ../branch_output_files
# Checkout other branch, get list of all code files changed between branches
git diff ${base_branch}...${other_branch} --diff-filter=cdrtuxb --name-only -- '*.cpp' '*.h' '*.c' '*.hpp' > ../branch_output_files/file_list.txt

if [ -n "$(cat ../branch_output_files/file_list.txt)" ]; then
	# Compare branches
	git checkout $base_branch
	base_branch_sanitized=$(echo $base_branch | tr "/" "-")
	pmccabe $(cat ../branch_output_files/file_list.txt) > ../branch_output_files/pmccabe_$base_branch_sanitized.txt
	lizard -t 6 $(cat ../branch_output_files/file_list.txt) > ../branch_output_files/lizard_$base_branch_sanitized.txt

	git checkout $other_branch
	other_branch_sanitized=$(echo $other_branch | tr "/" "-") 
	pmccabe $(cat ../branch_output_files/file_list.txt) > ../branch_output_files/pmccabe_$other_branch_sanitized.txt
	lizard -t 6 $(cat ../branch_output_files/file_list.txt) > ../branch_output_files/lizard_$other_branch_sanitized.txt
fi
