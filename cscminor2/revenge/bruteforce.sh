#!/bin/bash


STR="http://hello-world.ctf.fifthdoma.in:2000/"
a="a"
for i in {1..1000}
do
	STR=$STR$a
	wget $STR -O ->> output.txt 
done


