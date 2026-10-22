import json
from datetime import datetime

with open("config/exceptions.json", encoding="utf-8") as f:

    # EXCEPTIONS : 앞에서 작성한 예외 권한 5건을 불러온 목록
    EXCEPTIONS = json.load(f)     

# TIME_FORMAT : 날짜와 시각의 형식
TIME_FORMAT = "%Y-%m-%d %H:%M"


# user : 요청한 사용자 / permission : 요청한 권한 / now : 권한을 확인하는 시각
def find_exception(user, permission, now): # 예외 권한 찾기 함수

    """유효한 예외가 있으면 (True, 예외 번호), 없으면 (False, None)을 리턴한다."""


    # 1. EXCEPTIONS에서 예외 exc를 하나씩 꺼낸다
    for exc in EXCEPTIONS:

    # 2. exc의 user와 permission이 요청과 같은지 확인한다
        if exc["user"] == user and exc["permission"] == permission:
    # 3. expires를 날짜·시각으로 변환한다
            expires = datetime.strptime(exc["expires"], TIME_FORMAT)

    # 4. now가 expires보다 앞이면 True와 예외 번호를 리턴한다
            if now < expires:
                return True, exc["id"]
    # 5. 끝까지 찾지 못했다면 False, None을 리턴한다
    
    return False, None