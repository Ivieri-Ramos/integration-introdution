import math
import csv

def ler_e_verificar_dados(caminho_arquivo):
    vetor_x = []
    vetor_fx = []
    
    try:
        arquivo = open(caminho_arquivo, 'r', encoding='utf-8')
    except FileNotFoundError:
        raise ValueError(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        
    delta_x_referencia = None
    
    with arquivo:
        leitor = csv.reader(arquivo, delimiter=';')
        for partes in leitor:
            if len(partes) == 2:
                try:
                    novo_x = float(partes[0])
                    novo_fx = float(partes[1])
                except ValueError:
                    continue
                
                if len(vetor_x) > 0:
                    delta_atual = novo_x - vetor_x[-1]
                    
                    if len(vetor_x) == 1:
                        delta_x_referencia = delta_atual
                    else:
                        if not math.isclose(delta_atual, delta_x_referencia, abs_tol=1e-5):
                            raise ValueError("Erro: impossibilidade de continuar por causa dos dados irregulares.")
                
                vetor_x.append(novo_x)
                vetor_fx.append(novo_fx)
                
    return vetor_x, vetor_fx