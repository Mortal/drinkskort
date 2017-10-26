import random
import subprocess


names = '''
Anaconda
Belloq
Big Boulder
Crucifix
Crystal Skull Special
Den Hellige Gral
Disneyland
Dr. Jones
Gun to a knife fight
Han Solo
INKAs Hemmelighed
Krystalkraniets Kongehue
Lady Marion
Luftwaffe
Nazi-guld
Ophidiofobi
Pyramidens Hemmelighed
Raiders of the Lost Ark
The Last Crusade
The Lost Ark
Temple of Doom
Tomb Raider
Zeppelineren
'''.strip().splitlines()

rng = random.Random(1234)
rng2 = random.Random(1235)

# Drinks der indeholder "Vodka"
vodka = [0, 5, 8, 9, 14, 15, 20]

def swap(i, j):
    shuffled[i], shuffled[j] = shuffled[j], shuffled[i]

for i in range(10):
    with open('tutorfest2017.txt') as fp, open('tutorfest2017-%s.txt' % i, 'w') as fp2:
        shuffled = list(names)
        rng.shuffle(shuffled)

        swap(shuffled.index('Luftwaffe'), 4 if i % 2 else 11)
        swap(shuffled.index('Crystal Skull Special'),
             rng2.choice(vodka))

        j = 0
        for line in fp:
            if line.startswith('= '):
                orig = line.strip('\n =')
                line = '= %s (%s)\n' % (shuffled[j], orig)
                j += 1
            fp2.write(line)
    subprocess.check_call(('make', 'fest=tutorfest2017-%s' % i, 'columns=gratis', 'all'))
subprocess.check_call(['pdfjoin'] + ['mixing_tutorfest2017-%s.pdf' % i for i in range(10)] + ['-o', 'mixing_tutorfest2017.pdf'])
