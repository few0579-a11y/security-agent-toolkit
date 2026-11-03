
import pandas as pd

EVENTS_PATH = "normalized_events.json"
FAILED_PATH = "failed_events.csv"


def load_events(path):
    """JSON 파일을 DataFrame으로 읽는다."""
    events = pd.read_json(path)
    return events


def pick_failed(events):
    """실패한 이벤트만 추출한다."""
    results = events["result"]
    is_fail = results == "실패"
    failed = events[is_fail]
    return failed


def count_by_user(failed):
    """사용자별 실패 횟수를 많은 순서로 정렬한다."""
    grouped = failed.groupby("user")
    counts = grouped.size()
    sorted_counts = counts.sort_values(ascending=False)
    return sorted_counts


def add_hour(events):
    """이벤트 발생 시각에서 시간(hour)을 추출한다."""
    times = pd.to_datetime(events["time"])
    hours = times.dt.hour
    events["hour"] = hours
    return events


def count_by_hour(failed):
    """시간대별 실패 횟수를 계산한다."""
    grouped = failed.groupby("hour")
    counts = grouped.size()
    return counts


def save_failed(failed, path):
    """실패한 이벤트를 CSV 파일로 저장한다."""
    failed.to_csv(path, index=False)
