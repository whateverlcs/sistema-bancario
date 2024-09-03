menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
 
=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito realizado no valor de R$ {valor:.2f}\n"
        else:
            print("Não é possível realizar um depósito zerado ou negativo!")

    elif opcao == "s":
        if numero_saques >= LIMITE_SAQUES:
            print("Você atingiu o limite máximo de saques diários!")
            continue

        valor = float(input("Informe o valor do saque: "))

        if valor > 0:
            if valor <= 500:
                if saldo >= valor:
                    saldo -= valor
                    extrato += f"Saque realizado no valor de R$ {valor:.2f}\n"
                    numero_saques += 1
                else:
                    print(f"Não é possível realizar o saque no valor de R$ {valor:.2f}, pois o saldo é insuficiente!")
            else:
                print("Não é possível realizar um saque acima de R$ 500,00!")  
        else:
            print("Não é possível realizar um saque zerado ou negativo!")

    elif opcao == "e":
        print("---------------EXTRATO---------------")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("-------------------------------------")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")