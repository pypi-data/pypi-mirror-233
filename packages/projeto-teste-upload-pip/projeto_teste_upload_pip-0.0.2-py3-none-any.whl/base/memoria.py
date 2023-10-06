def limpar_arquivo():
    with open('base_palavras.txt', 'w'):
        # não é preciso fazer nada
        # abrir o arquivo em modo write já o limpará
        pass


# p = palavra
def armazenar_palavra(p):
    # a = arquivo
    with open('base_palavras.txt', 'a') as a:
        a.write(p + '\n')


def ler_palavras():
    # a = arquivo
    with open('base_palavras.txt', 'r') as a:
        for linha in a:
            print(linha.strip())
