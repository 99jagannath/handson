#!/bin/bash

function clean_up_log_dir {
    for items in ./log_dir/nginx*; do
        echo $items;
        rm -rf $items;
    done
}

clean_up_log_dir