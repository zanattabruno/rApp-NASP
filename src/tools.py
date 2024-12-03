import json

def create_rrm_policy(input_json):
    def remove_duplicates_from_rrm_policy(data):
        """
        Removes duplicate entries from the 'RRMPolicyRatioList' in the provided data dictionary.
        """
        if "RRMPolicyRatioList" in data:
            dict_list = data["RRMPolicyRatioList"]
            seen = set()
            new_list = []
            for d in dict_list:
                s = json.dumps(d, sort_keys=True)
                if s not in seen:
                    seen.add(s)
                    new_list.append(d)
            data["RRMPolicyRatioList"] = new_list
        else:
            print("Key 'RRMPolicyRatioList' not found in data.")
        return data

    # Access 'resource_description' directly from input_json
    resource_description = input_json.get("resource_description", {})

    # Extract plmnId and snssaiList from resource_description -> core -> nfs where name == "amf"
    nfs_core = resource_description.get("core", {}).get("nfs", [])
    for nf in nfs_core:
        if nf.get("name") == "amf":
            amf_config = nf.get("config", {})
            amf_plmnSupportList = amf_config.get("plmnSupportList", [])
            break
    else:
        amf_plmnSupportList = []

    # Extract mcc, mnc, nci, slices from resource_description -> ran -> nfs where name == "ueransim"
    nfs_ran = resource_description.get("ran", {}).get("nfs", [])
    for nf in nfs_ran:
        if nf.get("name") == "ueransim":
            ran_config = nf.get("config", {})
            break
    else:
        ran_config = {}

    ran_mcc = ran_config.get("mcc", "")
    ran_mnc = ran_config.get("mnc", "")
    ran_nci = ran_config.get("nci", "")
    ran_slices = ran_config.get("slices", [])

    # Get the Guaranteed Flow Bit Rate - Downlink and Max Flow Bit Rate - Downlink
    ssq = input_json.get("Slice Attributes", {}).get("SSQ", {})
    guaranteed_flow_bit_rate_downlink = ssq.get("Guaranteed Flow Bit Rate - Downlink", 0)
    max_flow_bit_rate_downlink = ssq.get("Max Flow Bit Rate - Downlink", 0)

    # Use function toPRB to calculate minPRB and maxPRB
    def toPRB(flow_bit_rate):
        # Placeholder function; replace with your actual implementation
        if flow_bit_rate == guaranteed_flow_bit_rate_downlink:
            return 50  # Example value
        elif flow_bit_rate == max_flow_bit_rate_downlink:
            return 70  # Example value
        else:
            return 0  # Default value if flow bit rate is unknown

    rrm_policy_ratio_list = []

    # First, process amf plmnSupportList
    for plmnSupport in amf_plmnSupportList:
        plmnId = plmnSupport.get("plmnId", {})
        snssaiList = plmnSupport.get("snssaiList", [])
        for snssai in snssaiList:
            sst = snssai.get("sst")
            sd = snssai.get("sd")
            entry = {
                "plmnId": {
                    "mcc": str(plmnId.get("mcc", "")),
                    "mnc": str(plmnId.get("mnc", ""))
                },
                "nci": ran_nci,
                "sst": sst,
                "sd": sd,
                "minPRB": toPRB(guaranteed_flow_bit_rate_downlink),
                "maxPRB": toPRB(max_flow_bit_rate_downlink)
            }
            rrm_policy_ratio_list.append(entry)

    # Then, process ran slices
    for slice_item in ran_slices:
        sst = slice_item.get("sst")
        sd = slice_item.get("sd")
        entry = {
            "plmnId": {
                "mcc": ran_mcc,
                "mnc": ran_mnc
            },
            "nci": ran_nci,
            "sst": sst,
            "sd": sd,
            "minPRB": toPRB(guaranteed_flow_bit_rate_downlink),
            "maxPRB": toPRB(max_flow_bit_rate_downlink)
        }
        rrm_policy_ratio_list.append(entry)

    result = {
        "RRMPolicyRatioList": rrm_policy_ratio_list
    }
    return remove_duplicates_from_rrm_policy(result)

from dataclasses import dataclass
from math import ceil

@dataclass
class MCS:
    modulation_order: int
    target_code_rate: int
    spectral_efficiency: float

@dataclass
class Slot:
    downlink: float
    uplink: float
    flexible: float

# 3GPP TS 38.214 version 15.3.0 Release 15
# Table 5.1.3.1
mcs_tables_5_1_3_1: [[MCS]] = [[
    MCS(2, 120, 0.2344), # 0
    MCS(2, 157, 0.3066), # 1
    MCS(2, 193, 0.3770), # 2
    MCS(2, 251, 0.4902), # 3
    MCS(2, 308, 0.6016), # 4
    MCS(2, 379, 0.7402), # 5
    MCS(2, 449, 0.8770), # 6
    MCS(2, 526, 1.0273), # 7
    MCS(2, 602, 1.1758), # 8
    MCS(2, 679, 1.3262), # 9
    MCS(4, 340, 1.3281), # 10
    MCS(4, 378, 1.4766), # 11
    MCS(4, 434, 1.6953), # 12
    MCS(4, 490, 1.9141), # 13
    MCS(4, 553, 2.1602), # 14
    MCS(4, 616, 2.4063), # 15
    MCS(4, 658, 2.5703), # 16
    MCS(6, 438, 2.5664), # 17
    MCS(6, 466, 2.7305), # 18
    MCS(6, 517, 3.0293), # 19
    MCS(6, 567, 3.3223), # 20
    MCS(6, 616, 3.6094), # 21
    MCS(6, 666, 3.9023), # 22
    MCS(6, 719, 4.2129), # 23
    MCS(6, 772, 4.5234), # 24
    MCS(6, 822, 4.8164), # 25
    MCS(6, 873, 5.1152), # 26
    MCS(6, 910, 5.3320), # 27
    MCS(6, 948, 5.5547), # 28
    MCS(2, 0, 0.0), # 29 (reserved)
    MCS(4, 0, 0.0), # 30 (reserved)
    MCS(6, 0, 0.0), # 31 (reserved)
],
[
    MCS(2, 120, 0.2344), #0
    MCS(2, 193, 0.3770), #1
    MCS(2, 308, 0.6016), #2
    MCS(2, 449, 0.8770), #3
    MCS(2, 602, 1.1758), #4
    MCS(4, 378, 1.4766), #5
    MCS(4, 434, 1.6953), #6
    MCS(4, 490, 1.9141), #7
    MCS(4, 553, 2.1602), #8
    MCS(4, 616, 2.4063), #9
    MCS(4, 658, 2.5703), #10
    MCS(6, 466, 2.7305), #11
    MCS(6, 517, 3.0293), #12
    MCS(6, 567, 3.3223), #13
    MCS(6, 616, 3.6094), #14
    MCS(6, 666, 3.9023), #15
    MCS(6, 719, 4.2129), #16
    MCS(6, 772, 4.5234), #17
    MCS(6, 822, 4.8164), #18
    MCS(6, 873, 5.1152), #19
    MCS(8, 682.5, 5.3320), #20
    MCS(8, 711, 5.5547), #21
    MCS(8, 754, 5.8906), #22
    MCS(8, 797, 6.2266), #23
    MCS(8, 841, 6.5703), #24
    MCS(8, 885, 6.9141), #25
    MCS(8, 916.5, 7.1602), #26
    MCS(8, 948, 7.4063), #27
    MCS(2, 0, 0.0), #28 (reserved)
    MCS(4, 0, 0.0), #29 (reserved)
    MCS(6, 0, 0.0), #30 (reserved)
    MCS(8, 0, 0.0), #31  (reserved)
],
[
    MCS(2, 30, 0.0586), #0
    MCS(2, 40, 0.0781), #1
    MCS(2, 50, 0.0977), #2
    MCS(2, 64, 0.1250), #3
    MCS(2, 78, 0.1523), #4
    MCS(2, 99, 0.1934), #5
    MCS(2, 120, 0.2344), #6
    MCS(2, 157, 0.3066), #7
    MCS(2, 193, 0.3770), #8
    MCS(2, 251, 0.4902), #9
    MCS(2, 308, 0.6016), #10
    MCS(2, 379, 0.7402), #11
    MCS(2, 449, 0.8770), #12
    MCS(2, 526, 1.0273), #13
    MCS(2, 602, 1.1758), #14
    MCS(4, 340, 1.3281), #15
    MCS(4, 378, 1.4766), #16
    MCS(4, 434, 1.6953), #17
    MCS(4, 490, 1.9141), #18
    MCS(4, 553, 2.1602), #19
    MCS(4, 616, 2.4063), #20
    MCS(6, 438, 2.5664), #21
    MCS(6, 466, 2.7305), #22
    MCS(6, 517, 3.0293), #23
    MCS(6, 567, 3.3223), #24
    MCS(6, 616, 3.6094), #25
    MCS(6, 666, 3.9023), #26
    MCS(6, 719, 4.2129), #27
    MCS(6, 772, 4.5234), #28
    MCS(2, 0, 0.0), #29 (reserved)
    MCS(4, 0, 0.0), #30 (reserved)
    MCS(6, 0, 0.0), #31 (reserved)
],
[
    MCS(2, 120, 0.2344), #0
    MCS(2, 193, 0.3770), #1
    MCS(2, 449, 0.8770), #2
    MCS(4, 378, 1.4766), #3
    MCS(4, 490, 1.9141), #4
    MCS(4, 616, 2.4063), #5
    MCS(6, 466, 2.7305), #6
    MCS(6, 517, 3.0293), #7
    MCS(6, 567, 3.3223), #8
    MCS(6, 616, 3.6094), #9
    MCS(6, 666, 3.9023), #10
    MCS(6, 719, 4.2129), #11
    MCS(6, 772, 4.5234), #12
    MCS(6, 822, 4.8164), #13
    MCS(6, 873, 5.1152), #14
    MCS(8, 682.5, 5.3320), #15
    MCS(8, 711, 5.5547), #16
    MCS(8, 754, 5.8906), #17
    MCS(8, 797, 6.2266), #18
    MCS(8, 841, 6.5703), #19
    MCS(8, 885, 6.9141), #20
    MCS(8, 916.5, 7.1602), #21
    MCS(8, 948, 7.4063), #22
    MCS(10, 805.5, 7.8662), #23
    MCS(10, 853, 8.3301), #24
    MCS(10, 900.5, 8.7939), #25
    MCS(10, 948, 9.2578), #26
    MCS(2, 0, 0.0), #27 (reserved)
    MCS(4, 0, 0.0), #28 (reserved)
    MCS(6, 0, 0.0), #29 (reserved)
    MCS(8, 0, 0.0), #30 (reserved)
    MCS(10, 0, 0.0), #31 (reserved)
],
]

# 3GPP TS 38.101-1 version 18.6.0 Release 18
# Table 5.3.2
# maps a bandwidth (in MHz) to an array with the max number of PRBs per numerology
bw: dict[int, [int]] = {
    3:   [15,  0,   0],
    5:   [25,  11,  0],
    10:  [52,  24,  11],
    15:  [79,  38,  18],
    20:  [106, 51,  24],
    25:  [133, 65,  31],
    30:  [160, 78,  38],
    35:  [188, 92,  44],
    40:  [216, 106, 51],
    45:  [242, 119, 58],
    50:  [270, 133, 65],
    60:  [0,   162, 79],
    70:  [0,   189, 93],
    80:  [0,   217, 107],
    90:  [0,   245, 121],
    100: [0,   273, 135],
}

# 3GPP TS 38.213 version 18.4.0 Release 18
# Table 11.1.1-1
symbol_table: [Slot] = []

def populate_symbol_table() -> None:
    symbols: [str] = [
        "DDDDDDDDDDDDDD", #0
        "UUUUUUUUUUUUUU", #1
        "FFFFFFFFFFFFFF", #2
        "DDDDDDDDDDDDDF", #3
        "DDDDDDDDDDDDFF", #4
        "DDDDDDDDDDDFFF", #5
        "DDDDDDDDDDFFFF", #6
        "DDDDDDDDDFFFFF", #7
        "FFFFFFFFFFFFFU", #8
        "FFFFFFFFFFFFUU", #9
        "FUUUUUUUUUUUUU", #10
        "FFUUUUUUUUUUUU", #11
        "FFFUUUUUUUUUUU", #12
        "FFFFUUUUUUUUUU", #13
        "FFFFFUUUUUUUUU", #14
        "FFFFFFUUUUUUUU", #15
        "DFFFFFFFFFFFFF", #16
        "DDFFFFFFFFFFFF", #17
        "DDDFFFFFFFFFFF", #18
        "DFFFFFFFFFFFFU", #19
        "DDFFFFFFFFFFFU", #20
        "DDDFFFFFFFFFFU", #21
        "DFFFFFFFFFFFUU", #22
        "DDFFFFFFFFFFUU", #23
        "DDDFFFFFFFFFUU", #24
        "DFFFFFFFFFFUUU", #25
        "DDFFFFFFFFFUUU", #26
        "DDDFFFFFFFFUUU", #27
        "DDDDDDDDDDDDFU", #28
        "DDDDDDDDDDDFFU", #29
        "DDDDDDDDDDFFFU", #30
        "DDDDDDDDDDDFUU", #31
        "DDDDDDDDDDFFUU", #32
        "DDDDDDDDDFFFUU", #33
        "DFUUUUUUUUUUUU", #34
        "DDFUUUUUUUUUUU", #35
        "DDDFUUUUUUUUUU", #36
        "DFFUUUUUUUUUUU", #37
        "DDFFUUUUUUUUUU", #38
        "DDDFFUUUUUUUUU", #39
        "DFFFUUUUUUUUUU", #40
        "DDFFFUUUUUUUUU", #41
        "DDDFFFUUUUUUUU", #42
        "DDDDDDDDDFFFFU", #43
        "DDDDDDFFFFFFUU", #44
        "DDDDDDFFUUUUUU", #45
        "DDDDDFUDDDDDFU", #46
        "DDFUUUUDDFUUUU", #47
        "DFUUUUUDFUUUUU", #48
        "DDDDFFUDDDDFFU", #49
        "DDFFUUUDDFFUUU", #50
        "DFFUUUUDFFUUUU", #51
        "DFFFFFUDFFFFFU", #52
        "DDFFFFUDDFFFFU", #53
        "FFFFFFFDDDDDDD", #54
        "DDFFFUUUDDDDDD", #55
    ]
    for s in symbols:
        symbol_table.append(Slot(s.count('D') / 14, s.count('U') / 14, s.count('F') / 14))
populate_symbol_table()

# Computes the maximum speed (in bps) for a given cell
def to_bps(
        is_uplink: bool,
        mcs: int, 
        numerology: int, 
        bandwidth: int, 
        scaling_factor: float = 1.0, 
        mimo: int = 1, 
        symbol_format: int = 5, 
        is_tdd: bool = True, 
        use_flex_sym: bool = True, 
        mcs_table: int = 0
        ) -> float:
    if is_uplink:
        overhead = 0.08
    else:
        overhead = 0.14
    result = 1.0
    # vlayers
    result *= mimo
    # Qm
    result *= mcs_tables_5_1_3_1[mcs_table][mcs].modulation_order
    # f
    result *= scaling_factor
    # Rmax
    result *= mcs_tables_5_1_3_1[mcs_table][mcs].target_code_rate / 1024
    # T
    result *= 14 * (2**numerology) * (10**3)
    result *= 12
    # Nprb
    result *= bw[bandwidth][numerology]
    # OH
    result *= 1 - overhead
    if is_tdd:
        symbol_ratio: float = 0.0
        if is_uplink:
            symbol_ratio += symbol_table[symbol_format].uplink
        else:
            symbol_ratio += symbol_table[symbol_format].downlink
        if use_flex_sym:
            symbol_ratio += symbol_table[symbol_format].flexible
        result *= symbol_ratio
    return result

# Computes the minimum percentage of PRBs required to achieve a given speed (in
# bps)
def to_prb(
        speed: float, 
        is_uplink: bool, 
        mcs: int, 
        numerology: int, 
        bandwidth: int, 
        scaling_factor: float = 1.0, 
        mimo: int = 1, 
        symbol_format: int = 5, 
        is_tdd: bool = True, 
        use_flex_sym: bool = True, 
        mcs_table: int = 0
        ) -> int:
    total_speed: float = to_bps(is_uplink, mcs, numerology, bandwidth, mimo=mimo, scaling_factor=scaling_factor, symbol_format=symbol_format, is_tdd=is_tdd, use_flex_sym=use_flex_sym, mcs_table=mcs_table)
    if total_speed == 0.0:
        return 0
    return ceil((speed/total_speed) * 100.0)

# Computes the latency (in miliseconds) for each slot
def latency(
    numerology: int, 
    ) -> float:
    return 1 / (2**numerology)
