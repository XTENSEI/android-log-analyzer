"""
ADB Capture Module

Handles live capture of AVC denials from Android devices via ADB.
Supports multiple log sources and non-blocking reads.
"""

import subprocess
import select
import threading
import time
from typing import Optional, Callable, List, Dict, Any
from .parser import AVCParser


LOG_SOURCES = [
    ("dmesg", ["shell", "dmesg", "-w"]),
    ("logcat_events", ["shell", "logcat", "-b", "events", "-v", "brief"]),
    ("logcat_crash", ["shell", "logcat", "-b", "crash", "-v", "brief"]),
    ("logcat_radio", ["shell", "logcat", "-b", "radio", "-v", "brief"]),
    ("logcat_main", ["shell", "logcat", "-b", "main", "-v", "brief"]),
    ("kmsg", ["shell", "cat", "/proc/kmsg"]),
]


def wait_for_device(timeout: Optional[int] = None, verbose: bool = False) -> bool:
    """
    Wait for an ADB device to be available.
    Returns True when device is connected.
    """
    start_time = time.time()
    
    while True:
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True
        )
        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:
            if '\tdevice' in line or '\trecovery' in line:
                return True
        
        if timeout and (time.time() - start_time) > timeout:
            return False
        
        if verbose:
            print("Waiting for ADB device...")
        time.sleep(2)


def is_device_connected() -> bool:
    """Check if an ADB device is connected."""
    result = subprocess.run(
        ['adb', 'devices'],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split('\n')
    return any('\tdevice' in line or '\trecovery' in line for line in lines[1:])


def capture_logcat(
    source_name: str,
    args: List[str],
    callback: Callable[[Dict[str, Any]], None],
    stop_event: threading.Event,
    verbose: bool = False,
) -> None:
    """Capture logs from a single source and call callback for each AVC denial."""
    try:
        if verbose:
            print(f"[{source_name}] Starting: adb {' '.join(args)}")
        
        process = subprocess.Popen(
            ['adb'] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace'
        )
        
        fd = process.stdout.fileno()
        parser = AVCParser()
        
        while not stop_event.is_set():
            rlist, _, _ = select.select([fd], [], [], 1.0)
            if fd in rlist:
                line = process.stdout.readline()
                if not line:
                    break
                
                denial = parser.parse_line(line)
                if denial:
                    callback(denial.to_dict())
        
        process.terminate()
        process.wait(timeout=5)
        
    except Exception as e:
        if verbose:
            print(f"[{source_name}] Error: {e}")


def capture_all_sources(
    callback: Callable[[Dict[str, Any]], None],
    duration: int = 60,
    verbose: bool = False,
    sources: Optional[List[tuple]] = None,
) -> int:
    """
    Capture AVC denials from all log sources.
    Returns the total number of denials captured.
    """
    if sources is None:
        sources = LOG_SOURCES
    
    if not is_device_connected():
        if not wait_for_device(verbose=verbose):
            raise RuntimeError("No ADB device connected")
    
    stop_event = threading.Event()
    threads = []
    total_count = [0]
    lock = threading.Lock()
    
    def wrapped_callback(denial: Dict[str, Any]) -> None:
        with lock:
            total_count[0] += 1
        callback(denial)
    
    for name, args in sources:
        t = threading.Thread(
            target=capture_logcat,
            args=(name, args, wrapped_callback, stop_event, verbose)
        )
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.2)
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("Interrupted, stopping capture...")
    finally:
        stop_event.set()
        time.sleep(1)
    
    return total_count[0]


def pull_pstore(callback: Callable[[Dict[str, Any]], None], verbose: bool = False) -> int:
    """Pull and parse AVC denials from pstore."""
    count = [0]
    parser = AVCParser()
    
    try:
        result = subprocess.run(
            ['adb', 'shell', 'ls', '/sys/fs/pstore'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return 0
        
        files = result.stdout.strip().split('\n')
        for f in files:
            if not f:
                continue
            
            if verbose:
                print(f"[pstore] Pulling {f}")
            
            content = subprocess.run(
                ['adb', 'shell', 'cat', f'/sys/fs/pstore/{f}'],
                capture_output=True
            )
            text = content.stdout.decode('utf-8', errors='ignore')
            
            for line in text.split('\n'):
                denial = parser.parse_line(line)
                if denial:
                    callback(denial.to_dict())
                    count[0] += 1
    
    except Exception as e:
        if verbose:
            print(f"[pstore] Error: {e}")
    
    return count[0]
