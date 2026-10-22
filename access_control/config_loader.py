import json

def load_json(path, default):
    """JSON 파일을 읽어 리턴한다. 파일이 없거나 깨졌으면 경고를 출력하고 default를 리턴한다."""

    # 1. try로 시작한다
    try:
    # 2. with open으로 파일을 연다
        with open(path, encoding="utf-8") as f:
    # 3. json.load로 읽은 내용을 리턴한다
            return json.load(f)
    # 4. 파일이 없을 때 예외 처리
    except FileNotFoundError:
        print("[경고] 설정 파일 없음:", path)
        return default
    # 5. JSON이 깨졌을 때 예외 처리
    except json.JSONDecodeError:
        print("[경고] 설정 파일 깨짐:", path)
        return default