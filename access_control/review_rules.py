from datetime import datetime
from exception_policy import TIME_FORMAT


def find_stale(access_list, now):
    stale = []

    for entry in access_list:
        expires = entry.get("expires")
        reason = ""

        if not entry["employed"]:
            reason = "퇴사한 계정"

        elif expires is not None and datetime.strptime(expires, TIME_FORMAT) <= now:
            reason = "만료된 예외"

        if reason != "":
            stale_entry = entry.copy()
            stale_entry["reason"] = reason
            stale.append(stale_entry)

    return stale