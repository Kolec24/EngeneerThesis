from library import Engine, Stage, Rocket, Payload


def sortTen(val):
    return val[9]


def oblicz(payload, orbit, amax, wydluzenie):
    e = Engine()
    number = e.count_engines()
    p_ratio = 0
    p = Payload(payload, orbit)
    r = Rocket()
    r.fill_index(r.index_tab)
    acceleration = []
    final_mass = []
    ladunek = []
    wskaznik = 0
    wyniki = [[0 for x in range(10)] for y in range(1000)]
    licznik = 0
    Lista_wynikow = open("Wyniki.txt", 'w')
    Lista_wynikow.write(
        "Nr   Silnik - Stopien 1     Silnik - Stopien 2     Silnik - Stopien 3        Masa- Stopien 1                  Masa- Stopien 2             Masa- Stopien 3                    Masa calkowita                   Wspolczynnik ladunku platnego")
    Lista_wynikow.write("\n")

    for stg in range(1, 4):
        for i in range(0, number):
            for j in range(0, number):
                for k in range(0, number):
                    r = Rocket()
                    r.fill_index(r.index_tab)
                    r.index_tab[0] = i + 1
                    r.index_tab[1] = j + 1
                    r.index_tab[2] = k + 1
                    r.generate(p, stg, r.index_tab)
                    #                    print(len(r.stages), r.stages[0].engine1.name)
                    x = r.calculate_model(r.calculate_velocity(wydluzenie))
                    if x == True:
                        print("silniki dzialaja")
                    else:
                        #                        print("silniki nie dzialaja")
                        r.stages.clear()
                        continue
                    for l in range(0, stg):
                        acceleration.append(None)
                        ladunek.append(None)
                        final_mass.append(None)
                    w = stg - 1
                    ladunek[w] = r.payload.payload
                    while w >= 1:
                        ladunek[w - 1] = r.stages[w].empty + r.stages[w].fuel + ladunek[w]
                        w = w - 1
                    for l in range(0, stg):
                        final_mass[l] = r.stages[l].empty + ladunek[l]
                        acceleration[l] = (final_mass[l] / r.stages[l].engine1.thrust_v) / 9.81
                        if acceleration[l] > amax:
                            wskaznik = 1
                    if wskaznik > 0:
                        #                        print("Przekroczono maksymalne przyspieszenie", )
                        r.stages.clear()
                        break
                    tmp_rocket = Rocket()
                    if p_ratio < r.payload.payload / (r.empty_mass() + r.fuel_mass()):
                        tmp_rocket = r
                        p_ratio = r.payload.payload / (r.empty_mass() + r.fuel_mass())
                    if stg == 1:
                        wyniki[licznik][0] = licznik
                        wyniki[licznik][1] = r.stages[0].engine1.name
                        wyniki[licznik][2] = "brak"
                        wyniki[licznik][3] = "brak"
                        wyniki[licznik][4] = r.stages[0].empty + r.stages[0].fuel
                        wyniki[licznik][5] = "brak"
                        wyniki[licznik][6] = "brak"
                        wyniki[licznik][7] = r.stages[0].empty + r.stages[0].fuel + r.payload.payload
                        wyniki[licznik][8] = acceleration[0]
                        wyniki[licznik][9] = r.payload.payload / (r.empty_mass() + r.fuel_mass())
                        licznik = licznik + 1
                    if stg == 2:
                        wyniki[licznik][0] = licznik
                        wyniki[licznik][1] = r.stages[0].engine1.name
                        wyniki[licznik][2] = r.stages[1].engine1.name
                        wyniki[licznik][3] = "brak"
                        wyniki[licznik][4] = r.stages[0].empty + r.stages[0].fuel
                        wyniki[licznik][5] = r.stages[1].empty + r.stages[1].fuel
                        wyniki[licznik][6] = "brak"
                        wyniki[licznik][7] = r.stages[0].empty + r.stages[0].fuel + r.stages[1].empty + r.stages[
                            1].fuel + r.payload.payload
                        wyniki[licznik][8] = max(acceleration[0], acceleration[1])
                        wyniki[licznik][9] = r.payload.payload / (r.empty_mass() + r.fuel_mass())
                        licznik = licznik + 1
                    if stg == 3:
                        wyniki[licznik][0] = licznik
                        wyniki[licznik][1] = r.stages[0].engine1.name
                        wyniki[licznik][2] = r.stages[1].engine1.name
                        wyniki[licznik][3] = r.stages[2].engine1.name
                        wyniki[licznik][4] = r.stages[0].empty + r.stages[0].fuel
                        wyniki[licznik][5] = r.stages[1].empty + r.stages[1].fuel
                        wyniki[licznik][6] = r.stages[2].empty + r.stages[2].fuel
                        wyniki[licznik][7] = r.stages[0].empty + r.stages[0].fuel + r.stages[1].empty + r.stages[
                            1].fuel + r.stages[2].empty + r.stages[2].fuel + r.payload.payload
                        wyniki[licznik][8] = max(acceleration[0], acceleration[1], acceleration[2])
                        wyniki[licznik][9] = r.payload.payload / (r.empty_mass() + r.fuel_mass())
                        licznik = licznik + 1
                    r.stages.clear()
    wyniki.sort(key=sortTen, reverse=True)
    if p_ratio == 0:
        print("blad programu")
    else:
        print("wspolczynnik ladunku platoego wynosi:", p_ratio * 100, "%")

    for i in range(0, 31):
        Lista_wynikow.write(
            "'{0}'      '{1}'               '{2}'              '{3}'                '{4}'                '{5}'              '{6}'                  '{7}'                   '{8}'".format(
                wyniki[i][0], wyniki[i][1], wyniki[i][2], wyniki[i][3], wyniki[i][4], wyniki[i][5], wyniki[i][6],
                wyniki[i][7], wyniki[i][9]))
        Lista_wynikow.write('\n')
    Lista_wynikow.close()
    return wyniki
