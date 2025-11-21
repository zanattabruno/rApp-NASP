#!/bin/bash

set -euo pipefail

POLICY_ID=1
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

curl -v -X PUT http://service-ricplt-a1mediator-http.ricplt.svc.cluster.local:10000/a1-p/policytypes/${POLICY_ID} \
-H "Content-Type: application/json" \
-d @"${SCRIPT_DIR}/SliceSchemav5.json"
