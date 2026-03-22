"""
Rule Management Module

Handles storage, merging, filtering, and retrieval of SELinux rules.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Tuple, Any
from collections import defaultdict
import threading
import time


@dataclass
class Rule:
    """Represents a single SELinux allow rule."""
    source: str
    target: str
    tclass: str
    permissions: Set[str]
    metadata: List[Tuple[str, float]] = field(default_factory=list)
    
    def to_tuple(self) -> Tuple[str, str, str, List[str]]:
        return (self.source, self.target, self.tclass, sorted(self.permissions))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'target': self.target,
            'class': self.tclass,
            'permissions': sorted(self.permissions),
        }


class RuleSet:
    """
    Manages a collection of SELinux rules with support for:
    - Permission merging
    - Filtering by source/target/permissions
    - Thread-safe operations
    - Metadata tracking
    """
    
    def __init__(self, merge_permissions: bool = False):
        self.merge_permissions = merge_permissions
        self._merged_rules: Dict[str, Dict[str, Dict[str, Set[str]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(set))
        )
        self._unmerged_rules: Set[Tuple[str, str, str, str]] = set()
        self._metadata: Dict[Tuple[str, str, str, str], List[Tuple[str, float]]] = defaultdict(list)
        self._lock = threading.Lock()
    
    def add_denial(self, denial: Dict[str, Any]) -> None:
        """Add an AVC denial to the rule set."""
        src = denial.get('source') or denial.get('src')
        tgt = denial.get('target') or denial.get('tgt')
        cls = denial.get('class') or denial.get('tclass')
        perms = denial.get('permissions') or denial.get('perms', set())
        raw = denial.get('raw', '')
        ts = denial.get('timestamp', time.time())
        
        if not all([src, tgt, cls, perms]):
            return
        
        with self._lock:
            if self.merge_permissions:
                self._merged_rules[src][tgt][cls].update(perms)
                for perm in perms:
                    key = (src, tgt, cls, perm)
                    if len(self._metadata[key]) < 3:
                        self._metadata[key].append((raw, ts))
            else:
                for perm in perms:
                    key = (src, tgt, cls, perm)
                    self._unmerged_rules.add(key)
                    if len(self._metadata[key]) < 3:
                        self._metadata[key].append((raw, ts))
    
    def get_all_rules(self) -> List[Tuple[str, str, str, List[str]]]:
        """Get all rules as a list of tuples."""
        if self.merge_permissions:
            rules = []
            for src in self._merged_rules:
                for tgt in self._merged_rules[src]:
                    for cls, perms in self._merged_rules[src][tgt].items():
                        rules.append((src, tgt, cls, sorted(perms)))
            return rules
        else:
            return [
                (src, tgt, cls, [perm])
                for (src, tgt, cls, perm) in sorted(self._unmerged_rules)
            ]
    
    def get_rule_objects(self) -> List[Rule]:
        """Get all rules as Rule objects."""
        rules = []
        for src, tgt, cls, perms in self.get_all_rules():
            meta = self._get_metadata_internal(src, tgt, cls)
            rules.append(Rule(
                source=src,
                target=tgt,
                tclass=cls,
                permissions=perms,
                metadata=meta,
            ))
        return rules
    
    def _get_metadata_internal(self, src: str, tgt: str, cls: str, perm: Optional[str] = None) -> List[Tuple[str, float]]:
        if self.merge_permissions and perm is None:
            combined = []
            for p in self._merged_rules[src][tgt][cls]:
                combined.extend(self._metadata.get((src, tgt, cls, p), []))
            return combined[:3]
        else:
            key = (src, tgt, cls, perm) if perm else (src, tgt, cls, '')
            return self._metadata.get(key, [])
    
    def get_metadata(self, src: str, tgt: str, cls: str, perm: Optional[str] = None) -> List[Tuple[str, float]]:
        """Get metadata for a specific rule."""
        with self._lock:
            return self._get_metadata_internal(src, tgt, cls, perm)
    
    def filter(
        self,
        source_whitelist: Optional[Set[str]] = None,
        source_blacklist: Optional[Set[str]] = None,
        perm_whitelist: Optional[Set[str]] = None,
    ) -> 'RuleSet':
        """Filter rules based on source domains and/or permissions."""
        new_ruleset = RuleSet(merge_permissions=self.merge_permissions)
        
        for src, tgt, cls, perms in self.get_all_rules():
            if source_whitelist and src not in source_whitelist:
                continue
            if source_blacklist and src in source_blacklist:
                continue
            
            filtered_perms = perms
            if perm_whitelist:
                filtered_perms = [p for p in perms if p in perm_whitelist]
                if not filtered_perms:
                    continue
            
            for perm in filtered_perms:
                denial = {
                    'source': src,
                    'target': tgt,
                    'class': cls,
                    'permissions': {perm},
                    'raw': f"<filtered from {src} {tgt} {cls} {perm}>",
                    'timestamp': time.time(),
                }
                new_ruleset.add_denial(denial)
        
        return new_ruleset
    
    def count(self) -> int:
        """Get the total number of rules."""
        return len(self.get_all_rules())
    
    def get_unique_sources(self) -> Set[str]:
        """Get all unique source domains."""
        return {src for src, _, _, _ in self.get_all_rules()}
    
    def get_unique_targets(self) -> Set[str]:
        """Get all unique target types."""
        return {tgt for _, tgt, _, _ in self.get_all_rules()}
    
    def get_unique_classes(self) -> Set[str]:
        """Get all unique target classes."""
        return {cls for _, _, cls, _ in self.get_all_rules()}
    
    def summarize(self) -> Dict[str, Any]:
        """Get a summary of the rule set."""
        rules = self.get_all_rules()
        groups = defaultdict(set)
        for src, tgt, cls, perms in rules:
            groups[(src, tgt, cls)].update(perms)
        
        return {
            'total_rules': len(rules),
            'unique_sources': len(self.get_unique_sources()),
            'unique_targets': len(self.get_unique_targets()),
            'unique_classes': len(self.get_unique_classes()),
            'grouped_count': len(groups),
            'groups': {
                f"{src} -> {tgt} : {cls}": sorted(perms)
                for (src, tgt, cls), perms in groups.items()
            }
        }
