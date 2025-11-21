#!/bin/bash

# Resolve payload path relative to this script so it works from any directory.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_FILE="$SCRIPT_DIR/SliceInstancev5.json"

if [[ ! -f "$PAYLOAD_FILE" ]]; then
	echo "Payload file not found: $PAYLOAD_FILE" >&2
	exit 1
fi

curl -v -X PUT "http://nonrtricgateway.nonrtric.svc.cluster.local:9090/a1-policy/v2/policies" \
-H "Content-Type: application/json" \
-d @"$PAYLOAD_FILE"
