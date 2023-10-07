grouping = 0x00001000
for session_start in range(0, int(0xffffffff / grouping) + 1):
    print(range(session_start * grouping, (session_start + 1) * grouping ))
