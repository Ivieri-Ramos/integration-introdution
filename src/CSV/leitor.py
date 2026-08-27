class Node:
    def __init__(self, x, fx):
        self.x = x
        self.fx = fx
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def inserir_no_final(self, x, fx):
        novo_no = Node(x, fx)

        if self.head is None:
            self.head = novo_no
            return

        temp = self.head
        while temp.next is not None:
            temp = temp.next
        temp.next = novo_no

    def imprimir_lista(self):
        temp = self.head
        print("\n--- Dados Carregados da Lista ---")
        while temp is not None:
            print(f"x: {temp.x:8.4f}  |  f(x): {temp.fx:8.4f}")
            temp = temp.next
        print("---------------------------------")


def main():
    lista = LinkedList()

    try:
        with open("dados.csv", "r") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(",")

                if len(partes) == 2:
                    try:
                        x = float(partes[0])
                        fx = float(partes[1])
                        lista.inserir_no_final(x, fx)
                    except ValueError:
                        pass
    except FileNotFoundError:
        print("Erro: Nao foi possivel abrir o arquivo 'dados.csv'.")
        return

    lista.imprimir_lista()


if __name__ == "__main__":
    main()