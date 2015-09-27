#!/usr/bin/env python
# encoding: utf-8

from random import randrange, sample, choice

temp = """{{
  "pk": {pk},
  "model": "bp_cupid.student",
  "fields": {{
    "mat_nr": {mat_nr},
    "vorname": "{vorname}",
    "name": "{name}",
    "weiblich": {weiblich},
    "verwaltungszeitraum": 1,
    "landkreise": {landkreise},
    "kinder": {kinder},
    "kompl": {kompl},
    "sport": {sport},
    "sono": {sono},
    "hohe_duene": {hohe_duene},
    "gewichtung_sport": {gewichtung_sport},
    "gewichtung_kompl": {gewichtung_kompl},
    "gewichtung_kinder": {gewichtung_kinder},
    "gewichtung_sono": {gewichtung_sono},
    "gewichtung_hohe_duene": {gewichtung_hohe_duene},
    "fs_und_fahrzeug": {fs_und_fahrzeug},
    "priv_unterkunft": {priv_unterkunft},
    "entfernte_praxis_wenn_unterkunft": {entfernte_praxis}
  }}
}}"""
tf = ['true', 'false']
mat_start = [4, 5, 6, 7, 8, 209, 210, 211, 212, 213, 214]

def erzeuge_zufaelligen_student(line, pk, weiblich, end=None):
    mat_nr = (
        str(choice(mat_start))
        + '2'
        + '{:05}'.format(randrange(10**5))
    )

    vorname, name = line.split()

    kinder = choice(tf)
    if kinder == 'true':
        gewichtung_kinder = randrange(1, 4)
    else:
        gewichtung_kinder = 0
    kompl = choice(tf)
    if kompl == 'true':
        gewichtung_kompl = randrange(1, 4)
    else:
        gewichtung_kompl = 0
    sport = choice(tf)
    if sport == 'true':
        gewichtung_sport = randrange(1, 4)
    else:
        gewichtung_sport = 0
    sono = choice(tf)
    if sono == 'true':
        gewichtung_sono = randrange(1, 4)
    else:
        gewichtung_sono = 0
    hohe_duene = choice(tf)
    if hohe_duene == 'true':
        gewichtung_hohe_duene = randrange(1, 4)
    else:
        gewichtung_hohe_duene = 0

    if end:
        temp_end = end
    else:
        temp_end = ',\n'

    print(
        temp.format(
            pk=pk,
            mat_nr=mat_nr,
            vorname=vorname,
            name=name,
            weiblich=weiblich,
            landkreise=sorted(sample(range(1, 11), 3)),
            kinder=kinder,
            gewichtung_kinder=gewichtung_kinder,
            kompl=kompl,
            gewichtung_kompl=gewichtung_kompl,
            sport=sport,
            gewichtung_sport=gewichtung_sport,
            sono=sono,
            gewichtung_sono=gewichtung_sono,
            hohe_duene=hohe_duene,
            gewichtung_hohe_duene=gewichtung_hohe_duene,
            fs_und_fahrzeug=choice(tf),
            priv_unterkunft=choice(tf),
            entfernte_praxis=choice(tf),
        ),
        end=temp_end,
    )

def main():
    pk = 1
    print('[')

    with open('weibliche_studenten.txt') as f:
        for line in f:
            erzeuge_zufaelligen_student(
                line=line,
                pk=pk,
                weiblich='true',
            )
            pk += 1

    with open('maennliche_studenten.txt') as f:
        lines = f.readlines()
        last_line = lines[-1]

        for line in lines:
            if line is last_line:
                erzeuge_zufaelligen_student(
                    line=line,
                    pk=pk,
                    weiblich='false',
                    end='\n',
                )
            else:
                erzeuge_zufaelligen_student(
                    line=line,
                    pk=pk,
                    weiblich='false',
                )

            pk += 1
    print(']')

if __name__ == '__main__':
    main()
