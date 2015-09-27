#!/usr/bin/env python
# encoding: utf-8

from random import randrange, sample, choice

def main():
    temp = """{{
  "pk": {pk},
  "model": "bp_cupid.praxis",
  "fields": {{
    "vorname": "{vorname}",
    "name": "{name}",
    "landkreis": {landkreis},
    "zeitraeume": {zeitraeume},
    "kinder": {kinder},
    "kompl": {kompl},
    "sport": {sport},
    "sono": {sono},
    "plz": {plz},
    "nur_mit_auto": {nur_mit_auto},
    "freie_unterkunft": {freie_unterkunft},
    "billige_unterkunft": {billige_unterkunft}
  }}
}}"""
    tf = ['true', 'false']
    plzs = (
        list(range(17160, 17180))
        + list(range(18000, 18099))
        + list(range(18200, 18259))
        + list(range(18260, 18349))
        + list(range(19000, 19102))
        + list(range(19220, 19249))
        + list(range(19380, 19400))
        + list(range(23950, 24000))
    )
    pk = 1

    with open('arztnamen.txt') as f:
        lines = f.readlines()
        last_line = lines[-1]

        print('[')

        for line in lines:
            vorname, name = line.split()

            if line is last_line:
                end='\n'
            else:
                end=',\n'

            print(
                temp.format(
                    pk=pk,
                    vorname=vorname,
                    name=name,
                    landkreis=randrange(1, 11),
                    zeitraeume=sorted(sample(range(1, 10), randrange(10))),
                    kinder=choice(tf),
                    kompl=choice(tf),
                    sport=choice(tf),
                    sono=choice(tf),
                    plz=choice(plzs),
                    nur_mit_auto=choice(tf),
                    freie_unterkunft=choice(tf),
                    billige_unterkunft=choice(tf)
                ),
                end=end
            )
            pk += 1

        print(']')

if __name__ == '__main__':
    main()
