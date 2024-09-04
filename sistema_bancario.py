from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    
    def __str__(self):
        return f"""\
            Nome: {self.nome}
            Data de Nascimento: {self.data_nascimento}
            CPF: {self.cpf}
            Endereço: {self.endereco}
        """

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > 0:
            if self._saldo >= valor:
                self._saldo -= valor
                print(f"\nO saque de R$ {valor:.2f} foi realizado com sucesso!")
                return True
            else:
                print(f"\nNão é possível realizar o saque no valor de R$ {valor:.2f}, pois o saldo é insuficiente!")
        else:
            print("\nNão é possível realizar um saque zerado ou negativo!")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nO depósito de R$ {valor:.2f} foi realizado com sucesso!")
        else:
            print("\nNão é possível realizar um depósito zerado ou negativo!")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        if numero_saques >= self.limite_saques:
            print("\nVocê atingiu o limite máximo de saques diários!")

        elif valor > self.limite:
            print("\nNão é possível realizar um saque acima de R$ 500,00!")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            Número da Conta: {self.numero}
            Usuário: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.depositar(self.valor)

        if transacao_realizada:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_realizada = conta.sacar(self.valor)

        if transacao_realizada:
            conta.historico.adicionar_transacao(self)

def realizar_acao(usuarios_cadastrados, tipo):
    cpf = str(input("Informe o CPF (Com ou sem pontuação): ")).replace(".", "").replace("-", "")
    usuario = identificar_usuario(usuarios_cadastrados, cpf)

    if not usuario:
        print(f"\nO usuário com o CPF {cpf} não existe no sistema!")
        return
    
    valor = float(input(f"Informe o valor do {("depósito" if tipo == "depósito" else "saque")}: "))
    transacao = Deposito(valor) if tipo == "depósito" else Saque(valor)

    conta = recuperar_conta_usuario(usuario)

    if not conta:
        return
    
    usuario.realizar_transacao(conta, transacao)

def recuperar_conta_usuario(usuario):
    if not usuario.contas:
        print("\n O Usuário não possui uma conta!")
        return

    return usuario.contas[0]

def exibir_extrato(usuarios_cadastrados):
    cpf = str(input("Informe o CPF (Com ou sem pontuação): ")).replace(".", "").replace("-", "")
    usuario = identificar_usuario(usuarios_cadastrados, cpf)

    if not usuario:
        print(f"\nO usuário com o CPF {cpf} não existe no sistema!")
        return
    
    conta = recuperar_conta_usuario(usuario)

    if not conta:
        return

    print("---------------EXTRATO---------------")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: R$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
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

    usuario = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    usuarios_cadastrados.append(usuario)

    print(f"\nO usuário {nome} foi criado com sucesso!")

def identificar_usuario(usuarios_cadastrados, cpf):
    usuarios_identificados = [usuario for usuario in usuarios_cadastrados if usuario.cpf == cpf]
    return usuarios_identificados[0] if usuarios_identificados else None

def criar_conta_corrente(numero_conta, usuarios_cadastrados, contas_correntes_cadastradas):
    cpf = str(input("Informe o CPF do usuário (Com ou sem pontuação): ")).replace(".", "").replace("-", "")
    usuario = identificar_usuario(usuarios_cadastrados, cpf)

    if not usuario:
        print(f"\nO usuário com o CPF {cpf} não existe no sistema!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta)
    contas_correntes_cadastradas.append(conta)
    usuario.contas.append(conta)

    print(f"\nA conta corrente {numero_conta} foi criada e vinculada ao usuário de CPF {cpf} com sucesso!")

def listar_usuarios(usuarios_cadastrados):
    print("---------------USUÁRIOS CADASTRADOS---------------")
    print("Não foram cadastrados novos usuários." if not usuarios_cadastrados else "")
    for usuario in usuarios_cadastrados:
        print(str(usuario))
    print("--------------------------------------------------")

def listar_contas_correntes(contas_correntes_cadastradas):
    print("---------------CONTAS CORRENTES CADASTRADAS---------------")
    print("Não foram cadastrados novas contas correntes." if not contas_correntes_cadastradas else "")
    for conta in contas_correntes_cadastradas:
        print(str(conta))
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
    usuarios_cadastrados = []
    contas_correntes_cadastradas = []

    while True:

        opcao = input(menu())

        if opcao == "1":
            realizar_acao(usuarios_cadastrados, "depósito")

        elif opcao == "2":
            realizar_acao(usuarios_cadastrados, "saque")

        elif opcao == "3":
            exibir_extrato(usuarios_cadastrados)

        elif opcao == "4": 
            criar_usuario(usuarios_cadastrados)

        elif opcao == "5":
            numero_conta = len(contas_correntes_cadastradas) + 1
            criar_conta_corrente(numero_conta, usuarios_cadastrados, contas_correntes_cadastradas)

        elif opcao == "6":
            listar_usuarios(usuarios_cadastrados)

        elif opcao == "7":
            listar_contas_correntes(contas_correntes_cadastradas)

        elif opcao == "8":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()