#!/bin/bash

process_css() {
    for file in ./static_files/less/*.less
    do
        file_name=${file%.less}
        echo "Processing $file"
        lessc ${file} > ${file_name}.css
    done
}

process_css

chsum1=`ls -lR static_files/less/ | md5`
chsum2=$chsum1

while [[ true ]]
do
    sleep 1
    chsum2=`ls -lR static_files/less/ | md5`

    if [[ $chsum1 != $chsum2 ]] ; then
        process_css

        chsum1=`ls -lR static_files/less/ | md5`
        chsum2=$chsum1
    fi
done
