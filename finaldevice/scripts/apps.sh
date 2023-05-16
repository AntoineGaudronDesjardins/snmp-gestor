#!bin/bash
count=$(apt list --installed 2>/dev/null | wc -l)
echo $count 
