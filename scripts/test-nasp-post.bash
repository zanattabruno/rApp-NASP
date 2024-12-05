curl -X POST http://localhost:5001/create_slice_policy \
     -H "Content-Type: application/json" \
     -d '{
  "name": "ewtwet",
  "description": {
    "N3GPP Support": false,
    "Slice Attributes": {
      "Accuracy": 1e-07,
      "DN": 1,
      "MMTel": true,
      "Maximum number of PDU sessions": 1000,
      "Maximum number of UEs": 100000,
      "N3GPP Support": true,
      "SSC": 1,
      "SSQ": {
        "Guaranteed Flow Bit Rate - Downlink": 100000,
        "Guaranteed Flow Bit Rate - Uplink": 100000,
        "Max Flow Bit Rate - Downlink": 100000000,
        "Max Flow Bit Rate - Uplink": 100000,
        "Maximum Data Burts Volume": 0.001,
        "Maximum Packet Loss Rate": 100000,
        "Packet Delay Budget": 0.00012,
        "Packet Error Rate": 1e-07,
        "Priority Level": 1
      },
      "Shared": false,
      "Supported Data Network": "internet",
      "Supported device velocity": 10,
      "Synchronicity": "Between BS and UE",
      "UE density": 10000,
      "availability": 1,
      "exposed": true,
      "shared": true
    },
    "resource_description": {
      "core": {
        "nfs": [
          {
            "config": {
              "plmnSupportList": [
                {
                  "plmnId": {
                    "mcc": 208,
                    "mnc": 93
                  },
                  "snssaiList": [
                    {
                      "sd": 4227,
                      "sst": 1
                    },
                    {
                      "sd": 112233,
                      "sst": 1
                    }
                  ]
                }
              ],
              "supportDnnList": [
                "internet"
              ]
            },
            "name": "amf",
            "node": [
              "new_york"
            ]
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
            "config": {
              "amfConfigs": [
                {
                  "address": "127.0.0.1",
                  "port": 38412
                }
              ],
              "gtpIp": "127.0.0.1",
              "idLength": 32,
              "ignoreStreamIds": true,
              "linkIp": "127.0.0.1",
              "mcc": "208",
              "mnc": "93",
              "nci": "0x000000010",
              "ngapIp": "127.0.0.1",
              "slices": [
                {
                  "sd": 66051,
                  "sst": 1
                }
              ],
              "tac": 1
            },
            "name": "ueransim",
            "node": [],
            "replicas": 2,
            "type": "gnb"
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
    },
    "resources": "custom",
    "type": "custom"
  },
  "S_NSSAI": "1274464"
}'