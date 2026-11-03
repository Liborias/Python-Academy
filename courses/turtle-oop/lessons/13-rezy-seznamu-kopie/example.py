s = [10, 20, 30, 40, 50]
print(s[:2], s[-2:], s[1:4], s[::2], s[::-1])
print(s[3:100])                     # řez mimo rozsah je v pořádku

m = [[1, 2], [3, 4]]
mala = m.copy()                     # mělká kopie
mala[0].append(99)
print(m)                            # vnitřní seznam je sdílený: [[1, 2, 99], [3, 4]]

hluboka = [radek[:] for radek in m]   # zkopírujeme i vnitřní seznamy
hluboka[1].append(77)
print(m, hluboka)
