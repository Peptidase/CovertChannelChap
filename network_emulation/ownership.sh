#!/bin/bash

for item in ./captures/*; do
    chown ace-student:ace-student "$item" && echo "Changed ownership: $item"
done