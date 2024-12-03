#!/bin/bash

# Fetch all namespaces starting with 'ns-'
namespaces=$(kubectl get namespaces --no-headers -o custom-columns=:metadata.name | grep '^ns-')

# Check if any namespaces were found
if [ -z "$namespaces" ]; then
    echo "No namespaces starting with 'ns-' found."
    exit 0
fi

# Loop through each namespace and delete it in parallel
for ns in $namespaces; do
    echo "Deleting namespace: $ns"
    kubectl delete namespace "$ns" &
done

# Wait for all background processes to complete
wait
echo "All namespaces have been deleted."