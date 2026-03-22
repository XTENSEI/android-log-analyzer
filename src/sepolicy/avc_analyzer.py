"""
AVC Denial Analyzer Module

Analyzes SELinux AVC denial logs and generates policy rules.
"""

import json
import sys
from collections import defaultdict
from typing import Dict, List, Any, Optional, Tuple

if __name__ == "__main__":
    from parser import AVCParser, AVCDenial
else:
    from .parser import AVCParser, AVCDenial


class AVCDenialAnalyzer:
    """Analyzes AVC denials and generates statistics and policy rules."""
    
    def __init__(self):
        self.parser = AVCParser()
        self.denials: List[AVCDenial] = []
        self._source_count: Dict[str, int] = defaultdict(int)
        self._target_count: Dict[str, int] = defaultdict(int)
        self._tclass_count: Dict[str, int] = defaultdict(int)
        self._permission_count: Dict[str, int] = defaultdict(int)
        self._unique_combinations: set = set()
    
    def parse_file(self, path: str) -> List[AVCDenial]:
        """Parse an entire AVC log file."""
        self.denials = self.parser.parse_file(path)
        self._compute_stats()
        return self.denials
    
    def _compute_stats(self):
        """Compute statistics from parsed denials."""
        self._source_count.clear()
        self._target_count.clear()
        self._tclass_count.clear()
        self._permission_count.clear()
        self._unique_combinations.clear()
        
        for denial in self.denials:
            self._source_count[denial.source] += 1
            self._target_count[denial.target] += 1
            self._tclass_count[denial.tclass] += 1
            
            for perm in denial.permissions:
                self._permission_count[perm] += 1
            
            self._unique_combinations.add((
                denial.source,
                denial.target,
                denial.tclass
            ))
    
    def analyze(self) -> Dict[str, Any]:
        """Produce statistics about the denials."""
        return {
            'total_denials': len(self.denials),
            'by_source': dict(sorted(
                self._source_count.items(),
                key=lambda x: x[1],
                reverse=True
            )),
            'by_target': dict(sorted(
                self._target_count.items(),
                key=lambda x: x[1],
                reverse=True
            )),
            'by_tclass': dict(sorted(
                self._tclass_count.items(),
                key=lambda x: x[1],
                reverse=True
            )),
            'by_permission': dict(sorted(
                self._permission_count.items(),
                key=lambda x: x[1],
                reverse=True
            )),
            'unique_combinations': len(self._unique_combinations),
            'unique_combinations_list': [
                {
                    'source': combo[0],
                    'target': combo[1],
                    'tclass': combo[2]
                }
                for combo in sorted(self._unique_combinations)
            ],
        }
    
    def generate_rules(self) -> List[str]:
        """Generate allow rules for all unique (source, target, tclass) combinations."""
        rules = []
        
        combo_perms: Dict[Tuple[str, str, str], set] = defaultdict(set)
        
        for denial in self.denials:
            key = (denial.source, denial.target, denial.tclass)
            combo_perms[key].update(denial.permissions)
        
        for (source, target, tclass), perms in sorted(combo_perms.items()):
            rule = f"allow {source} {target}:{tclass} {','.join(sorted(perms))};"
            rules.append(rule)
        
        return rules
    
    def to_json(self) -> Dict[str, Any]:
        """Return a dict with all analysis."""
        analysis = self.analyze()
        return {
            'analysis': analysis,
            'suggested_rules': self.generate_rules(),
        }


def main():
    """Main function to analyze an AVC log file."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m sepolicy.avc_analyzer <avc_log_file>")
        sys.exit(1)
    
    log_file = sys.argv[1]
    
    analyzer = AVCDenialAnalyzer()
    analyzer.parse_file(log_file)
    
    analysis = analyzer.analyze()
    rules = analyzer.generate_rules()
    
    print("AVC Denial Analysis")
    print("=" * 40)
    print(f"Total denials: {analysis['total_denials']}")
    print()
    
    print("By Source (top 10):")
    for source, count in list(analysis['by_source'].items())[:10]:
        print(f"  {source}: {count}")
    print()
    
    print("By Target:")
    for target, count in analysis['by_target'].items():
        print(f"  {target}: {count}")
    print()
    
    print("By Class:")
    for tclass, count in analysis['by_tclass'].items():
        print(f"  {tclass}: {count}")
    print()
    
    print("By Permission:")
    for perm, count in analysis['by_permission'].items():
        print(f"  {perm}: {count}")
    print()
    
    print(f"Unique (source, target, tclass) combinations: {analysis['unique_combinations']}")
    print()
    
    print("Suggested Policy Rules:")
    for rule in rules[:20]:
        print(f"  {rule}")
    if len(rules) > 20:
        print(f"  ... and {len(rules) - 20} more rules")


if __name__ == "__main__":
    main()
