#!/bin/sh

is_all=0
while getopts a opt
do
    case ${opt} in
    a)
        is_all=1;;
    ?)
        exit 1;;
    esac
done

if [ $is_all -ne 0 ]; then
    echo "process all data!!"
fi
