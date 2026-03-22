"""
Rule Analysis Module

Analyzes SELinux rules for potential issues and improvements.
"""

import re
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from .rules import RuleSet


@dataclass
class AnalysisResult:
    """Result of rule analysis."""
    warnings: List[str]
    suggestions: List[str]
    security_issues: List[str]


class RuleAnalyzer:
    """Analyzes SELinux rules for potential issues."""
    
    def __init__(self):
        self.warnings = []
        self.suggestions = []
        self.issues = []
    
    def analyze_rules(self, ruleset: RuleSet) -> AnalysisResult:
        """Analyze all rules and return issues."""
        self.warnings = []
        self.suggestions = []
        self.issues = []
        
        for src, tgt, cls, perms in ruleset.get_all_rules():
            self._check_permissions(src, tgt, cls, perms)
            self._check_domains(src, tgt)
            self._check_paths(tgt)
        
        return AnalysisResult(
            warnings=self.warnings,
            suggestions=self.suggestions,
            security_issues=self.issues,
        )
    
    def _check_permissions(self, src: str, tgt: str, cls: str, perms: List[str]) -> None:
        """Check for dangerous permission combinations."""
        dangerous = {
            'exec': ['execute', 'execmod', 'execmem'],
            'write': ['write', 'add_name', 'remove_name'],
        }
        
        for category, perms_list in dangerous.items():
            if any(p in perms for p in perms_list):
                self.warnings.append(
                    f"{src} -> {tgt}:{cls} has dangerous {category} permission"
                )
    
    def _check_domains(self, src: str, tgt: str) -> None:
        """Check domain-related issues."""
        if src == 'untrusted_app' and 'system' in tgt:
            self.issues.append(
                f"untrusted_app accessing system type {tgt} may be security issue"
            )
    
    def _check_paths(self, tgt: str) -> None:
        """Check target type naming."""
        if tgt.startswith('/'):
            self.warnings.append(f"Target {tgt} looks like a path, not a type")


def analyze_rules(ruleset: RuleSet) -> AnalysisResult:
    """Convenience function to analyze rules."""
    analyzer = RuleAnalyzer()
    return analyzer.analyze_rules(ruleset)
