
name = "p0w8rk2mzq.xyz"
label = name.split(".")[-2]

digits = 0
vowels = 0

for ch in label:
    if ch in "0123456789":
        digits = digits + 1
    if ch in "aeiou":
        vowels = vowels + 1

print(label, len(label), digits, vowels)
