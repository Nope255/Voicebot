#!/bin/bash

function tool_check() {
    if ! command -v python >/dev/null; then
        echo "Could not find Python in your operating system"
        exit 1
    fi 
}

function run() {
    local SOURCE_DIR="src"
    local MAIN_ENTRY="main.py"

    if [ ! -d "$SOURCE_DIR" ];then 
        echo "Could not find your $SOURCE_DIR"
        exit 1
    fi 

    cd "$SOURCE_DIR" || exit
    if [ ! -f "$MAIN_ENTRY" ]; then
        echo "Could not find your $MAIN_ENTRY"
        exit 1
    fi 

    python "$MAIN_ENTRY"
}

function main() {
    tool_check
    run
}

main