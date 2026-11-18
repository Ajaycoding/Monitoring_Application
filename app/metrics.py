"""Localhost-only CPU and memory metrics for the demo.

Security: never shells out and never contacts remote hosts. Inventory
IP/hostname fields are display-only and are not used for collection.
"""

from __future__ import annotations

import time
from pathlib import Path

PROC_STAT = Path("/proc/stat")
PROC_MEMINFO = Path("/proc/meminfo")


def _read_cpu_times() -> tuple[int, int]:
    """Return (idle_plus_iowait, total) jiffies from /proc/stat."""
    line = PROC_STAT.read_text(encoding="utf-8").splitlines()[0]
    parts = line.split()
    values = [int(x) for x in parts[1:8]]
    idle = values[3] + values[4]
    total = sum(values)
    return idle, total


def get_cpu_percent(sample_seconds: float = 0.1) -> float:
    """Sample CPU usage on this machine as a percentage (0–100)."""
    idle1, total1 = _read_cpu_times()
    time.sleep(sample_seconds)
    idle2, total2 = _read_cpu_times()
    total_delta = total2 - total1
    idle_delta = idle2 - idle1
    if total_delta <= 0:
        return 0.0
    busy = 1.0 - (idle_delta / total_delta)
    return round(max(0.0, min(100.0, busy * 100.0)), 1)


def _parse_meminfo() -> dict[str, int]:
    """Parse /proc/meminfo into {key: bytes}."""
    result: dict[str, int] = {}
    for line in PROC_MEMINFO.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, rest = line.split(":", 1)
        parts = rest.split()
        if not parts:
            continue
        # Values are in kB.
        result[key] = int(parts[0]) * 1024
    return result


def _human_bytes(num: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(num)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{num} B"


def get_memory_stats() -> dict:
    """Return used / free (available) / total memory for this machine."""
    info = _parse_meminfo()
    total = info.get("MemTotal", 0)
    free = info.get("MemAvailable", info.get("MemFree", 0))
    used = max(0, total - free)
    return {
        "used_bytes": used,
        "free_bytes": free,
        "total_bytes": total,
        "used_human": _human_bytes(used),
        "free_human": _human_bytes(free),
        "total_human": _human_bytes(total),
    }


def collect_localhost_metrics(sample_seconds: float = 0.1) -> dict:
    """Single localhost snapshot used for all inventory rows in this demo."""
    return {
        "source": "localhost",
        "cpu_percent": get_cpu_percent(sample_seconds=sample_seconds),
        "memory": get_memory_stats(),
    }
