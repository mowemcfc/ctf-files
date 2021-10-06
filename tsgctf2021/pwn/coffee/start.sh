#!/bin/sh

timeout --foreground -s 9 60s stdbuf -i0 -o0 -e0 ./coffee
