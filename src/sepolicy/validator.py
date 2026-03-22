"""
Validation Module

Validates SELinux rules for correctness.
"""

import re
from typing import List, Tuple
from .rules import RuleSet


class RuleValidator:
    """Validates SELinux rules."""
    
    VALID_CLASSES = {
        "file", "dir", "lnk_file", "chr_file", "blk_file",
        "sock_file", "fifo_file", "socket", "tcp_socket",
        "udp_socket", "rawip_socket", "netlink_socket",
        "packet_socket", "key_socket", "binder", 
        "property_service", "service_manager",
        "hwservice_manager", "device",
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_ruleset(self, ruleset: RuleSet) -> bool:
        """Validate all rules in a rule set."""
        self.errors = []
        self.warnings = []
        
        for src, tgt, cls, perms in ruleset.get_all_rules():
            self._validate_rule(src, tgt, cls, perms)
        
        return len(self.errors) == 0
    
    def _validate_rule(self, src: str, tgt: str, cls: str, perms: List[str]) -> None:
        """Validate a single rule."""
        if not src:
            self.errors.append("Source domain cannot be empty")
        if not tgt:
            self.errors.append("Target type cannot be empty")
        if not cls:
            self.errors.append("Class cannot be empty")
        if cls not in self.VALID_CLASSES:
            self.warnings.append(f"Unknown class: {cls}")
        if not perms:
            self.errors.append("No permissions specified")


def validate_rules(ruleset: RuleSet) -> Tuple[bool, List[str]]:
    """Validate rules and return (is_valid, errors)."""
    validator = RuleValidator()
    is_valid = validator.validate_ruleset(ruleset)
    return is_valid, validator.errors
