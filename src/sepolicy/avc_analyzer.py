"""
Professional-Grade AVC (Access Vector Cache) Denial Analyzer

A comprehensive SELinux AVC analysis system for Android with:
- Risk Intelligence Engine with scoring
- Root Cause Analysis
- Fix Generator with multiple policy rule types
- Interactive HTML Report Generator
- Trend Analysis
- Correlation Engine

Author: Security Engineering Team
"""

import json
import re
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum

if __name__ == "__main__":
    from parser import AVCParser, AVCDenial
else:
    try:
        from .parser import AVCParser, AVCDenial
    except ImportError:
        from parser import AVCParser, AVCDenial


class RiskLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class RiskAssessment:
    score: int
    level: RiskLevel
    factors: List[str]
    exploitability: str
    impact: str


@dataclass
class RootCauseAnalysis:
    cause_type: str
    description: str
    details: str


@dataclass
class PolicyFix:
    rule_type: str
    rule: str
    comment: str
    priority: int


@dataclass
class AnalyzedDenial:
    denial: AVCDenial
    risk: RiskAssessment
    root_cause: RootCauseAnalysis
    fixes: List[PolicyFix]
    denial_hash: str
    group_id: str


class CRITICAL_PERMISSIONS:
    EXEC = {'execmem', 'exec', 'execute', 'execheap', 'exmmap'}
    PRIVILEGED = {'setuid', 'setgid', 'setpgid', 'setsched', 'setcap'}
    DEVICE = {'mknod', 'mkfifo', 'mknodat'}
    IPC = {'shmget', 'shmctl', 'msgget', 'msgsnd', 'msgrcv'}
    IOCTL = {'ioctl'}
    DANGEROUS = {'write', 'read', 'open'} | IOCTL


class PRIVILEGED_DOMAINS:
    ROOT = {'root', 'kernel'}
    SYSTEM = {'init', 'system_server', 'surfaceflinger', 'servicemanager'}
    HAL = {'hal_fingerprint', 'hal_health', 'hal_power', 'hal_audio', 'hal_camera',
           'hal_secure_element', 'hal_keymaster', 'hal_gnss'}
    CORE = {'zygote', 'installd', 'vold', 'netd', 'healthd', 'lmkd'}


class SENSITIVE_TARGETS:
    CREDENTIALS = {'keystore', 'credentials', 'password', 'gatekeeper', 'fingerprint'}
    SECURITY = {'selinuxfs', 'securityfs', 'apex', 'teqc'}
    DEVICE = {'binder', 'vndbinder', 'hwbinder', 'device', 'chr_file'}
    PROC = {'proc_perfmgr', 'proc_audit', 'proc_sysrq'}


class ExploitabilityAnalyzer:
    EXPLOIT_PATTERNS = {
        'mknod_privileged': (r'mknod|mkfifo|mknodat', 'Device creation could allow privilege escalation'),
        'exec_heap': (r'execmem|execheap', 'Executable memory mapping for code injection'),
        'setuid_root': (r'setuid.*root|setgid.*root', 'Potential root privilege escalation'),
        'binder_device': (r'binder_device|vndbinder|hwbinder', 'Binder IPC manipulation'),
        'selinux_status': (r'selinuxfs', 'SELinux status detection - possible security bypass attempt'),
        'proc_manipulation': (r'proc_perfmgr', 'Performance manager manipulation'),
    }

    @classmethod
    def analyze(cls, denial: AVCDenial) -> Tuple[str, int]:
        for name, (pattern, desc) in cls.EXPLOIT_PATTERNS.items():
            if re.search(pattern, ' '.join(denial.permissions), re.IGNORECASE):
                return desc, 80
            if denial.target in SENSITIVE_TARGETS.DEVICE:
                return 'Direct device access attempt', 75
            if denial.target in SENSITIVE_TARGETS.SECURITY:
                return 'Security subsystem access attempt', 90
        return '', 0


class RiskIntelligenceEngine:
    PERMISSION_WEIGHTS = {
        'execmem': 40, 'exec': 35, 'execute': 35, 'execheap': 40,
        'setuid': 50, 'setgid': 50, 'setpgid': 45, 'setsched': 45,
        'mknod': 45, 'mkfifo': 40, 'mknodat': 45,
        'ioctl': 20,
        'shmget': 25, 'shmctl': 30, 'msgget': 20,
        'write': 10, 'read': 5, 'open': 5,
        'getattr': 5, 'setattr': 15,
    }

    TARGET_WEIGHTS = {
        'keystore': 50, 'credentials': 50, 'password': 50,
        'gatekeeper': 45, 'fingerprint': 40,
        'selinuxfs': 35, 'securityfs': 40,
        'binder_device': 25, 'vndbinder': 25, 'hwbinder': 25,
        'proc_perfmgr': 20,
    }

    DOMAIN_WEIGHTS = {
        'init': 30, 'system_server': 25, 'root': 50,
        'zygote': 20, 'surfaceflinger': 20,
        'hal_fingerprint': 25, 'hal_keystore': 30,
        'untrusted_app': 10, 'platform_app': 15, 'system_app': 15,
    }

    @classmethod
    def assess(cls, denial: AVCDenial) -> RiskAssessment:
        score = 0
        factors = []
        exploitability, exploit_score = ExploitabilityAnalyzer.analyze(denial)
        score += exploit_score
        if exploitability:
            factors.append(f"Exploitable: {exploitability}")

        for perm in denial.permissions:
            perm_lower = perm.lower()
            for key, weight in cls.PERMISSION_WEIGHTS.items():
                if key in perm_lower:
                    score += weight
                    if weight >= 30:
                        factors.append(f"Critical permission: {perm}")
                    break

        target_lower = denial.target.lower()
        for key, weight in cls.TARGET_WEIGHTS.items():
            if key in target_lower:
                score += weight
                factors.append(f"Sensitive target: {denial.target}")
                break

        source_lower = denial.source.lower()
        for key, weight in cls.DOMAIN_WEIGHTS.items():
            if key in source_lower:
                score += weight
                factors.append(f"Privileged domain: {denial.source}")
                break

        if denial.permissive:
            score = max(0, score - 20)
            factors.append("Running in permissive mode (lower risk)")

        score = min(100, score)

        if score >= 80:
            level = RiskLevel.CRITICAL
            impact = "Critical security violation - immediate attention required"
        elif score >= 60:
            level = RiskLevel.HIGH
            impact = "High risk - may lead to privilege escalation or system compromise"
        elif score >= 40:
            level = RiskLevel.MEDIUM
            impact = "Medium risk - could affect system stability or security"
        elif score >= 20:
            level = RiskLevel.LOW
            impact = "Low risk - minor security or functionality impact"
        else:
            level = RiskLevel.INFO
            impact = "Informational - unlikely to cause issues"

        return RiskAssessment(
            score=score,
            level=level,
            factors=factors,
            exploitability=exploitability or "Not easily exploitable",
            impact=impact
        )


class RootCauseAnalyzer:
    @classmethod
    def analyze(cls, denial: AVCDenial) -> RootCauseAnalysis:
        if denial.source.startswith('untrusted_app'):
            if 'read' in denial.permissions and 'selinuxfs' in denial.target:
                return RootCauseAnalysis(
                    cause_type="PERMISSION_DENIED",
                    description="App lacks permission to read SELinux status",
                    details="Untrusted apps should not be able to read SELinux enforce status. "
                           "This is typically blocked for security reasons."
                )
            return RootCauseAnalysis(
                cause_type="PERMISSION_DENIED",
                description=f"App lacks permission to perform {', '.join(denial.permissions)} on {denial.target}",
                details=f"The domain '{denial.source}' does not have the required SELinux permission "
                       f"to {', '.join(denial.permissions)} {denial.tclass} with target context '{denial.target}'"
            )

        if denial.source.startswith('hal_') or '_hal_' in denial.source:
            return RootCauseAnalysis(
                cause_type="HAL_PERMISSION_MISSING",
                description=f"HAL module {denial.source} missing sepolicy rules",
                details="Hardware Abstraction Layer modules require specific SELinux policies. "
                       "The module is attempting to access a resource without proper policy definition."
            )

        if denial.source in PRIVILEGED_DOMAINS.HAL:
            return RootCauseAnalysis(
                cause_type="DOMAIN_TRANSITION",
                description="Domain transition not allowed",
                details=f"The domain '{denial.source}' is attempting to access '{denial.target}' "
                       f"but lacks the necessary domain transition rules or type enforcement."
            )

        if denial.tclass == 'chr_file' and denial.target.endswith('_device'):
            return RootCauseAnalysis(
                cause_type="DEVICE_ACCESS_DENIED",
                description="Missing device access policy",
                details=f"No SELinux policy allows '{denial.source}' to access device '{denial.target}'. "
                       f"Add a device type or allow rule for this device access."
            )

        if denial.target.startswith('u:object_r:sysfs'):
            return RootCauseAnalysis(
                cause_type="SYSFS_ACCESS_DENIED",
                description="Missing sysfs node access policy",
                details="The source domain lacks permission to access this sysfs node. "
                       "Either add an allow rule or mark the sysfs node with appropriate file context."
            )

        return RootCauseAnalysis(
            cause_type="MISSING_POLICY_RULE",
            description="Missing sepolicy rule for this access pattern",
            details=f"No allow rule exists for: {denial.source} -> {denial.target}:{denial.tclass} "
                   f"with permissions {denial.permissions}"
        )


class FixGenerator:
    @classmethod
    def generate_fixes(cls, denial: AnalyzedDenial) -> List[PolicyFix]:
        fixes = []
        d = denial.denial

        fixes.append(PolicyFix(
            rule_type="basic",
            rule=f"allow {d.source} {d.target}:{d.tclass} {','.join(sorted(d.permissions))};",
            comment=f"Basic allow rule for {d.source} to access {d.target} {d.tclass}",
            priority=1
        ))

        fixes.append(PolicyFix(
            rule_type="neverallow_check",
            rule=f"# Verify this doesn't violate neverallow rules:\n# neverallow {d.source} {d.target}:{d.tclass} {{ {','.join(sorted(d.permissions))} }};",
            comment="Neverallow check - verify this rule doesn't conflict with existing policy",
            priority=2
        ))

        if d.target.startswith('u:object_r:'):
            actual_target = d.target.replace('u:object_r:', '')
            fixes.append(PolicyFix(
                rule_type="type_enforcement",
                rule=f"# Type enforcement rule\ntype {actual_target}_t;\nallow {d.source} {actual_target}_t:{d.tclass} {','.join(sorted(d.permissions))};",
                comment=f"Define type {actual_target}_t and allow access",
                priority=3
            ))

        if d.source.startswith('hal_') or '_hal_' in d.source:
            fixes.append(PolicyFix(
                rule_type="hal_attribute",
                rule=f"# HAL module rule with attributes\nallow {d.source} {d.target}:{d.tclass} {','.join(sorted(d.permissions))};\n# Or use hal attribute:\nallow hal_{d.source.split('_')[-1]}_domain {d.target}:{d.tclass} {','.join(sorted(d.permissions))};",
                comment="HAL domain attribute-based rule for better compatibility",
                priority=4
            ))

        if d.tclass in ('file', 'dir') and hasattr(d, 'path') and d.path:
            path = d.path
            if '/sys/' in path:
                fixes.append(PolicyFix(
                    rule_type="file_context",
                    rule=f"# File context for sysfs\n{path} u:object_r:{d.target}:s0",
                    comment="File context rule for sysfs node (requires file_contexts update)",
                    priority=5
                ))
            elif '/proc/' in path:
                fixes.append(PolicyFix(
                    rule_type="file_context",
                    rule=f"# File context for procfs\n{path} u:object_r:{d.target}:s0",
                    comment="File context rule for proc node (requires file_contexts update)",
                    priority=5
                ))

        fixes.append(PolicyFix(
            rule_type="audit",
            rule=f"# Audit rule to suppress logging (optional)\ndontaudit {d.source} {d.target}:{d.tclass} {','.join(sorted(d.permissions))};",
            comment="Don't audit rule - suppress repeated denial logs (use carefully)",
            priority=6
        ))

        return fixes


class CorrelationEngine:
    @classmethod
    def find_correlations(cls, denials: List[AnalyzedDenial]) -> Dict[str, Any]:
        by_app = defaultdict(list)
        by_source = defaultdict(list)
        by_target = defaultdict(list)

        for d in denials:
            if d.denial.app:
                by_app[d.denial.app].append(d)
            by_source[d.denial.source].append(d)
            by_target[d.denial.target].append(d)

        correlations = {
            'apps_with_multiple_issues': [],
            'frequent_sources': [],
            'frequent_targets': [],
            'denial_chains': [],
        }

        for app, app_denials in by_app.items():
            if len(app_denials) >= 2:
                correlations['apps_with_multiple_issues'].append({
                    'app': app,
                    'count': len(app_denials),
                    'denials': [str(d.denial.permissions) for d in app_denials[:5]]
                })

        for source, src_denials in by_source.items():
            if len(src_denials) >= 3:
                correlations['frequent_sources'].append({
                    'source': source,
                    'count': len(src_denials),
                    'targets': list(set(d.denial.target for d in src_denials))
                })

        chains = cls._detect_chains(denials)
        if chains:
            correlations['denial_chains'] = chains

        return correlations

    @classmethod
    def _detect_chains(cls, denials: List[AnalyzedDenial]) -> List[Dict]:
        chains = []
        source_to_target = defaultdict(list)
        
        for d in denials:
            source_to_target[d.denial.source].append({
                'target': d.denial.target,
                'permissions': d.denial.permissions,
                'class': d.denial.tclass
            })

        return chains


class TrendAnalyzer:
    @classmethod
    def compare_scans(cls, old_denials: List[AnalyzedDenial], 
                      new_denials: List[AnalyzedDenial]) -> Dict[str, Any]:
        old_hashes = {d.denial_hash for d in old_denials}
        new_hashes = {d.denial_hash for d in new_denials}

        new_only = new_hashes - old_hashes
        fixed = old_hashes - new_hashes

        old_by_hash = {d.denial_hash: d for d in old_denials}
        new_by_hash = {d.denial_hash: d for d in new_denials}

        escalated = []
        for h in (old_hashes & new_hashes):
            old_score = old_by_hash[h].risk.score
            new_score = new_by_hash[h].risk.score
            if new_score > old_score + 10:
                escalated.append({
                    'denial': old_by_hash[h].denial.source,
                    'old_score': old_score,
                    'new_score': new_score,
                    'change': new_score - old_score
                })

        new_denials_list = [new_by_hash[h] for h in new_only if h in new_by_hash]
        patterns = cls._detect_patterns(new_denials_list)

        return {
            'new_denials': len(new_only),
            'fixed_denials': len(fixed),
            'escalated_risks': escalated,
            'patterns': patterns,
            'summary': f"{len(new_only)} new, {len(fixed)} fixed, {len(escalated)} escalated"
        }

    @classmethod
    def _detect_patterns(cls, denials: List[AnalyzedDenial]) -> List[Dict]:
        patterns = []
        perm_patterns = defaultdict(int)
        
        for d in denials:
            for p in d.denial.permissions:
                perm_patterns[p] += 1

        if perm_patterns:
            top_perms = sorted(perm_patterns.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_perms:
                patterns.append({
                    'type': 'permission_frequency',
                    'description': f"Most common denied permissions: {', '.join(f'{p}({c})' for p,c in top_perms)}"
                })

        return patterns


class HTMLReportGenerator:
    @classmethod
    def generate(cls, denials: List[AnalyzedDenial], 
                 correlations: Dict = None,
                 title: str = "AVC Denial Analysis Report") -> str:
        stats = cls._compute_stats(denials)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-red: #f85149;
            --accent-orange: #d29922;
            --accent-purple: #a371f7;
            --border-color: #30363d;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        
        header {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 24px;
        }}
        
        h1 {{ font-size: 2rem; margin-bottom: 8px; }}
        h2 {{ font-size: 1.4rem; margin-bottom: 16px; color: var(--text-secondary); }}
        
        .meta {{ color: var(--text-secondary); font-size: 0.9rem; }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .stat-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        
        .stat-value {{ font-size: 2.5rem; font-weight: bold; }}
        .stat-label {{ color: var(--text-secondary); font-size: 0.9rem; }}
        
        .critical {{ color: var(--accent-red); }}
        .high {{ color: var(--accent-orange); }}
        .medium {{ color: var(--accent-purple); }}
        .low {{ color: var(--accent-blue); }}
        .info {{ color: var(--text-secondary); }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}
        
        .chart-container {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
        }}
        
        .chart-title {{
            font-size: 1rem;
            margin-bottom: 16px;
            color: var(--text-secondary);
        }}
        
        .denial-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 16px;
            overflow: hidden;
        }}
        
        .denial-header {{
            padding: 16px 20px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid transparent;
            transition: background 0.2s;
        }}
        
        .denial-card.open .denial-header {{ border-bottom-color: var(--border-color); }}
        
        .denial-header:hover {{ background: var(--bg-tertiary); }}
        
        .denial-summary {{
            display: flex;
            align-items: center;
            gap: 16px;
            flex: 1;
        }}
        
        .risk-badge {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .risk-critical {{ background: rgba(248,81,73,0.2); color: var(--accent-red); border: 1px solid var(--accent-red); }}
        .risk-high {{ background: rgba(210,153,34,0.2); color: var(--accent-orange); border: 1px solid var(--accent-orange); }}
        .risk-medium {{ background: rgba(163,113,247,0.2); color: var(--accent-purple); border: 1px solid var(--accent-purple); }}
        .risk-low {{ background: rgba(88,166,255,0.2); color: var(--accent-blue); border: 1px solid var(--accent-blue); }}
        .risk-info {{ background: rgba(139,148,158,0.2); color: var(--text-secondary); border: 1px solid var(--text-secondary); }}
        
        .denial-details {{
            padding: 20px;
            display: none;
        }}
        
        .denial-card.open .denial-details {{ display: block; }}
        
        .detail-section {{
            margin-bottom: 20px;
        }}
        
        .detail-section h3 {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .detail-row {{
            display: flex;
            gap: 12px;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }}
        
        .detail-label {{ color: var(--text-secondary); min-width: 120px; }}
        .detail-value {{ flex: 1; word-break: break-all; }}
        
        .code-block {{
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.85rem;
            overflow-x: auto;
            position: relative;
        }}
        
        .copy-btn {{
            position: absolute;
            top: 8px;
            right: 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
        }}
        
        .copy-btn:hover {{ background: var(--accent-blue); color: white; }}
        
        .accordion-icon {{
            transition: transform 0.2s;
            color: var(--text-secondary);
        }}
        
        .denial-card.open .accordion-icon {{ transform: rotate(180deg); }}
        
        .tabs {{ display: flex; gap: 4px; margin-bottom: 16px; border-bottom: 1px solid var(--border-color); }}
        .tab {{
            padding: 12px 20px;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }}
        .tab:hover {{ color: var(--text-primary); }}
        .tab.active {{ color: var(--accent-blue); border-bottom-color: var(--accent-blue); }}
        
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        
        .correlation-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        
        .tag {{
            display: inline-block;
            background: var(--bg-tertiary);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-right: 4px;
            margin-bottom: 4px;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ AVC Denial Analysis Report</h1>
            <h2>{title}</h2>
            <div class="meta">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                Total Denials: {stats['total']}
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value critical">{stats['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-card">
                <div class="stat-value high">{stats['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-card">
                <div class="stat-value medium">{stats['medium']}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-card">
                <div class="stat-value low">{stats['low']}</div>
                <div class="stat-label">Low</div>
            </div>
            <div class="stat-card">
                <div class="stat-value info">{stats['info']}</div>
                <div class="stat-label">Info</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['unique_sources']}</div>
                <div class="stat-label">Unique Sources</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">Risk Distribution</div>
                <canvas id="riskChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Top Offenders by Source</div>
                <canvas id="sourceChart"></canvas>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('all')">All Denials</button>
            <button class="tab" onclick="showTab('critical')">Critical Only</button>
            <button class="tab" onclick="showTab('high')">High Risk</button>
            <button class="tab" onclick="showTab('correlations')">Correlations</button>
        </div>
        
        <div id="all" class="tab-content active">
            {cls._render_denials(denials)}
        </div>
        
        <div id="critical" class="tab-content">
            {cls._render_denials([d for d in denials if d.risk.level == RiskLevel.CRITICAL])}
        </div>
        
        <div id="high" class="tab-content">
            {cls._render_denials([d for d in denials if d.risk.level in (RiskLevel.CRITICAL, RiskLevel.HIGH)])}
        </div>
        
        <div id="correlations" class="tab-content">
            {cls._render_correlations(correlations or {})}
        </div>
    </div>
    
    <script>
        const riskData = {{
            labels: ['Critical', 'High', 'Medium', 'Low', 'Info'],
            datasets: [{{
                data: [{stats['critical']}, {stats['high']}, {stats['medium']}, {stats['low']}, {stats['info']}],
                backgroundColor: ['#f85149', '#d29922', '#a371f7', '#58a6ff', '#8b949e'],
                borderWidth: 0
            }}]
        }};
        
        const sourceData = {{
            labels: {json.dumps(list(stats['top_sources'].keys())[:8])},
            datasets: [{{
                label: 'Denials',
                data: {json.dumps(list(stats['top_sources'].values())[:8])},
                backgroundColor: '#58a6ff'
            }}]
        }};
        
        new Chart(document.getElementById('riskChart'), {{
            type: 'doughnut',
            data: riskData,
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#e6edf3' }} }}
                }}
            }}
        }});
        
        new Chart(document.getElementById('sourceChart'), {{
            type: 'bar',
            data: sourceData,
            options: {{
                responsive: true,
                plugins: {{ legend: {{ display: false }} }},
                scales: {{
                    y: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#30363d' }} }},
                    x: {{ ticks: {{ color: '#8b949e' }}, grid: {{ display: false }} }}
                }}
            }}
        }});
        
        function showTab(tabId) {{
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            event.target.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }}
        
        function toggleCard(element) {{
            element.closest('.denial-card').classList.toggle('open');
        }}
        
        function copyCode(btn) {{
            const code = btn.parentElement.textContent.replace('Copy', '').trim();
            navigator.clipboard.writeText(code);
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy', 2000);
        }}
    </script>
</body>
</html>"""
        return html

    @classmethod
    def _compute_stats(cls, denials: List[AnalyzedDenial]) -> Dict:
        stats = {
            'total': len(denials),
            'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0,
            'unique_sources': set(),
            'top_sources': defaultdict(int)
        }
        
        for d in denials:
            level = d.risk.level
            stats[level.value.lower()] += 1
            stats['unique_sources'].add(d.denial.source)
            stats['top_sources'][d.denial.source] += 1
        
        stats['unique_sources'] = len(stats['unique_sources'])
        stats['top_sources'] = dict(sorted(stats['top_sources'].items(), 
                                           key=lambda x: x[1], reverse=True))
        return stats

    @classmethod
    def _render_denials(cls, denials: List[AnalyzedDenial]) -> str:
        if not denials:
            return '<p style="color: var(--text-secondary); padding: 20px;">No denials to display.</p>'
        
        html = []
        for i, d in enumerate(denials):
            risk_class = f"risk-{d.risk.level.value.lower()}"
            fixes_html = ''
            for fix in d.fixes:
                fixes_html += f"""
                <div style="margin-top: 12px;">
                    <div style="color: var(--text-secondary); font-size: 0.8rem; margin-bottom: 4px;">
                        {fix.rule_type.upper()} - {fix.comment}
                    </div>
                    <div class="code-block">
                        <button class="copy-btn" onclick="copyCode(this)">Copy</button>
                        {fix.rule}
                    </div>
                </div>"""
            
            html.append(f"""
            <div class="denial-card">
                <div class="denial-header" onclick="toggleCard(this)">
                    <div class="denial-summary">
                        <span class="risk-badge {risk_class}">{d.risk.level.value}</span>
                        <span style="font-weight: 600;">{d.denial.source}</span>
                        <span style="color: var(--text-secondary);">→</span>
                        <span>{d.denial.target}</span>
                        <span style="color: var(--accent-blue);">({d.denial.tclass})</span>
                    </div>
                    <span style="color: var(--text-secondary);">Score: {d.risk.score}</span>
                    <span class="accordion-icon">▼</span>
                </div>
                <div class="denial-details">
                    <div class="detail-section">
                        <h3>Root Cause Analysis</h3>
                        <div class="detail-row">
                            <span class="detail-label">Type:</span>
                            <span class="detail-value">{d.root_cause.cause_type}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Description:</span>
                            <span class="detail-value">{d.root_cause.description}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Details:</span>
                            <span class="detail-value">{d.root_cause.details}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Impact:</span>
                            <span class="detail-value">{d.risk.impact}</span>
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h3>Risk Factors</h3>
                        {"".join(f'<span class="tag">{f}</span>' for f in d.risk.factors)}
                    </div>
                    
                    <div class="detail-section">
                        <h3>Access Details</h3>
                        <div class="detail-row">
                            <span class="detail-label">Permissions:</span>
                            <span class="detail-value">{", ".join(sorted(d.denial.permissions))}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Class:</span>
                            <span class="detail-value">{d.denial.tclass}</span>
                        </div>
                        {f'<div class="detail-row"><span class="detail-label">Path:</span><span class="detail-value">{d.denial.path}</span></div>' if d.denial.path else ''}
                        {f'<div class="detail-row"><span class="detail-label">App:</span><span class="detail-value">{d.denial.app}</span></div>' if d.denial.app else ''}
                    </div>
                    
                    <div class="detail-section">
                        <h3>Suggested Fixes</h3>
                        {fixes_html}
                    </div>
                </div>
            </div>""")
        
        return '\n'.join(html)

    @classmethod
    def _render_correlations(cls, correlations: Dict) -> str:
        if not correlations:
            return '<p style="color: var(--text-secondary); padding: 20px;">No correlations detected.</p>'
        
        html = []
        
        if correlations.get('apps_with_multiple_issues'):
            html.append('<h3 style="color: var(--text-secondary); margin-bottom: 12px;">Apps with Multiple Issues</h3>')
            for item in correlations['apps_with_multiple_issues']:
                html.append(f"""
                <div class="correlation-card">
                    <div style="font-weight: 600; margin-bottom: 8px;">{item['app']}</div>
                    <div style="color: var(--text-secondary);">{item['count']} denials detected</div>
                    <div style="margin-top: 8px;">
                        {"".join(f'<span class="tag">{p}</span>' for p in item['denials'])}
                    </div>
                </div>""")
        
        if correlations.get('frequent_sources'):
            html.append('<h3 style="color: var(--text-secondary); margin-bottom: 12px; margin-top: 20px;">Frequent Offenders</h3>')
            for item in correlations['frequent_sources']:
                html.append(f"""
                <div class="correlation-card">
                    <div style="font-weight: 600; margin-bottom: 8px;">{item['source']}</div>
                    <div style="color: var(--text-secondary);">{item['count']} denials</div>
                    <div style="margin-top: 8px;">
                        Targets: {", ".join(item['targets'][:5])}
                    </div>
                </div>""")
        
        if not html:
            html.append('<p style="color: var(--text-secondary);">No significant correlations found.</p>')
        
        return '\n'.join(html)


class AVCAnalyzer:
    def __init__(self):
        self.parser = AVCParser()
        self.denials: List[AVCDenial] = []
        self.analyzed_denials: List[AnalyzedDenial] = []
        self._source_stats: Dict[str, int] = defaultdict(int)
        
    def parse_file(self, path: str) -> List[AnalyzedDenial]:
        self.denials = self.parser.parse_file(path)
        self.analyzed_denials = self._analyze_denials()
        self._compute_stats()
        return self.analyzed_denials
    
    def parse_logs(self, log_content: str) -> List[AnalyzedDenial]:
        for line in log_content.split('\n'):
            denial = self.parser.parse_line(line)
            if denial:
                self.denials.append(denial)
        self.analyzed_denials = self._analyze_denials()
        self._compute_stats()
        return self.analyzed_denials
    
    def _analyze_denials(self) -> List[AnalyzedDenial]:
        analyzed = []
        for denial in self.denials:
            risk = RiskIntelligenceEngine.assess(denial)
            root_cause = RootCauseAnalyzer.analyze(denial)
            
            denial_hash = hashlib.md5(
                f"{denial.source}{denial.target}{denial.tclass}{','.join(sorted(denial.permissions))}".encode()
            ).hexdigest()[:12]
            
            analyzed_denial = AnalyzedDenial(
                denial=denial,
                risk=risk,
                root_cause=root_cause,
                fixes=FixGenerator.generate_fixes(AnalyzedDenial(
                    denial=denial, risk=risk, root_cause=root_cause, 
                    fixes=[], denial_hash='', group_id=''
                )),
                denial_hash=denial_hash,
                group_id=f"{denial.source}_{denial.target}_{denial.tclass}"
            )
            analyzed_denial.fixes = FixGenerator.generate_fixes(analyzed_denial)
            analyzed.append(analyzed_denial)
        
        return analyzed
    
    def _compute_stats(self):
        self._source_stats.clear()
        for d in self.analyzed_denials:
            self._source_stats[d.denial.source] += 1
    
    def get_statistics(self) -> Dict[str, Any]:
        by_level = defaultdict(int)
        by_source = defaultdict(int)
        by_target = defaultdict(int)
        by_class = defaultdict(int)
        
        for d in self.analyzed_denials:
            by_level[d.risk.level.value] += 1
            by_source[d.denial.source] += 1
            by_target[d.denial.target] += 1
            by_class[d.denial.tclass] += 1
        
        return {
            'total_denials': len(self.analyzed_denials),
            'by_risk_level': dict(by_level),
            'by_source': dict(sorted(by_source.items(), key=lambda x: x[1], reverse=True)),
            'by_target': dict(sorted(by_target.items(), key=lambda x: x[1], reverse=True)),
            'by_class': dict(sorted(by_class.items(), key=lambda x: x[1], reverse=True)),
        }
    
    def get_correlations(self) -> Dict:
        return CorrelationEngine.find_correlations(self.analyzed_denials)
    
    def generate_report(self, output_path: str = None) -> str:
        correlations = self.get_correlations()
        html = HTMLReportGenerator.generate(self.analyzed_denials, correlations)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        
        return html
    
    def compare_with(self, other: 'AVCAnalyzer') -> Dict:
        return TrendAnalyzer.compare_scans(self.analyzed_denials, other.analyzed_denials)
    
    def to_json(self) -> Dict[str, Any]:
        return {
            'statistics': self.get_statistics(),
            'denials': [
                {
                    'hash': d.denial_hash,
                    'source': d.denial.source,
                    'target': d.denial.target,
                    'class': d.denial.tclass,
                    'permissions': list(d.denial.permissions),
                    'risk_score': d.risk.score,
                    'risk_level': d.risk.level.value,
                    'root_cause': d.root_cause.description,
                    'fixes': [{'type': f.rule_type, 'rule': f.rule} for f in d.fixes]
                }
                for d in self.analyzed_denials
            ]
        }


def main():
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("Usage: python avc_analyzer.py <avc_log_file> [--html [output.html]]")
        print("       python avc_analyzer.py <log1> <log2> --compare")
        sys.exit(1)
    
    files = [f for f in sys.argv[1:] if not f.startswith('--')]
    args = [f for f in sys.argv[1:] if f.startswith('--')]
    
    if '--compare' in args and len(files) >= 2:
        analyzer1 = AVCAnalyzer()
        analyzer1.parse_file(files[0])
        
        analyzer2 = AVCAnalyzer()
        analyzer2.parse_file(files[1])
        
        comparison = analyzer1.compare_with(analyzer2)
        print(json.dumps(comparison, indent=2))
        return
    
    if not files:
        print("Error: No log file specified")
        sys.exit(1)
    
    log_file = files[0]
    if not os.path.exists(log_file):
        print(f"Error: File not found: {log_file}")
        sys.exit(1)
    
    analyzer = AVCAnalyzer()
    analyzer.parse_file(log_file)
    
    if '--html' in args:
        output_idx = args.index('--html') + 1
        output_file = args[output_idx] if output_idx < len(args) else 'avc_report.html'
        analyzer.generate_report(output_file)
        print(f"HTML report generated: {output_file}")
    else:
        stats = analyzer.get_statistics()
        print(json.dumps(stats, indent=2))
        
        print("\n=== Top Policy Fixes ===")
        critical = [d for d in analyzer.analyzed_denials if d.risk.level == RiskLevel.CRITICAL][:5]
        for d in critical:
            print(f"\n[{d.risk.level.value}] {d.denial.source} -> {d.denial.target}")
            print(f"  Root cause: {d.root_cause.description}")
            if d.fixes:
                print(f"  Fix: {d.fixes[0].rule}")


if __name__ == "__main__":
    main()
