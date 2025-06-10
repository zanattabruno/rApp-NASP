curl -X POST http://localhost:5001/create_slice_policy \
     -H "Content-Type: application/json" \
     -d '{
  "name": "oi\u00e7\u00e7o\u00e7i",
  "description": {
    "type": "custom",
    "resources": "custom",
    "N3GPP Support": false,
    "Slice Attributes": {
      "availability": 1,
      "MMTel": true,
      "N3GPP Support": true,
      "SSC": 1,
      "DN": 1,
      "Supported Data Network": "internet",
      "SSQ": {
        "Priority Level": 1,
        "Packet Delay Budget": 0.00012,
        "Packet Error Rate": 1e-07,
        "Maximum Data Burts Volume": 0.001,
        "Guaranteed Flow Bit Rate - Downlink": 100000,
        "Guaranteed Flow Bit Rate - Uplink": 100000,
        "Max Flow Bit Rate - Downlink": 100000,
        "Max Flow Bit Rate - Uplink": 100000,
        "Maximum Packet Loss Rate": 100000
      },
      "Supported device velocity": 10,
      "Synchronicity": "Between BS and UE",
      "Accuracy": 1e-07,
      "Shared": false,
      "UE density": 10000,
      "Maximum number of UEs": 100000,
      "Maximum number of PDU sessions": 1000,
      "exposed": true,
      "shared": true
    },
    "resource_description": {
      "core": {
        "nfs": [
          {
            "name": "amf",
            "node": [
              "new_york"
            ],
            "config": {
              "plmnSupportList": [
                {
                  "plmnId": {
                    "mcc": 208,
                    "mnc": 93
                  },
                  "snssaiList": [
                    {
                      "sst": 1,
                      "sd": 112233
                    }
                  ]
                }
              ],
              "supportDnnList": [
                "internet"
              ]
            }
          },
          {
            "name": "nrf"
          },
          {
            "name": "ausf"
          },
          {
            "name": "nssf"
          },
          {
            "name": "pcf"
          },
          {
            "name": "udm"
          },
          {
            "name": "udr"
          },
          {
            "name": "smf"
          },
          {
            "name": "upf"
          }
        ]
      },
      "ran": {
        "nfs": [
          {
            "name": "ueransim",
            "type": "gnb",
            "replicas": 2,
            "node": [],
            "config": {
              "mcc": "208",
              "mnc": "93",
              "nci": 411,
              "idLength": 32,
              "tac": 1,
              "linkIp": "127.0.0.1",
              "ngapIp": "127.0.0.1",
              "gtpIp": "127.0.0.1",
              "amfConfigs": [
                {
                  "address": "127.0.0.1",
                  "port": 38412
                }
              ],
              "slices": [
                {
                  "sst": 1,
                  "sd": 112233
                }
              ],
              "ignoreStreamIds": true
            }
          }
        ]
      },
      "tn": {
        "routes": [
          {
            "name": "backhaul"
          }
        ]
      }
    }
  },
  "S_NSSAI": "1274484",
  "imsi_range": "208950000000001-208950000000003",
  "imsi_data": {
    "start": "208950000000001",
    "end": "208950000000003",
    "count": 3,
    "mcc": "208",
    "mnc": "95",
    "range": "208950000000001-208950000000003",
    "valid": true
  }
}'