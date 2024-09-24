#!/bin/bash

POLICY_ID=1


curl -v -X PUT http://10.101.111.161:10000/a1-p/policytypes/${POLICY_ID} \
-H "Content-Type: application/json" \
-d @SliceSchema.json
