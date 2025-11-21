#!/bin/bash

set -euo pipefail

POLICY_ID=1

curl -v -X DELETE http://service-ricplt-a1mediator-http.ricplt.svc.cluster.local:10000/a1-p/policytypes/${POLICY_ID}