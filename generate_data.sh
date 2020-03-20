#!/bin/bash

git clone $1 cloned_repo
cd cloned_repo
git log --merges --reverse > commit_log.txt
awk '{ if($1 == "commit") print $2;}' commit_log.txt > commit_hash.txt
mkdir ../commit_output_files
commit_couter=0
previous_commit=git rev-list --max-parents=0 HEAD
cat commit_hash.txt | while read line
do
commit_couter=$((commit_couter+1))
git checkout $line
git diff $previous_commit $line --diff-filter=am --name-only | find  \( -name '*.cpp' -o -name '*.h' -o -name '*.c' -o -name '*.hpp'  \)  >> ../commit_output_files/tmp_list.txt
cat ../commit_output_files/tmp_list.txt | wc -l >> ../commit_output_files/changed.txt
pmccabe $(cat ../commit_output_files/tmp_list.txt) > ../commit_output_files/pmccabe_$commit_couter.txt
lizard -t 6 $(cat ../commit_output_files/tmp_list.txt) > ../commit_output_files/lizard_$commit_couter.txt
echo  $commit_couter
done
