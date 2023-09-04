def teste(x):
    return x + "a"
lista1 = ['oi', 'ou', 'ai', 'ae']

lista2 = list(map(teste, lista1))

print(lista2)