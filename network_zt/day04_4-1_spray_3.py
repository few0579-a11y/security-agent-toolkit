LOG = [
    ("185.220.101.4", "kim", "fail"),
    ("185.220.101.4", "lee", "fail"),
    ("185.220.101.4", "park", "fail"),
    ("185.220.101.4", "choi", "fail"),
    ("211.36.10.7", "kim", "success"),
    ("121.134.5.9", "lee", "fail"),
    ("121.134.5.9", "lee", "fail"),
    ("121.134.5.9", "lee", "success"),
    ("45.155.205.9", "han", "fail"),
    ("45.155.205.9", "seo", "fail"),
]

failed = {}

for ip, user, result in LOG:
    if result == "fail":
        users = failed.get(ip, [])
        if user not in users:
            users.append(user)
        failed[ip] = users

for ip in failed:
    if len(failed[ip]) >= 3:
        print(ip, len(failed[ip]), failed[ip])