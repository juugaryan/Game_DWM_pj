n = int(input("n = "))
emails = [input() for _ in range(n)]

m = int(input("m = "))
names = [input for _ in range(m)]

for name in names:
    index = ""
    while True:
        email = "%s%s@untitled.py" % (name, index)
        if email not in emails:
            emails.append(email)
            print(email)
            break
        index = index + 1 if index else 1