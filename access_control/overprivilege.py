
def entry_key(entry):                                            # 현황의 권한 한 건의 식별 키를 만드는 함수
    """현황의 권한 한 건(또는 그 복사본)의 식별 키(user:permission:source 를 이어 붙인 글자)를 리턴한다."""
    return entry["user"] + ":" + entry["permission"] + ":" + entry["source"]   # 세 값을 : 로 이어 붙인다


def make_stale_reason(stale):                                    # 규칙에 걸린 권한 목록을 받는 함수
    """규칙에 걸린 권한의 식별 키를 키로, 걸린 이유를 값으로 하는 딕셔너리를 리턴한다."""
    stale_reason = {}                                            # 식별 키 → 걸린 이유를 담을 빈 딕셔너리
    for item in stale:                                           # 규칙에 걸린 권한을 하나씩 꺼낸다
        stale_reason[entry_key(item)] = item["reason"]           # 식별 키로 걸린 이유를 찾을 수 있게 담는다
    return stale_reason                                          # 딕셔너리를 리턴한다


def make_unused_keys(unused):                                    # 안 쓴 권한 목록을 받는 함수
    """안 쓴 권한의 식별 키를 담은 목록을 리턴한다."""
    unused_keys = []                                             # 안 쓴 권한의 식별 키를 담을 빈 목록
    for item in unused:                                          # 안 쓴 권한을 하나씩 꺼낸다
        unused_keys.append(entry_key(item))                      # 식별 키를 목록에 추가한다
    return unused_keys                                           # 목록을 리턴한다


def generate_report(access_list, stale, unused, days, generated_at):   # 현황 · 규칙 결과 · 안 쓴 결과 · 기준 일 수 · 만든 시각 글자를 받는 함수
    """과다권한 후보 리포트(딕셔너리)를 리턴한다. 후보마다 "reasons" 키에 이유 목록을 적는다."""
    stale_reason = make_stale_reason(stale)                      # 규칙에 걸린 권한의 식별 키 → 걸린 이유 딕셔너리를 만든다(미리 채움)
    unused_keys = make_unused_keys(unused)                       # 안 쓴 권한의 식별 키 목록을 만든다(미리 채움)
    findings = []                                                # 후보를 담을 빈 목록
    for entry in access_list:                                    # 현황의 권한을 한 건씩 꺼낸다
        key = entry_key(entry)                                   # 그 권한의 식별 키를 만든다
        reasons = []                                             # 이유를 담을 빈 목록
        if key in stale_reason:                                  # 규칙에 걸린 권한이면
            reasons.append(stale_reason[key])                    # 걸린 이유를 추가한다
        if key in unused_keys:                                   # 안 쓴 권한이면
            reasons.append(f"{days}일 넘게 안 씀(이력 없음 포함)")   # 안 쓴 이유를 추가한다
        if len(reasons) > 0:                                     # 이유가 하나라도 있으면
            finding = entry.copy()                               # 권한을 복사해서
            finding["reasons"] = reasons                         # 복사본에 이유 목록을 적고
            findings.append(finding)                             # 후보에 추가한다
    return {"generated_at": generated_at, "total": len(access_list), "finding_count": len(findings), "findings": findings}   # 리포트를 리턴한다
