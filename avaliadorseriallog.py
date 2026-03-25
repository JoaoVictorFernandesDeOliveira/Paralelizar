import os
import time
import multiprocessing

# ===============================
# Configurações e Lógica de Processamento
# ===============================

def processar_arquivo(caminho):
    """Sua lógica original com carga pesada simulada"""
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.readlines()

        total_linhas = len(conteudo)
        total_palavras = 0
        total_caracteres = 0
        contagem = {"erro": 0, "warning": 0, "info": 0}

        for linha in conteudo:
            linha_low = linha.lower()
            palavras = linha_low.split()
            total_palavras += len(palavras)
            total_caracteres += len(linha)
            
            for p in palavras:
                if p in contagem:
                    contagem[p] += 1
            
            # Carga pesada simulada (do seu arquivo original)
            for _ in range(1000):
                pass

        return {
            "linhas": total_linhas,
            "palavras": total_palavras,
            "caracteres": total_caracteres,
            "contagem": contagem
        }
    except Exception:
        return None

def worker(fila_tarefas, fila_resultados):
    """Consumidor: Retira arquivos da fila e processa"""
    while True:
        caminho = fila_tarefas.get()
        if caminho is None: # Sinal de parada
            fila_tarefas.task_done()
            break
        resultado = processar_arquivo(caminho)
        fila_resultados.put(resultado)
        fila_tarefas.task_done()

# ===============================
# Funções de Execução
# ===============================

def executar_paralelo(pasta, num_processos):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.txt')]
    
    # Modelo Produtor-Consumidor com Buffer Limitado (maxsize=50)
    fila_tarefas = multiprocessing.JoinableQueue(maxsize=50)
    fila_resultados = multiprocessing.Queue()
    
    processos = []
    for _ in range(num_processos):
        p = multiprocessing.Process(target=worker, args=(fila_tarefas, fila_resultados))
        p.start()
        processos.append(p)

    inicio = time.perf_counter()

    for arq in arquivos:
        fila_tarefas.put(arq)

    for _ in range(num_processos):
        fila_tarefas.put(None)

    fila_tarefas.join()
    fim = time.perf_counter()
    
    return fim - inicio

def executar_serial(pasta):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.txt')]
    inicio = time.perf_counter()
    for arq in arquivos:
        processar_arquivo(arq)
    fim = time.perf_counter()
    return fim - inicio

# ===============================
# Bloco Principal e Cálculos
# ===============================

if __name__ == "__main__":
    pasta_alvo = "log2" 
    
    if not os.path.exists(pasta_alvo):
        print(f"Erro: Pasta '{pasta_alvo}' não encontrada. Rode o gerador primeiro.")
    else:
        print(f"Iniciando Testes na pasta: {pasta_alvo}")
        
        # 1. Obter Tempo Serial (T1)
        print("Calculando Tempo Serial (Base)...")
        tempo_serial = executar_serial(pasta_alvo)
        
        resultados_finais = []

        # 2. Testar 2, 4, 8 e 12 processos
        for n in [2, 4, 8, 12]:
            print(f"Executando com {n} processos...")
            t_paralelo = executar_paralelo(pasta_alvo, n)
            
            # CÁLCULOS SOLICITADOS NO RELATÓRIO
            speedup = tempo_serial / t_paralelo
            eficiencia = speedup / n
            
            resultados_finais.append({
                "proc": n,
                "tempo": t_paralelo,
                "speedup": speedup,
                "eficiencia": eficiencia
            })

        # 3. Impressão da Tabela para o README.md
        print("\n" + "="*65)
        print(f"{'Processos':<12} | {'Tempo (s)':<12} | {'Speedup':<12} | {'Eficiência':<12}")
        print("-" * 65)
        print(f"{'1 (Serial)':<12} | {tempo_serial:<12.4f} | {'1.00':<12} | {'1.00':<12}")
        
        for r in resultados_finais:
            print(f"{r['proc']:<12} | {r['tempo']:<12.4f} | {r['speedup']:<12.4f} | {r['eficiencia']:<12.4f}")
        print("="*65)
        print("\nCopie os valores acima para as tabelas e gráficos do seu relatório.")