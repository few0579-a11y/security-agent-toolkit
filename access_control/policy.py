from rbac import check_permission
from exception_policy import find_exception


def evaluate_access(user, resource, action, now):
    """(허용 여부, 이유)를 리턴한다."""

    # 1. check_permission으로 역할 권한 판정
    ok, reason = check_permission(user, resource, action)
    # 2. 역할 권한으로 허용되면 True 반환
    if ok == True : # if ok: 로 생략 가능.
        return True, "역할 권한"    
    # 3. 권한 없음 이외의 이유로 거부되면 즉시 거부
    if reason != "권한 없음":
        return False, reason
    # 4. find_exception으로 유효한 예외 권한 확인
    found, exc_id = find_exception(user, f"{resource}:{action}", now)
    # 5. 유효한 예외가 있으면 True 반환
    if found :
        return True, f"예외 {exc_id}번"
    # 6. 모두 해당하지 않으면 권한 없음으로 거부
    return False, "권한 없음"