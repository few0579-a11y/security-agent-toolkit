from datetime import datetime                                    # 글자를 시각으로 바꾸는 데 쓴다
from config_loader import load_json                              # 10/22(목)에 만든 안전한 읽기 함수를 불러온다
from exception_policy import TIME_FORMAT                         # 시각 글자의 형식("%Y-%m-%d %H:%M")을 불러온다


def load_last_used():                                            # 사용 이력 파일을 읽어 「마지막 사용 시각」 딕셔너리를 만드는 함수
    """「사용자:권한」 글자를 키로, 마지막으로 쓴 시각 글자를 값으로 하는 딕셔너리를 리턴한다."""
    last_used_map = {}                                           # 빈 딕셔너리로 시작한다
    for log in load_json("config/access_log.json", []):          # 사용 이력을 한 건씩 꺼낸다(파일이 없으면 빈 목록)
        key = f"{log['user']}:{log['permission']}"               # 「사용자:권한」 글자를 키로 만든다
        last_used_map[key] = log["last_used"]                    # 그 키의 값에 마지막 사용 시각 글자를 담는다
    return last_used_map                                         # 딕셔너리를 리턴한다


def make_unused(entry, used_text):                               # 현황의 권한 한 건과 마지막 사용 시각 글자를 받는 함수
    """권한 한 건을 복사해 "last_used" 키(마지막 사용 시각, 이력이 없으면 None)를 적어 리턴한다. 원래 권한은 바꾸지 않는다."""
    unused_entry = entry.copy()                                  # 원래 권한은 바꾸지 않고 복사한다
    unused_entry["last_used"] = used_text                        # 복사본에 마지막 사용 시각(없으면 None)을 적는다
    return unused_entry                                          # 복사본을 리턴한다


def days_since(used_text, now):                                  # 마지막 사용 시각 글자와 지금 시각을 받는 함수
    """마지막 사용 시각 글자를 시각으로 바꿔, 지금까지 안 쓴 일 수를 리턴한다."""
    used_at = datetime.strptime(used_text, TIME_FORMAT)          # 글자를 시각으로 바꾼다
    return (now - used_at).days                                  # 지금 - 마지막 사용 시각의 일 수를 리턴한다


def find_unused(access_list, last_used_map, now, limit_days):    # 현황 · 마지막 사용 시각 딕셔너리 · 지금 시각 · 기준 일 수를 받는 함수
    """마지막 사용이 limit_days 일보다 오래됐거나 사용 이력이 없는 권한을 리턴한다. 후보마다 "last_used" 키에 마지막 사용 시각(없으면 None)을 적는다."""
    unused = []                                                  # 후보를 담을 빈 목록
    for entry in access_list:                                    # 현황의 권한을 한 건씩 꺼낸다
        key = f"{entry['user']}:{entry['permission']}"           # 그 권한의 「사용자:권한」 글자를 만든다
        used_text = last_used_map.get(key)                       # 마지막 사용 시각 글자를 꺼낸다(이력이 없으면 None)
        if used_text is None:                                    # 사용 이력이 없으면
            unused.append(make_unused(entry, None))              # 마지막 사용 시각을 None 으로 적은 복사본을 후보에 추가한다
        elif days_since(used_text, now) > limit_days:            # 사용 이력이 있고 기준 일 수보다 오래 안 썼으면
            unused.append(make_unused(entry, used_text))         # 마지막 사용 시각을 적은 복사본을 후보에 추가한다
    return unused                                                # 후보 목록을 리턴한다

def find_unused(access_list, last_used_map, now, limit_days):
    unused = []

    for entry in access_list:
        key = f"{entry['user']}:{entry['permission']}"
        used_text = last_used_map.get(key)

        if used_text is None:
            unused.append(make_unused(entry, None))

        elif days_since(used_text, now) > limit_days:
            unused.append(make_unused(entry, used_text))

    return unused