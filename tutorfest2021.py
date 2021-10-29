mapping_str = r"""
Alabama S.	Dramaqueen
Bear Grills	Trailer park
Brandbil	Sunset Boulevard
Champagnebrus	Brad Pitt
Chuck Norris	Malibu Express
Filur	12 i huen
FUAN Love	Sugardaddy
Galliano H.	\#MeToo
Hyldehans	Husk at drikke vand!
Isbjørn	Harvey Weinstein
Jim\&Lennon	City of Angles
Jägerbomb	Fake Taxi
Karamælk	Bollywood
KongFU	Paparazzi
Lille FU	Zack Snyder
Long Island	Extravagance
SpiriT	Attrappistol
Styx	Walk of Fame
Tequila S.	Rave
Tutte	Walk of Shame
White R.	Slowmotion
Vanilla Ice	Psytrance
Ginny	Produktionsassistent
Verdens bedste sommerdrink	Skovbrand
"""
mapping = dict(line.split("\t") for line in mapping_str.strip().splitlines())

with open("tutorfest2017.txt") as fp, open("tutorfest2021.txt", "w") as ofp:
    for line in fp:
        if line.startswith("= "):
            ofp.write("= %s%s" % (mapping[line[2:].strip()], line))
        else:
            ofp.write(line)
