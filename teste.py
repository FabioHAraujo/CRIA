def main():
    # Compilador C.R.I.A

    x = 0
    y = 0
    resultado = 0
    i = 0

    x = int(input('Informe a variável x: '))
    y = int(input('Informe a variável y: '))
    if x > y:
        print("X é maior que Y")
    else:
        print("Y é maior ou igual a X")
    for i in range(1, 20 + 1):
        resultado = resultado + i
    while x < 100:
        x = x + 10
    x = int(input('Informe a variável x: '))
    print(resultado)

if __name__ == '__main__':
    main()
