"""
CLI Output Module

Simple, clean CLI output for SELinux policy rule generation.
"""

import os
from typing import List, Optional
try:
    from .parser import AVCDenial
except ImportError:
    from parser import AVCDenial


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class CLIFormatter:
    """CLI formatter for printing and saving SELinux policy rules."""
    
    MAX_RULES_DISPLAY = 20
    
    def __init__(self):
        pass
    
    def print_rules(self, denials: List[AVCDenial], format: str = 'cil', unique: bool = True) -> None:
        """Print rules nicely to stdout."""
        if not denials:
            print(f"{Colors.YELLOW}No rules to display.{Colors.RESET}")
            return
        
        if unique:
            rules = self._get_unique_rules(denials, format)
        else:
            rules = self._generate_rules(denials, format)
        
        if format == 'cil':
            label = "Generated CIL rules"
        else:
            label = "Generated TE rules"
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}{label}:{Colors.RESET}")
        
        display_rules = rules[:self.MAX_RULES_DISPLAY]
        for rule in display_rules:
            print(f"  {Colors.GREEN}{rule}{Colors.RESET}")
        
        remaining = len(rules) - self.MAX_RULES_DISPLAY
        if remaining > 0:
            print(f"  {Colors.YELLOW}... and {remaining} more rules{Colors.RESET}")
        
        if unique:
            print(f"\n{Colors.BLUE}{Colors.BOLD}Unique rules: {len(rules)} | Total denials: {len(denials)}{Colors.RESET}")
        else:
            print(f"\n{Colors.BLUE}{Colors.BOLD}Total rules generated: {len(rules)}{Colors.RESET}")
    
    def save_rules(self, denials: List[AVCDenial], filepath: str, format: str = 'cil', unique: bool = True) -> None:
        """Save rules to a file."""
        if not denials:
            print(f"{Colors.YELLOW}No rules to save.{Colors.RESET}")
            return
        
        if unique:
            rules = self._get_unique_rules(denials, format)
        else:
            rules = self._generate_rules(denials, format)
        
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(rules))
            f.write('\n')
        
        if unique:
            print(f"\n{Colors.GREEN}✅ {len(rules)} unique rules saved to: {filepath}{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}✅ {len(rules)} rules saved to: {filepath}{Colors.RESET}")
    
    def print_summary(self, denials: List[AVCDenial]) -> None:
        """Print statistics summary."""
        if not denials:
            print(f"{Colors.YELLOW}No denials to summarize.{Colors.RESET}")
            return
        
        sources = set(d.source for d in denials)
        targets = set(d.target for d in denials)
        tclasses = set(d.tclass for d in denials)
        
        all_perms = set()
        for d in denials:
            all_perms.update(d.permissions)
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 Summary:{Colors.RESET}")
        print(f"  {Colors.GREEN}Total denials:{Colors.RESET} {len(denials)}")
        print(f"  {Colors.GREEN}Unique sources:{Colors.RESET} {len(sources)}")
        print(f"  {Colors.GREEN}Unique targets:{Colors.RESET} {len(targets)}")
        print(f"  {Colors.GREEN}Unique classes:{Colors.RESET} {len(tclasses)}")
        print(f"  {Colors.GREEN}Permissions:{Colors.RESET} {', '.join(sorted(all_perms))}")
    
    def _generate_rules(self, denials: List[AVCDenial], format: str) -> List[str]:
        """Generate rules from denials."""
        if format == 'cil':
            return [self._to_cil(d) for d in denials]
        else:
            return [self._to_te(d) for d in denials]
    
    def _get_unique_rules(self, denials: List[AVCDenial], format: str) -> List[str]:
        """Create unique rules by deduplicating based on source, target, class, and permissions."""
        seen = set()
        unique_rules = []
        
        for denial in denials:
            key = (denial.source, denial.target, denial.tclass, frozenset(denial.permissions))
            if key not in seen:
                seen.add(key)
                if format == 'cil':
                    unique_rules.append(self._to_cil(denial))
                else:
                    unique_rules.append(self._to_te(denial))
        
        return unique_rules
    
    def _to_cil(self, denial: AVCDenial) -> str:
        """Convert denial to CIL format."""
        source = denial.source
        target = denial.target
        tclass = denial.tclass
        perms = ' '.join(sorted(denial.permissions))
        return f"(allow {source} {target} ({tclass} ({perms})))"
    
    def _to_te(self, denial: AVCDenial) -> str:
        """Convert denial to TE format."""
        source = denial.source
        target = denial.target
        tclass = denial.tclass
        perms = ' '.join(sorted(denial.permissions))
        return f"allow {source} {target}:{tclass} {{ {perms} }};"
    
    def format_output(self, denials: List[AVCDenial], filepath: Optional[str] = None, 
                      format: str = 'cil', unique: bool = True) -> None:
        """Format and output rules - print to stdout and optionally save to file."""
        if not denials:
            print(f"{Colors.YELLOW}No rules to output.{Colors.RESET}")
            return
        
        if unique:
            rules = self._get_unique_rules(denials, format)
        else:
            rules = self._generate_rules(denials, format)
        
        if format == 'cil':
            label = "Generated CIL rules"
        else:
            label = "Generated TE rules"
        
        print(f"\n{Colors.BLUE}{Colors.BOLD}📄 {label}:{Colors.RESET}")
        
        display_rules = rules[:self.MAX_RULES_DISPLAY]
        for rule in display_rules:
            print(f"  {Colors.GREEN}{rule}{Colors.RESET}")
        
        remaining = len(rules) - self.MAX_RULES_DISPLAY
        if remaining > 0:
            print(f"  {Colors.YELLOW}... and {remaining} more rules{Colors.RESET}")
        
        if filepath:
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            with open(filepath, 'w') as f:
                f.write('\n'.join(rules))
                f.write('\n')
            print(f"\n{Colors.GREEN}✅ Rules saved to: {filepath}{Colors.RESET}")
        
        if unique:
            print(f"\n{Colors.BLUE}{Colors.BOLD}📊 Unique rules: {len(rules)} | Total denials: {len(denials)}{Colors.RESET}")
        else:
            print(f"\n{Colors.BLUE}{Colors.BOLD}📊 Total rules generated: {len(rules)}{Colors.RESET}")
