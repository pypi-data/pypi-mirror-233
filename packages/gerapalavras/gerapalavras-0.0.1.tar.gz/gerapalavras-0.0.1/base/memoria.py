def armazenar(palavra):
    with open ('base_palavras.txt','a') as arq:
        arq.write(f'{palavra}-')

def visualizar():
    with open ('base_palavras.txt','r') as arq:
        print(arq.read())