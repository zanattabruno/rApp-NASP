#!/bin/bash


curl -v -X PUT "http://10.111.85.136:9090/a1-policy/v2/policies" \
-H "Content-Type: application/json" \
-d @SliceInstancev4.json
