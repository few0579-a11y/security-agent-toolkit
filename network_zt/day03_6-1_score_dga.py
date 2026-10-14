name = "p0w8rk2mzq.xyz"
rcode = "NXDOMAIN"

parts = name.split(".")
score = 0

if len(parts[-2]) >= 10:
    score = score + 1

if parts[-1] in ["top", "xyz", "tk"]:
    score = score + 1

if rcode == "NXDOMAIN":
    score = score + 2

print(name, score, score >= 3)
