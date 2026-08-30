from dataclasses import dataclass
import csv

@dataclass(frozen=True)
class CSVDataDTO:
    vector_x: list[float]
    vector_y: list[float]

def ler_dados_csv(caminho_arquivo) -> CSVDataDTO:
    vetor_x, vetor_fx = [], []

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')

            next(leitor, None)

            for num_linha, partes in enumerate(leitor, start=2):
                if not partes:
                    continue

                if len(partes) != 2:
                    raise ValueError(f"Erro na linha {num_linha}: esperava 2 colunas, mas encontrou {len(partes)}.")

                try:
                    novo_x = float(partes[0].replace(',', '.'))
                    novo_fx = float(partes[1].replace(',', '.'))
                except ValueError:
                    raise ValueError(f"Erro na linha {num_linha}: dado inválido detectado ({partes[0]}; {partes[1]}).")

                vetor_x.append(novo_x)
                vetor_fx.append(novo_fx)

    except FileNotFoundError:
        raise ValueError(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")

    return CSVDataDTO(vetor_x, vetor_fx)