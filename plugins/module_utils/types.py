from typing import Literal

StatePresentAbsent = Literal["present", "absent"]
StateEnabledDisabled = Literal["enabled", "disabled"]
OVHPolicies = Literal["deny", "admin", "readOnly", "readWrite"]
OVHVolumeType = Literal["classic", "high-speed", "high-speed-gen2"]
OVHBootType = Literal["harddisk", "rescue-customer", "ipxe-shell", "poweroff"]
OVHNASProtocolType = Literal["NFS", "CIFS", "NFS_CIFS"]
OVHRecordType = Literal[
    "A",
    "AAAA",
    "CAA",
    "CNAME",
    "DKIM",
    "DMARC",
    "DNAME",
    "LOC",
    "MX",
    "NAPTR",
    "NS",
    "PTR",
    "SPF",
    "SRV",
    "SSHFP",
    "TLSA",
    "TXT",
]
