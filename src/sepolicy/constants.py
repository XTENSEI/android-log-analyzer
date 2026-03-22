"""
Constants Module

Defines constants used throughout the sepolicy patcher.
"""

# SELinux policy classes
FILE_CLASSES = [
    "file", "dir", "lnk_file", "chr_file", "blk_file",
    "sock_file", "fifo_file", "socket", "tcp_socket",
    "udp_socket", "rawip_socket", "netlink_socket",
    "packet_socket", "key_socket", "unix_stream_socket",
    "unix_dgram_socket", "binder", "property_service",
    "service_manager", "hwservice_manager", "device",
]

# Common permissions by class
PERMISSIONS = {
    "file": ["read", "write", "execute", "getattr", "setattr", "lock", "append", "unlink", "rename"],
    "dir": ["add_name", "remove_name", "reparent", "search", "rmdir", "create", "getattr", "setattr"],
    "socket": ["bind", "connect", "listen", "accept", "getopt", "setopt", "shutdown"],
    "tcp_socket": ["bind", "connect", "listen", "accept", "newconn", "getopt", "setopt", "shutdown"],
    "service_manager": ["add", "find", "list", "get"],
    "hwservice_manager": ["add", "find", "list", "get"],
    "binder": ["call", "transfer", "inherit"],
}

# Android specific domains
ANDROID_DOMAINS = {
    "system": ["init", "ueventd", "logd", "vold", "netd", "zygote", "surfaceflinger"],
    "server": ["system_server", "statsd", "perfservice", "drm", "keystore", "gatekeeper"],
    "media": ["mediaserver", "audioserver", "cameraserver", "mediacodec", "mediaprovider"],
    "app": ["appdomain", "untrusted_app", "platform_app", "system_app", "priv_app", "shell"],
    "hal": ["hal_bluetooth_default", "hal_wifi_default", "hal_power_default", "hal_fingerprint_default"],
    "vendor": ["vendor_init", "vendor_shell", "vnd_shell"],
}

# SELinux boolean mappings
BOOLEANS = {
    "allow_untrusted_app_execmem": "untrusted_app can execute code from memory",
    "allow_untrusted_app_proc": "untrusted_app can access /proc files",
    "allow_untrusted_app_sysfs": "untrusted_app can access sysfs files",
    "allow_platform_app_execmem": "platform_app can execute code from memory",
    "allow_platform_app_perfmgr": "platform_app can access perfmgr",
    "allow_audioserver_power": "audioserver can access power HAL",
    "domain_auto_trans": "Auto transition to a new domain",
}

# Neverallow rules that should never be generated
NEVERALLOW_RULES = [
    ("untrusted_app.*system_data_file.*write", "Security violation: untrusted_app cannot write to system_data_file"),
    ("platform_app.*app_data_file.*execute", "Security violation: platform_app cannot execute from app_data_file"),
    ("shell.*system_file.*exec", "Security violation: shell cannot execute system files"),
]
