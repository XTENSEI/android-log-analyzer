"""
Android SELinux Policy Patcher

A comprehensive tool for analyzing AVC denials and generating SELinux policy rules.
Supports both offline log analysis and live ADB capture.
"""

__version__ = "1.0.0"
__author__ = "XTENSEI"

from .parser import AVCParser, parse_avc_line, AVCDenial
from .rules import RuleSet, Rule
from .formatters import (
    format_cil,
    format_te,
    export_json,
    export_csv,
    export_markdown,
    export_rules,
)
from .suggester import TypeSuggester, suggest_type_for_path
from .trend import init_database, store_denial, print_trend_report
from .adb import capture_all_sources, is_device_connected, wait_for_device

__all__ = [
    "AVCParser",
    "parse_avc_line",
    "AVCDenial",
    "RuleSet",
    "Rule",
    "format_cil",
    "format_te",
    "export_json",
    "export_csv",
    "export_markdown",
    "export_rules",
    "TypeSuggester",
    "suggest_type_for_path",
    "init_database",
    "store_denial",
    "print_trend_report",
    "capture_all_sources",
    "is_device_connected",
    "wait_for_device",
]
