"""
Progress formatters
- Date / label helpers used by progress endpoints
- Keep this file side-effect free (NO routers/endpoints here)
"""

from __future__ import annotations
from datetime import date, datetime, timezone
from typing import Optional

TR_MONTHS = {
    1: "Oca", 2: "Şub", 3: "Mar", 4: "Nis", 5: "May", 6: "Haz",
    7: "Tem", 8: "Ağu", 9: "Eyl", 10: "Eki", 11: "Kas", 12: "Ara"
}

def ensure_date(value) -> Optional[date]:
    """
    Accepts: date | datetime | ISO string | None
    Returns: date | None
    """
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).date()
    if isinstance(value, str):
        try:
            if "T" in value:
                dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc).date()
            return date.fromisoformat(value[:10])
        except Exception:
            return None
    return None

def format_date_tr(d: Optional[date]) -> Optional[str]:
    """25 Ağu style"""
    if not d:
        return None
    return f"{d.day} {TR_MONTHS.get(d.month, d.month)}"
