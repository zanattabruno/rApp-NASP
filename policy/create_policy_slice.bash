curl http://localhost:5000/create_slice_policy -X POST -H "Content-Type: application/json" -d '[
  {
    "mcc": "001",
    "mnc": "01",
    "e2nodeid": "node123",
    "RRMPolicyRatioList": [
      {"plmnid": "00101", "sst": 1, "sd": 1, "minPRB": 10, "maxPRB": 20}
    ]
  }
]'