"""
Pipeline Module

Pipeline processing for rules.
"""

from typing import List, Callable, Any
from .rules import RuleSet


class Pipeline:
    """Pipeline for processing rules."""
    
    def __init__(self):
        self.steps: List[Callable[[RuleSet], RuleSet]] = []
    
    def add_step(self, func: Callable[[RuleSet], RuleSet]) -> 'Pipeline':
        """Add a processing step."""
        self.steps.append(func)
        return self
    
    def process(self, ruleset: RuleSet) -> RuleSet:
        """Process rules through pipeline."""
        result = ruleset
        for step in self.steps:
            result = step(result)
        return result


def create_pipeline() -> Pipeline:
    """Create a new pipeline."""
    return Pipeline()
