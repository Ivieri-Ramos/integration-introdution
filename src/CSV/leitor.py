import math
import os

def ler_e_verificar_dados(caminho_pasta):
    vetor_x = []
    vetor_fx = []
    
    if not os.path.isdir(caminho_pasta):
        print(f"Erro: A pasta '{caminho_pasta}' não foi encontrada.")
        return [], []
        
    arquivos_na_pasta = os.listdir(caminho_pasta)
    arquivos_csv = [f for f in arquivos_na_pasta if f.endswith('.csv')]
    
    if not arquivos_csv:
        print(f"Erro: Nenhum arquivo .csv foi encontrado dentro da pasta '{caminho_pasta}'.")
        return [], []
        
    caminho_arquivo = os.path.join(caminho_pasta, arquivos_csv[0])
    
    delta_x_referencia = None
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(';')
            
            if len(partes) == 2:
                try:
                    novo_x = float(partes[0])
                    novo_fx = float(partes[1])
                    
                    if len(vetor_x) > 0:
                        delta_atual = novo_x - vetor_x[-1]
                        
                        if len(vetor_x) == 1:
                            delta_x_referencia = delta_atual
                        else:
                            if not math.isclose(delta_atual, delta_x_referencia, abs_tol=1e-5):
                                print("Erro: impossibilidade de continuar por causa dos dados irregulares.")
                                return [], []
                    
                    vetor_x.append(novo_x)
                    vetor_fx.append(novo_fx)
                    
                except ValueError:
                    pass
                    
    return vetor_x, vetor_fx

def main():
    x, fx = ler_e_verificar_dados(r"integral-simpson\integration-introdution\Assets")
    
    if x and fx:
        print("\n--- Correspondência por Índices ---")
        for i in range(len(x)):
            print(f"Índice {i}: x = {x[i]:8.4f}  |  f(x) = {fx[i]:8.4f}")

if __name__ == "__main__":
    main()