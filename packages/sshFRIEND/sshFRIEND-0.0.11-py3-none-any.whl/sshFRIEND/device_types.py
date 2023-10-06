

SSH_MAPPER_DICT = {
    "aruba_os": {
        "cmd": "show version",
        "search_patterns": [r"ArubaOS"]
    },
    "alcatel_aos": {
        "cmd": "show system",
        "search_patterns": [r"Alcatel-Lucent"]
    },
    "alcatel_sros": {
        "cmd": "show version",
        "search_patterns": ["Nokia", "Alcatel"]
    },
    "cisco_ios": {
        "cmd": "show version",
        "search_patterns": [
            "Cisco IOS Software",
            "Cisco Internetwork Operating System Software",
        ]
    },
    "cisco_nxos": {
        "cmd": "show version",
        "search_patterns": [r"Cisco Nexus Operating System", r"NX-OS"],
    },
    "cisco_xr": {
        "cmd": "show version",
        "search_patterns": [r"Cisco IOS XR"],
    },
    "hp_comware": {
        "cmd": "display version",
        "search_patterns": ["HPE Comware", "HP Comware"],
    },
    "juniper_junos": {
        "cmd": "show version",
        "search_patterns": [
            r"JUNOS Software Release",
            r"JUNOS .+ Software",
            r"JUNOS OS Kernel",
            r"JUNOS Base Version",
        ],
    },
}