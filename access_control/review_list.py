from rbac import USERS, ROLES
from exception_policy import EXCEPTIONS


def role_entries(user, info):
    """사용자 한 명이 역할로 받은 권한을 현황의 권한 한 건씩 만들어 목록으로 리턴한다."""
    role = info["role"]
    entries = []

    for permission in ROLES.get(role, []):
        entry = {
            "user": user,
            "permission": permission,
            "source": f"역할 {role}",
            "employed": info["employed"]
        }
        entries.append(entry)

    return entries

def build_access_list():
    access_list = []

    # 1. 역할로 받은 권한 수집
    for user, info in USERS.items():
        access_list = access_list + role_entries(user, info)

    # 2. 예외로 받은 권한 수집
    for exception in EXCEPTIONS:
        user = exception["user"]

        entry = {
            "user": user,
            "permission": exception["permission"],
            "source": f"예외 {exception['id']}번",
            "employed": USERS[user]["employed"]
        }

        entry["expires"] = exception["expires"]
        access_list.append(entry)

    return access_list