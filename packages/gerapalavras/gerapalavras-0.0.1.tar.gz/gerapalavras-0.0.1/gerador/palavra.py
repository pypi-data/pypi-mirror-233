import random

consoantes = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
vogais = ['a','e','i','o','u']

def gerar():
    palavra = ""

    for i in range (2):
        letra1 = random.choice(consoantes)
        letra2 = random.choice(vogais)
        palavra+=letra1
        palavra+=letra2
    return palavra