#!/bin/bash

git clone $1 cloned_repo
cd cloned_repo
git log --reverse > commit_log.txt
awk '{ if($1 == "commit") print $2;}' commit_log.txt > commit_hash.txt
mkdir ../commit_output_files
commit_couter=0
previous_commit=git rev-list --max-parents=0 HEAD
cat commit_hash.txt | while read line
do
git checkout $line
git diff $previous_commit $line --diff-filter=cdrtuxb --name-only -- '*.cpp' '*.h' '*.c' '*.hpp'  > ../commit_output_files/tmp_list.txt
files_changed=$(cat ../commit_output_files/tmp_list.txt | wc -l)

# only create file entries if there have been changes
if [ $files_changed -gt 0 ]; then
echo "$files_changed" >> ../commit_output_files/changed.txt
pmccabe $(cat ../commit_output_files/tmp_list.txt) > ../commit_output_files/pmccabe_$commit_couter.txt
lizard -t 6 -l cpp --csv $(cat ../commit_output_files/tmp_list.txt) > ../commit_output_files/lizard_$commit_couter.txt
commit_couter=$((commit_couter+1))
fi

previous_commit=$line
done
