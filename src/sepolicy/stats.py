"""
Statistics Module

Statistics and reporting for SELinux rules.
"""

from typing import Dict, List, Any
from collections import Counter
from .rules import RuleSet


def get_rule_statistics(ruleset: RuleSet) -> Dict[str, Any]:
    """Get comprehensive statistics about rules."""
    rules = ruleset.get_all_rules()
    
    sources = [r[0] for r in rules]
    targets = [r[1] for r in rules]
    classes = [r[2] for r in rules]
    
    source_counts = Counter(sources)
    target_counts = Counter(targets)
    class_counts = Counter(classes)
    
    return {
        'total_rules': len(rules),
        'unique_sources': len(source_counts),
        'unique_targets': len(target_counts),
        'unique_classes': len(class_counts),
        'top_sources': source_counts.most_common(10),
        'top_targets': target_counts.most_common(10),
        'top_classes': class_counts.most_common(10),
    }


def print_statistics(ruleset: RuleSet) -> None:
    """Print formatted statistics."""
    stats = get_rule_statistics(ruleset)
    
    print("\n=== Rule Statistics ===")
    print(f"Total rules: {stats['total_rules']}")
    print(f"Unique sources: {stats['unique_sources']}")
    print(f"Unique targets: {stats['unique_targets']}")
    print(f"Unique classes: {stats['unique_classes']}")
    
    print("\nTop Sources:")
    for src, count in stats['top_sources'][:5]:
        print(f"  {src}: {count}")
    
    print("\nTop Targets:")
    for tgt, count in stats['top_targets'][:5]:
        print(f"  {tgt}: {count}")
    
    print("\nTop Classes:")
    for cls, count in stats['top_classes'][:5]:
        print(f"  {cls}: {count}")
