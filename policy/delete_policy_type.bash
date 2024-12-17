#!/bin/bash

# Define the policy ID to delete
POLICY_ID=1

# Execute the curl command to delete the policy
#curl -v -X DELETE http://service-ricplt-a1mediator-http.ricplt.svc.cluster.local:10000/a1-p/policytypes/${POLICY_ID}

curl -v -X DELETE http://10.101.111.161:10000/a1-p/policytypes/${POLICY_ID}