zvirata = ["pes", "kočka", "králík"]     # seznam tří řetězců

print(zvirata[0])                         # první prvek: pes
print(zvirata[-1])                        # poslední prvek: králík

zvirata[1] = "křeček"                     # přepsání druhého prvku
zvirata.append("kůň")                     # přidání na konec

print(len(zvirata))                       # počet prvků: 4
print(zvirata)                            # vypíše celý seznam v hranatých závorkách
