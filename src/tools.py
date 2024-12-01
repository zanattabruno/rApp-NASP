import json

def extract_flow_bit_rate(json_data):
    downlink = None
    uplink = None

    def search(data):
        nonlocal downlink, uplink
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "Guaranteed Flow Bit Rate - Downlink":
                    downlink = value
                elif key == "Guaranteed Flow Bit Rate - Uplink":
                    uplink = value
                else:
                    search(value)
        elif isinstance(data, list):
            for item in data:
                search(item)

    search(json_data)
    return downlink, uplink

