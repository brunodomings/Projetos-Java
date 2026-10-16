import turtle
import random

# ==========================================
# 1. CONFIGURAÇÃO DA TELA GRÁFICA
# ==========================================
tela = turtle.Screen()
tela.setup(width=900, height=600)
tela.bgcolor("#0b3d1e")
tela.title("Truco Paulista Gráfico - Estável")
tela.tracer(0)

# ==========================================
# 2. ESTRUTURA DE CARTAS E REGRAS
# ==========================================
VALORES_COMUNS = {'4': 1, '5': 2, '6': 3, '7': 4, 'Q': 5, 'J': 6, 'K': 7, 'A': 8, '2': 9, '3': 10}
SIMBOLOS_NAIPES = {'Paus': '♣', 'Copas': '♥', 'Espadas': '♠', 'Ouros': '♦'}

class CartaObj:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        
    def obter_manilhas(self, vira_valor):
        ordem_valores = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        idx_vira = ordem_valores.index(vira_valor)
        idx_manilha = (idx_vira + 1) % len(ordem_valores)
        return ordem_valores[idx_manilha]

    def forca(self, vira_valor):
        manilha_val = self.obter_manilhas(vira_valor)
        ordem_naipes = {'Paus': 4, 'Copas': 3, 'Espadas': 2, 'Ouros': 1}
        
        if self.valor == manilha_val:
            return 20 + ordem_naipes[self.naipe]
        return VALORES_COMUNS.get(self.valor, 0)

# ==========================================
# 3. ELEMENTOS GRÁFICOS
# ==========================================
escritor = turtle.Turtle()
escritor.hideturtle()
escritor.penup()
escritor.color("white")

pos_mesa = {
    0: (0, -40),   # Você
    1: (-140, 10), # Bot 1 (Esquerda)
    2: (0, 60),    # Bot 2 - Seu Parceiro (Topo)
    3: (140, 10)   # Bot 3 (Direita)
}

turtles_mesa = []
turtles_mao = []

def desenhar_retangulo(turt, x, y, largura, altura, cor_fundo, cor_borda="black"):
    turt.penup()
    turt.goto(x - largura/2, y - altura/2)
    turt.setheading(0)
    turt.pendown()
    turt.color(cor_borda, cor_fundo)
    turt.begin_fill()
    for _ in range(2):
        turt.forward(largura)
        turt.left(90)
        turt.forward(altura)
        turt.left(90)
    turt.end_fill()
    turt.penup()

def desenhar_carta(x, y, carta=None, largura=50, altura=75, na_mesa=True):
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    desenhar_retangulo(t, x, y, largura, altura, "white", "black")
    t.goto(x, y - 15)
    cor = "red" if carta.naipe in ['Copas', 'Ouros'] else "black"
    t.color(cor)
    simbolo = SIMBOLOS_NAIPES.get(carta.naipe, "")
    t.write(f"{carta.valor}\n{simbolo}", align="center", font=("Arial", 12, "bold"))
    
    if na_mesa:
        turtles_mesa.append(t)
    else:
        turtles_mao.append(t)
    return t

def limpar_turtles(lista):
    for t in lista:
        t.clear()
    lista.clear()

# ==========================================
# 4. ESTADO DO JOGO
# ==========================================
pontos_nos = 0
pontos_eles = 0
mao_jogador = []
mao_bots = [[], [], []]
vira_atual = None

vitorias_nos_mao = 0
vitorias_eles_mao = 0
aguardando_clique = True

def iniciar_nova_mao():
    global mao_jogador, mao_bots, vira_atual, vitorias_nos_mao, vitorias_eles_mao, aguardando_clique
    vitorias_nos_mao = 0
    vitorias_eles_mao = 0
    
    valores = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    naipes = ['Paus', 'Copas', 'Espadas', 'Ouros']
    baralho = [CartaObj(v, n) for v in valores for n in naipes]
    random.shuffle(baralho)
    
    mao_jogador = [baralho.pop(), baralho.pop(), baralho.pop()]
    for i in range(3):
        mao_bots[i] = [baralho.pop(), baralho.pop(), baralho.pop()]
    vira_atual = baralho.pop()
    
    limpar_turtles(turtles_mesa)
    aguardando_clique = True
    atualizar_interface("Sua vez! Clique em uma carta para jogar.")

def atualizar_interface(mensagem):
    escritor.clear()
    limpar_turtles(turtles_mao)
    
    # Placar Geral no topo
    escritor.goto(0, 260)
    escritor.color("white")
    escritor.write(f"NÓS: {pontos_nos}  X  ELES: {pontos_eles}", align="center", font=("Arial", 18, "bold"))
    
    # Identificação fixa dos Nomes e Equipes
    escritor.goto(0, -145)
    escritor.color("gold")
    escritor.write("VOCÊ (Equipe NÓS)", align="center", font=("Arial", 11, "bold"))
    
    escritor.goto(0, 160)
    escritor.color("gold")
    escritor.write("BOT 2 - SEU PARCEIRO (Equipe NÓS)", align="center", font=("Arial", 11, "bold"))
    
    escritor.goto(-240, 10)
    escritor.color("tomato")
    escritor.write("BOT 1\n(Adversário)", align="center", font=("Arial", 10, "bold"))
    
    escritor.goto(240, 10)
    escritor.color("tomato")
    escritor.write("BOT 3\n(Adversário)", align="center", font=("Arial", 10, "bold"))

    # Vira da Mesa
    escritor.color("white")
    escritor.goto(-320, 180)
    escritor.write("Vira da Mesa:", align="center", font=("Arial", 11, "normal"))
    if vira_atual:
        desenhar_carta(-320, 115, vira_atual, largura=45, altura=65, na_mesa=False)
    
    # Status inferior
    escritor.goto(0, -220)
    escritor.write(mensagem, align="center", font=("Arial", 13, "italic"))
    
    # Suas Cartas na mão (parte inferior)
    for i, carta in enumerate(mao_jogador):
        x = -90 + (i * 90)
        y = -90
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        desenhar_retangulo(t, x, y, 65, 90, "white", "gold")
        t.goto(x, y - 20)
        cor = "red" if carta.naipe in ['Copas', 'Ouros'] else "black"
        t.color(cor)
        simbolo = SIMBOLOS_NAIPES.get(carta.naipe, "")
        t.write(f"{carta.valor}\n{simbolo}", align="center", font=("Arial", 16, "bold"))
        turtles_mao.append(t)
        
        t.goto(x, y - 55)
        t.color("white")
        t.write(f"Carta {i+1}", align="center", font=("Arial", 9, "normal"))

    tela.update()

def bot_escolhe_carta(mao_bot):
    return min(mao_bot, key=lambda c: c.forca(vira_atual.valor))

# ==========================================
# 5. MECÂNICA DE CLIQUE E RODADA
# ==========================================
def clique_mouse(x, y):
    global mao_jogador, aguardando_clique
    if not aguardando_clique:
        return

    if -140 <= y <= -45 and len(mao_jogador) > 0:
        if -125 <= x <= -55: escolha = 0
        elif -35 <= x <= 35: escolha = 1
        elif 55 <= x <= 125: escolha = 2
        else: return
        
        if escolha < len(mao_jogador):
            aguardando_clique = False
            carta_jogador = mao_jogador.pop(escolha)
            executar_rodada(carta_jogador)

def executar_rodada(carta_jogador):
    global vitorias_nos_mao, vitorias_eles_mao, pontos_nos, pontos_eles, aguardando_clique
    limpar_turtles(turtles_mesa)
    
    # Você joga
    desenhar_carta(pos_mesa[0][0], pos_mesa[0][1], carta_jogador, na_mesa=True)
    cartas_rodada = [(0, carta_jogador)]
    tela.update()
    
    # Bots jogam sequencialmente com um pequeno atraso visual usando ontimer
    def jogar_bot_sequencial(idx_bot):
        if idx_bot <= 3:
            c_bot = bot_escolhe_carta(mao_bots[idx_bot - 1])
            mao_bots[idx_bot - 1].remove(c_bot)
            desenhar_carta(pos_mesa[idx_bot][0], pos_mesa[idx_bot][1], c_bot, na_mesa=True)
            cartas_rodada.append((idx_bot, c_bot))
            tela.update()
            tela.ontimer(lambda: jogar_bot_sequencial(idx_bot + 1), 400)
        else:
            # Fim da rodada, calcula o vencedor
            vencedor = max(cartas_rodada, key=lambda item: item[1].forca(vira_atual.valor))[0]
            
            global vitorias_nos_mao, vitorias_eles_mao
            if vencedor == 0 or vencedor == 2:
                vitorias_nos_mao += 1
                msg_rodada = "Sua dupla venceu esta queda!"
            else:
                vitorias_eles_mao += 1
                msg_rodada = "A dupla adversária venceu esta queda!"
                
            atualizar_interface(msg_rodada)
            
            # Verifica fim da mão ou próxima rodada
            if vitorias_nos_mao == 2 or vitorias_eles_mao == 2 or len(mao_jogador) == 0:
                global pontos_nos, pontos_eles
                if vitorias_nos_mao >= vitorias_eles_mao:
                    pontos_nos += 1
                    resultado_final = "Sua dupla venceu a mão! +1 Ponto."
                else:
                    pontos_eles += 1
                    resultado_final = "A dupla adversária venceu a mão! +1 Ponto."
                    
                atualizar_interface(resultado_final)
                tela.ontimer(iniciar_nova_mao, 2500)
            else:
                def liberar_proxima():
                    global aguardando_clique
                    limpar_turtles(turtles_mesa)
                    aguardando_clique = True
                    atualizar_interface("Sua vez! Jogue a próxima carta.")
                tela.ontimer(liberar_proxima, 2000)

    tela.ontimer(lambda: jogar_bot_sequencial(1), 400)

tela.onscreenclick(clique_mouse)

iniciar_nova_mao()
turtle.mainloop()