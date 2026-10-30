from review_list import build_access_list

access_list = build_access_list()

print("--- 단계 1: 현황 - 부여돼 있는 권한", len(access_list), "건")
for entry in access_list:
    print(entry["user"], entry["permission"], "<-", entry["source"], "| 재직", entry["employed"])

print("--- 단계 2: 점검 - 사용자별 권한 개수")
counts = {}
for entry in access_list:
    counts[entry["user"]] = counts.get(entry["user"], 0) + 1
print(counts)