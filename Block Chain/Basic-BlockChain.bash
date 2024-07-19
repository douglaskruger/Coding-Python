#!/bin/bash
for i in `seq 1 10032`
do
        echo $1$i ":" `echo $1$i | sha256sum`
done