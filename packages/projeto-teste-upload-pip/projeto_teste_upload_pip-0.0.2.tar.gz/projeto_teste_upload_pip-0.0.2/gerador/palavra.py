import random
from base import memoria

silabas = ['ba', 'be', 'bi', 'bo', 'bu',
           'ca', 'ce', 'ci', 'co', 'cu',
           'da', 'de', 'di', 'do', 'du',
           'fa', 'fe', 'fi', 'fo', 'fu',
           'ga', 'ge', 'gi', 'go', 'gu',
           'ha', 'he', 'hi', 'ho', 'hu',
           'ja', 'je', 'ji', 'jo', 'ju',
           'la', 'le', 'li', 'lo', 'lu',
           'ma', 'me', 'mi', 'mo', 'mu',
           'na', 'ne', 'ni', 'no', 'nu',
           'pa', 'pe', 'pi', 'po', 'pu',
           'ra', 're', 'ri', 'ro', 'ru',
           'sa', 'se', 'si', 'so', 'su',
           'ta', 'te', 'ti', 'to', 'tu',
           'va', 've', 'vi', 'vo', 'vu']


# q = quantidade
def gerar_palavra(q):
    memoria.limpar_arquivo()
    for i in range(q):
        # s = silaba
        s1 = random.choice(silabas)
        s2 = random.choice(silabas)

        # p = palavra
        p = s1 + s2

        memoria.armazenar_palavra(p)
        print(p)

    print(f'foram geradas {q} palavras')
