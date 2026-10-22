from rbac import check_permission, ROLES, USERS
from access_log import LOG

allowed = 0     # 허용된 요청 건수
denied = 0      # 거부된 요청 건수
counts = {}     # 사용자별 허용, 거부 건수
used = {}       # 역할별 실제 사용한 권한 목록

# ← 1부: 기록을 하나씩 판정하고 건수와 사용 권한 모으기
for log_id,time, user,resource, action in LOG:
    ok,reason = check_permission(user,resource,action)

    if ok == True: # if ok: 이것도 가능.
        allowed += 1

        # 여기에 사용자별 허용 건수 추가
        counts[user+" 허용"] = counts.get(user+" 허용", 0) + 1

print("허용", allowed, "거부", denied)
print(counts)


# ← 2부: 사용하지 않은 권한 찾기
