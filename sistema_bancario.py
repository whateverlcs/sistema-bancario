def realizar_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito realizado no valor de R$ {valor:.2f}\n"
        print(f"\nO depósito de R$ {valor:.2f} foi realizado com sucesso!")
    else:
        print("\nNão é possível realizar um depósito zerado ou negativo!")
    
    return saldo, extrato

def realizar_saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("\nVocê atingiu o limite máximo de saques diários!")

    elif valor > 0:
        if valor <= limite:
            if saldo >= valor:
                saldo -= valor
                extrato += f"Saque realizado no valor de R$ {valor:.2f}\n"
                numero_saques += 1
                print(f"\nO saque de R$ {valor:.2f} foi realizado com sucesso!")
            else:
                print(f"\nNão é possível realizar o saque no valor de R$ {valor:.2f}, pois o saldo é insuficiente!")
        else:
            print("\nNão é possível realizar um saque acima de R$ 500,00!")  
    else:
        print("\nNão é possível realizar um saque zerado ou negativo!")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("---------------EXTRATO---------------")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print("-------------------------------------")

def criar_usuario(usuarios_cadastrados):
    cpf = str(input("Informe o CPF (Com ou sem pontuação): ")).replace(".", "").replace("-", "")
    usuario = identificar_usuario(usuarios_cadastrados, cpf)

    if usuario:
        print(f"\nO usuário com o CPF {cpf} já existe no sistema!")
        return

    nome = str(input("Informe o nome do usuário: "))
    data_nascimento = str(input("Informe a data de nascimento (dd-mm-aaaa): "))
    endereco = str(input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "))

    usuarios_cadastrados.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(f"\nO usuário {nome} foi criado com sucesso!")

def identificar_usuario(usuarios_cadastrados, cpf):
    usuarios_identificados = [usuario for usuario in usuarios_cadastrados if usuario["cpf"] == cpf]
    return usuarios_identificados[0] if usuarios_identificados else None

def criar_conta_corrente(agencia, numero_conta, usuarios_cadastrados, contas_correntes_cadastradas):
    cpf = str(input("Informe o CPF do usuário (Com ou sem pontuação): ")).replace(".", "").replace("-", "")
    usuario = identificar_usuario(usuarios_cadastrados, cpf)

    if not usuario:
        print(f"\nO usuário com o CPF {cpf} não existe no sistema!")
        return
    
    contas_correntes_cadastradas.append({"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario})
    print(f"\nA conta corrente {numero_conta} foi criada e vinculada ao usuário de CPF {cpf} com sucesso!")

def listar_usuarios(usuarios_cadastrados):
    print("---------------USUÁRIOS CADASTRADOS---------------")
    print("Não foram cadastrados novos usuários." if not usuarios_cadastrados else "")
    for usuario in usuarios_cadastrados:
        print(f"""
            Nome: {usuario['nome']}
            Data de Nascimento: {usuario['data_nascimento']}
            CPF: {usuario['cpf']}
            Endereço: {usuario['endereco']}
        """)
    print("--------------------------------------------------")

def listar_contas_correntes(contas_correntes_cadastradas):
    print("---------------CONTAS CORRENTES CADASTRADAS---------------")
    print("Não foram cadastrados novas contas correntes." if not contas_correntes_cadastradas else "")
    for conta in contas_correntes_cadastradas:
        print(f"""
            Agência: {conta['agencia']}
            Número da conta: {conta['numero_conta']}
            Usuário: {conta['usuario']['nome']}
        """)
    print("----------------------------------------------------------")

def menu():
    return """\n
----------------------BEM VINDO AO BANCO X-------------------
[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta Corrente
[6] Listar Usuários
[7] Listar Contas Correntes
[8] Sair
=> """

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    numero_conta = 0
    AGENCIA = "0001"
    usuarios_cadastrados = []
    contas_correntes_cadastradas = []

    while True:

        opcao = input(menu())

        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = realizar_deposito(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = realizar_saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4": 
            criar_usuario(usuarios_cadastrados)

        elif opcao == "5":
            numero_conta = len(contas_correntes_cadastradas) + 1
            criar_conta_corrente(AGENCIA, numero_conta, usuarios_cadastrados, contas_correntes_cadastradas)

        elif opcao == "6":
            listar_usuarios(usuarios_cadastrados)

        elif opcao == "7":
            listar_contas_correntes(contas_correntes_cadastradas)

        elif opcao == "8":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()