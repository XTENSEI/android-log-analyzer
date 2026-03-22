"""
Type Suggester Module

Provides ML-based pattern recognition for suggesting new SELinux types
based on path patterns.
"""

import re
from typing import List, Dict, Set, Optional
from collections import defaultdict
from .rules import RuleSet


PATH_TYPE_PATTERNS = [
    (r'^/sys/', 'sysfs_type'),
    (r'^/proc/', 'proc_type'),
    (r'^/dev/', 'dev_type'),
    (r'^/data/', 'data_file_type'),
    (r'\.apk$', 'apk_data_file'),
    (r'/vendor/', 'vendor_file_type'),
    (r'/system/', 'system_file_type'),
    (r'/mnt/', 'mnt_type'),
    (r'/cache/', 'cache_file'),
    (r'/persist/', 'persist_file'),
]


BOOLEAN_PATTERNS = [
    (r'untrusted_app.*proc_.*', 'allow_untrusted_app_proc'),
    (r'untrusted_app.*sysfs.*', 'allow_untrusted_app_sysfs'),
    (r'platform_app.*proc_perfmgr', 'allow_platform_app_perfmgr'),
    (r'audioserver.*hal_power_hwservice', 'allow_audioserver_power'),
]


NEVERALLOW_PATTERNS = [
    (r'untrusted_app.*system_data_file:file.*write', 
     'untrusted_app cannot write to system_data_file'),
    (r'platform_app.*app_data_file:file.*execute',
     'platform_app cannot execute from app_data_file'),
]


KNOWN_DOMAINS = {
    'init', 'ueventd', 'logd', 'vold', 'netd', 'zygote', 'system_server',
    'surfaceflinger', 'mediaserver', 'audioserver', 'cameraserver',
    'drm', 'keystore', 'gatekeeper', 'statsd', 'dumpstate', 'shell',
    'appdomain', 'untrusted_app', 'platform_app', 'system_app', 'priv_app',
    'nfc', 'bluetooth', 'radio', 'wifi', 'rild', 'mediacodec', 'mediaprovider',
    'pnpmgr', 'mtk_hal_power', 'mtk_hal_audio', 'system_suspend',
}


KNOWN_TYPES = {
    'app_data_file', 'system_data_file', 'property_data_file', 'apk_data_file',
    'dex2oat_exec', 'dalvikcache_data_file', 'tmpfs', 'proc', 'sysfs',
    'device', 'socket_device', 'input_device', 'graphics_device',
    'vndbinder_device', 'hwservice_manager', 'keystore_msg', 'service_manager_type',
    'sysfs_batteryinfo', 'sysfs_therm', 'proc_perfmgr', 'proc_cgroups',
    'selinuxfs', 'cache_file', 'hal_fingerprint_default', 'hal_power_hwservice'
}


class TypeSuggester:
    """Analyzes rules and suggests new SELinux types based on patterns."""
    
    def __init__(self):
        self.path_counts: Dict[str, int] = defaultdict(int)
        self.pattern_matches: Dict[str, List[str]] = defaultdict(list)
    
    def analyze(self, ruleset: RuleSet) -> None:
        """Analyze a rule set for path patterns."""
        for src, tgt, cls, perms in ruleset.get_all_rules():
            for perm in perms:
                metadata = ruleset.get_metadata(src, tgt, cls, perm)
                for raw, ts in metadata:
                    from .parser import parse_avc_line
                    avc = parse_avc_line(raw)
                    if avc and avc.get('path'):
                        path = avc['path']
                        self.path_counts[path] += 1
                        for pattern, suggested_type in PATH_TYPE_PATTERNS:
                            if re.search(pattern, path):
                                self.pattern_matches[suggested_type].append(path)
    
    def suggest_new_types(self, threshold: int = 3) -> List[str]:
        """Get suggestions for new type definitions."""
        suggestions = []
        for suggested_type, paths in self.pattern_matches.items():
            unique_paths = set(paths)
            if len(unique_paths) >= threshold:
                suggestions.append(
                    f"Consider defining type '{suggested_type}' for paths like:\n"
                    + "\n".join(f"  {p}" for p in list(unique_paths)[:3])
                )
        return suggestions
    
    def suggest_type_declaration(self, type_name: str) -> Optional[str]:
        """Suggest a type declaration based on the type name."""
        if type_name in KNOWN_TYPES:
            return None
        
        if '_file' in type_name or '_data' in type_name or '_dir' in type_name:
            return f"type {type_name}, file_type, data_file_type;"
        elif 'device' in type_name:
            return f"type {type_name}, dev_type;"
        elif '_exec' in type_name:
            return f"type {type_name}, exec_type;"
        else:
            return f"type {type_name}, domain;  # FIXME: adjust attributes"
    
    def suggest_attribute(self, domain: str) -> Optional[str]:
        """Suggest SELinux attributes for a domain."""
        if domain in KNOWN_DOMAINS:
            return None
        if domain.endswith('_app'):
            return f"# {domain} might need 'appdomain' attribute"
        if domain.endswith('_service'):
            return f"# {domain} might need 'service_manager_type' attribute"
        return f"# {domain} is unknown; consider adding proper domain declaration"
    
    def suggest_boolean(self, rule_str: str) -> Optional[str]:
        """Suggest SELinux booleans based on rule patterns."""
        for pattern, boolean in BOOLEAN_PATTERNS:
            if re.search(pattern, rule_str):
                return boolean
        return None
    
    def check_neverallow(self, rule_str: str) -> Optional[str]:
        """Check for potential neverallow violations."""
        for pattern, desc in NEVERALLOW_PATTERNS:
            if re.search(pattern, rule_str):
                return desc
        return None


def suggest_type_for_path(path: str) -> Optional[str]:
    """Convenience function to suggest a type for a given path."""
    for pattern, suggested_type in PATH_TYPE_PATTERNS:
        if re.search(pattern, path):
            return suggested_type
    return None
