
LOG = [
    ("mail.naver.com", "NOERROR"),
    ("x7q9pz2kd.top", "NXDOMAIN"),
    ("login-kbbank.xyz", "NOERROR"),
    ("cdn.cloudflare.com", "NOERROR"),
    ("zq8w4n6r1m.tk", "NXDOMAIN")
]

for name, rcode in LOG:
    parts = name.split(".")
    score = 0

    if len(parts[-2]) >= 10:
        score = score + 1

    if parts[-1] in ["top", "xyz", "tk"]:
        score = score + 1

    if rcode == "NXDOMAIN":
        score = score + 2

    print(name, score, score >= 3)

