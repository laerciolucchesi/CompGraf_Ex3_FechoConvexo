import random
import csv
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy import stats

def orientacao(a, b, c):
    # Sinal do produto vetorial entre AB e AC
    # >0: ponto c está à esquerda de a->b, 
    # <0: ponto c está à direita de a->b, 
    # =0: ponto c é colinear com a->b
    ux, uy = b[1] - a[1], b[2] - a[2]
    vx, vy = c[1] - a[1], c[2] - a[2]
    return ux * vy - uy * vx

def ponto_inicial(pontos):
    # Escolho o ponto mais abaixo (menor y)
    # No caso de empate, escolho o mais à direita (maior x)
    # Os pontos tem o formato (id, x, y)
    # Retorna apenas o índice do ponto inicial
    p0 = pontos[0]
    for p in pontos[1:]:
        if p[2] < p0[2] or (p[2] == p0[2] and p[1] > p0[1]):
            p0 = p
    return p0

def gift_wrapping(pontos):
    # Algoritmo de Gift Wrapping
    # Argumento: lista de pontos com o formato (id, x, y)
    # Retorna apenas os índices dos pontos do fecho

    # Se o número de pontos for menor ou igual a 3, o fecho é o próprio conjunto de pontos
    if len(pontos) <= 3:
        return [p[0] for p in pontos]

    # cria lista dos índices dos pontos do fecho
    fecho = []

    # ponto inicial
    p = ponto_inicial(pontos)
    inicio = p

    while True:

        # adiciona o ponto p ao fecho
        fecho.append(p)

        # Escolhe candidato inicial q
        # qualquer ponto diferente de p e que não está no fecho
        q = None
        for ponto in pontos:
            if ponto != p and ponto not in fecho:
                q = ponto
                break
        
        # Se não encontrou candidato, todos os pontos estão no fecho
        if q is None:
            break

        # escolhe o ponto q que está mais à esquerda partindo de p
        # o ponto q escolhido é o próximo ponto do fecho
        for r in pontos:
            # ponto não pode ser p ou q
            if r == p or r == q:
                continue
            # Se r está mais à esquerda de p->q, atualiza q <- r
            if orientacao(p, q, r) > 0:
                q = r

        # atualiza o ponto p para o ponto q que é o próximo ponto do fecho
        p = q
        
        # se o ponto p for o ponto inicial, o fecho está completo
        if p == inicio:
            break

    return [v[0] for v in fecho]  # retorna somente os índices dos pontos do fecho

def gerar_pontos(n):
    # Gera n pontos aleatórios com coordenadas entre -10 e +10
    # os pontos tem o formato (id, x, y)
    pontos = []
    for i in range(n):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        pontos.append((i, x, y)) 
    return pontos

def salvar_csv_fecho(caminho_csv, fecho_pts):
    # Salva o fecho no formato id,x,y (uma linha por ponto, na ordem antihorária)
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "x", "y"])
        for pid, x, y in fecho_pts:
            w.writerow([str(pid), f"{x:.6f}", f"{y:.6f}"])

def plotar_pontos_e_fecho(pontos, fecho_pts, caminho_png, n_pontos):
    # Prepara listas de coordenadas (xs,ys) de todos os pontos
    xs = [p[1] for p in pontos]
    ys = [p[2] for p in pontos]

    # Coordenadas do fecho para desenhar a borda
    fecho_x = [p[1] for p in fecho_pts] + [fecho_pts[0][1]]
    fecho_y = [p[2] for p in fecho_pts] + [fecho_pts[0][2]]

    # Gráfico de todos os pontos e do fecho (cores azul para os pontos e vermelho para o fecho)
    plt.figure(figsize=(8, 8))
    plt.scatter(xs, ys, color='blue', s=1, alpha=0.6)
    plt.plot(fecho_x, fecho_y, linewidth=2, color='red')

    plt.title(f"Fecho Convexo usando Gift Wrapping - {n_pontos} pontos")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_png, dpi=150, bbox_inches='tight')
    plt.close() 

def formatar_nome_arquivo(n):
    """
    Converte o número de pontos em notação cientifica para o nome do arquivo
    Examplo: 4 -> 2e02, 16384 -> 2e14
    """
    if n == 4:
        return "2e02"
    elif n == 8:
        return "2e03"
    elif n == 16:
        return "2e04"
    elif n == 32:
        return "2e05"
    elif n == 64:
        return "2e06"
    elif n == 128:
        return "2e07"
    elif n == 256:
        return "2e08"
    elif n == 512:
        return "2e09"
    elif n == 1024:
        return "2e10"
    elif n == 2048:
        return "2e11"
    elif n == 4096:
        return "2e12"
    elif n == 8192:
        return "2e13"
    elif n == 16384:
        return "2e14"
    elif n == 32768:
        return "2e15"
    elif n == 65536:
        return "2e16"
    elif n == 131072:
        return "2e17"
    elif n == 262144:
        return "2e18"
    elif n == 524288:
        return "2e19"
    elif n == 1048576:
        return "2e20"
    else:
        # Fallback para outros números
        return f"{n}"

def processar_tamanho_pontos_multiplas_vezes(n, num_execucoes=10):
    """
    Processa fecho convexo para um número específico de pontos múltiplas vezes
    """
    print(f"Processando {n} pontos - {num_execucoes} execuções...")
    
    resultados = []
    
    for execucao in range(num_execucoes):
        # Gera pontos aleatórios
        pontos = gerar_pontos(n)
        
        # Mede tempo de execução
        start_time = time.perf_counter()
        ids_fecho = gift_wrapping(pontos)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        # Reconstrói a lista de pontos do fecho convexo
        # porque o algoritmo devolve somente os índices dos pontos do fecho
        mapa = {pid: (pid, x, y) for (pid, x, y) in pontos}
        fecho_pts = [mapa[pid] for pid in ids_fecho]
        
        # Armazena resultado
        resultados.append((n, len(fecho_pts), execution_time))
        
        # Salva arquivos apenas na primeira execução para se ter um snapshot
        if execucao == 0:
            sufixo = formatar_nome_arquivo(n)
            caminho_csv = f"fecho_convexo_{sufixo}.csv"
            caminho_png = f"fecho_convexo_{sufixo}.png"
            
            # Salva CSV com pontos do fecho convexo
            salvar_csv_fecho(caminho_csv, fecho_pts)
            
            # Cria e salva gráfico
            plotar_pontos_e_fecho(pontos, fecho_pts, caminho_png, n)
        
        print(f"  Execução {execucao+1}/{num_execucoes}: {len(fecho_pts)} pontos no fecho, tempo: {execution_time:.6f}s")
    
    return resultados

def salvar_dados_tempo(caminho_csv, dados):
    """
    Salva dados de tempo em arquivo CSV
    """
    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["num_pontos", "pontos_fecho", "tempo_execucao"])
        for num_pontos, pontos_fecho, tempo in dados:
            w.writerow([num_pontos, pontos_fecho, f"{tempo:.6f}"])

def estimar_complexidade(n_pontos, pontos_fecho, tempos):
    """
    Estima complexidade O(nh) usando regressão linear em gráfico log-log
    onde n é o número de pontos e h é o número de pontos no fecho convexo
    """
    # Calcula n*h para cada conjunto de pontos
    nh = [n * h for n, h in zip(n_pontos, pontos_fecho)]
    
    # Converte para escala logarítmica
    log_nh = np.log(nh)
    log_t = np.log(tempos)
    
    # Regressão linear: log(t) = c * log(nh) + b
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_nh, log_t)
    
    # A inclinação é o expoente c da complexidade O((nh)^c)
    c = slope
    
    return c, r_value, intercept, nh

def plotar_complexidade(n_pontos, pontos_fecho, tempos, caminho_png):
    """
    Cria gráfico log-log de n*h vs tempo de execução com estimativa de complexidade O((nh)^c)
    """
    # Estima complexidade
    c, r_squared, intercept, nh = estimar_complexidade(n_pontos, pontos_fecho, tempos)
    
    # Cria gráfico log-log
    plt.figure(figsize=(12, 10))
    
    # Plota pontos de dados reais
    plt.loglog(nh, tempos, 'bo', markersize=4, alpha=0.6, label='Dados Medidos')
    
    # Plota linha ajustada
    log_nh = np.log(nh)
    log_t_fitted = c * log_nh + intercept
    t_fitted = np.exp(log_t_fitted)
    plt.loglog(nh, t_fitted, 'r--', linewidth=2, 
               label=f'Linha Ajustada')
    
    # Adiciona informações de complexidade
    plt.title(f'Complexidade Estimada do Algoritmo Gift Wrapping', 
              fontsize=20, fontweight='bold')
    plt.xlabel('n*h [n=pontos da nuvem, h=pontos no fecho]', fontsize=20)
    plt.ylabel('Tempo de Execução [segundos]', fontsize=20)
    
    # Adiciona caixa de texto de complexidade no canto inferior direito
    textstr = f'Complexidade Estimada O( (nh)$^{{{c:.2f}}}$ )\n Coeficiente de determinação R² {r_squared:.4f}'
    props = None
    plt.text(0.95, 0.05, textstr, transform=plt.gca().transAxes, fontsize=20,
             verticalalignment='bottom', horizontalalignment='right', bbox=props)
    
    plt.grid(True, alpha=0.3)
    # Posiciona legenda no canto superior esquerdo
    plt.legend(fontsize=20, loc='upper left')
    
    # Altera o tamanho da fonte dos números dos eixos
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tick_params(axis='both', which='minor', labelsize=16)
    
    plt.tight_layout()
    plt.savefig(caminho_png, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    """
    Função principal que processa todos os tamanhos de pontos múltiplas vezes
    """
    # Lista de tamanhos de pontos para processar
    tamanhos = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
    num_execucoes = 1000  # Número de execuções para cada tamanho de nuvem de pontos
    
    print("Iniciando processamento de fecho convexo para múltiplos tamanhos de pontos...")
    print(f"Cada tamanho de nuvem de pontos será executado {num_execucoes} vezes.")
    print("=" * 80)
    
    # Coleta todos os dados
    todos_dados = []
    
    for n in tamanhos:
        try:
            resultados = processar_tamanho_pontos_multiplas_vezes(n, num_execucoes)
            todos_dados.extend(resultados) # adiciona os resultados a lista de todos os dados
            print()
        except Exception as e:
            print(f"Erro ao processar {n} pontos: {e}")
            print()
    
    # Salva dados de tempo em CSV
    caminho_tempo_csv = "tempos_execucao.csv"
    salvar_dados_tempo(caminho_tempo_csv, todos_dados)
    print(f"Dados de tempo salvos em: {caminho_tempo_csv}")
    
    # Cria gráfico de análise de complexidade
    if len(todos_dados) > 1:
        n_pontos = [d[0] for d in todos_dados]
        pontos_fecho = [d[1] for d in todos_dados]
        tempos = [d[2] for d in todos_dados]
        
        # Gráfico de complexidade (tempo vs n*h)
        caminho_complexidade_png = "analise_complexidade.png"
        plotar_complexidade(n_pontos, pontos_fecho, tempos, caminho_complexidade_png)
        print(f"Gráfico de análise de complexidade salvo em: {caminho_complexidade_png}")
        
        # Estima e imprime complexidade
        c, r_squared, _, nh = estimar_complexidade(n_pontos, pontos_fecho, tempos)
        print(f"Complexidade estimada: O((nh)^{c:.2f})")
        print(f"R² = {r_squared:.4f}")
        print(f"Total de pontos de dados: {len(tempos)}")
        
        # Estatísticas por tamanho
        print("\nEstatísticas por tamanho de pontos:")
        print("=" * 60)
        for n in tamanhos:
            dados_n = [d for d in todos_dados if d[0] == n]
            if dados_n:
                tempos_n = [d[2] for d in dados_n]
                fechos_n = [d[1] for d in dados_n]
                print(f"n={n:5d}: tempo médio={np.mean(tempos_n):.6f}s, fecho médio={np.mean(fechos_n):.1f} pontos, {len(dados_n)} execuções")
    
    # Finalização
    print("\n" + "=" * 80)
    print("Processamento concluído!")

if __name__ == "__main__":
    main()
