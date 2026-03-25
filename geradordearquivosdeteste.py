import os
import time
import random
import string


# ===============================
# Geração de arquivos de teste
# ===============================

def gerar_arquivos(pasta, qtd_arquivos=50, linhas_por_arquivo=200):
    os.makedirs(pasta, exist_ok=True)

    palavras = ["erro", "warning", "info", "processo", "dados", "sistema"]

    for i in range(qtd_arquivos):
        with open(os.path.join(pasta, f"arquivo_{i}.txt"), "w", encoding="utf-8") as f:
            for _ in range(linhas_por_arquivo):
                linha = " ".join(random.choices(palavras, k=20))
                f.write(linha + "\n")


if __name__ == "__main__":
    pasta = "log2"

    print("Gerando arquivos de teste...")
    gerar_arquivos(pasta, qtd_arquivos=1000, linhas_por_arquivo=10000)