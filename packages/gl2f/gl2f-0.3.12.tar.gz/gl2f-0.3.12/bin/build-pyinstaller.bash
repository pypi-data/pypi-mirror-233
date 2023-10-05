#!/bin/bash

bin=$(dirname "${BASH_SOURCE:-$0}")
echo $bin

src="${bin}/data/main.py"
pyinstaller $src --onefile --name gl2f --collect-data gl2f
