"""
Configuration Module

Handles configuration loading and management for the sepolicy patcher.
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, field


DEFAULT_CONFIG = {
    "merge_permissions": False,
    "output_format": "cil",
    "exclude_domains": [],
    "include_domains": [],
    "filter_perms": [],
    "suggest_types": True,
    "track_trends": False,
    "capture_timeout": 60,
    "verbose": False,
    "adb_sources": [
        "dmesg",
        "logcat_events",
        "logcat_crash",
        "logcat_radio",
        "logcat_main",
        "kmsg",
    ],
    "known_domains": [
        "init", "ueventd", "logd", "vold", "netd", "zygote",
        "system_server", "surfaceflinger", "mediaserver",
        "audioserver", "cameraserver", "shell", "untrusted_app",
        "platform_app", "system_app", "priv_app"
    ],
    "path_patterns": {
        "^/sys/": "sysfs_type",
        "^/proc/": "proc_type",
        "^/dev/": "dev_type",
        "^/data/": "data_file_type",
        "\\.apk$": "apk_data_file",
        "/vendor/": "vendor_file_type",
        "/system/": "system_file_type",
    }
}


@dataclass
class Config:
    """Configuration container for sepolicy patcher."""
    merge_permissions: bool = False
    output_format: str = "cil"
    exclude_domains: List[str] = field(default_factory=list)
    include_domains: List[str] = field(default_factory=list)
    filter_perms: List[str] = field(default_factory=list)
    suggest_types: bool = True
    track_trends: bool = False
    capture_timeout: int = 60
    verbose: bool = False
    adb_sources: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Config':
        """Create Config from a dictionary."""
        return cls(
            merge_permissions=data.get("merge_permissions", False),
            output_format=data.get("output_format", "cil"),
            exclude_domains=data.get("exclude_domains", []),
            include_domains=data.get("include_domains", []),
            filter_perms=data.get("filter_perms", []),
            suggest_types=data.get("suggest_types", True),
            track_trends=data.get("track_trends", False),
            capture_timeout=data.get("capture_timeout", 60),
            verbose=data.get("verbose", False),
            adb_sources=data.get("adb_sources", []),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary."""
        return {
            "merge_permissions": self.merge_permissions,
            "output_format": self.output_format,
            "exclude_domains": self.exclude_domains,
            "include_domains": self.include_domains,
            "filter_perms": self.filter_perms,
            "suggest_types": self.suggest_types,
            "track_trends": self.track_trends,
            "capture_timeout": self.capture_timeout,
            "verbose": self.verbose,
            "adb_sources": self.adb_sources,
        }


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file or use defaults."""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            data = json.load(f)
        return Config.from_dict(data)
    return Config.from_dict(DEFAULT_CONFIG)


def save_config(config: Config, config_path: str) -> None:
    """Save configuration to file."""
    with open(config_path, 'w') as f:
        json.dump(config.to_dict(), f, indent=2)


def get_config_path() -> str:
    """Get the default config file path."""
    return os.path.expanduser("~/.config/sepolicy_patcher/config.json")
