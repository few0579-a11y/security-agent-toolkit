name = "www.example.com"
parts = name.split(".")

print(parts[-1])
print(".".join(parts[-2:]))
print(list(reversed(parts)))
