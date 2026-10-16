import turtle
import math
import time

# ==========================================
# 1. TELA E ADAPTAÇÃO DINÂMICA
# ==========================================
tela = turtle.Screen()
tela.setup(width=920, height=520)
tela.bgcolor("#2c1d0c")
tela.title("Bilhar Profissional - Responsivo & Regras Ajustadas")
tela.tracer(0) 

# Pega o tamanho atual da janela para calcular limites proporcionais
largura_mesa = 800
altura_mesa = 400

# Feltro verde da mesa
feltro = turtle.Turtle()
feltro.speed(0)
feltro.shape("square")
feltro.color("#155843")
feltro.shapesize(stretch_wid=altura_mesa/20, stretch_len=largura_mesa/20)
feltro.penup()
feltro.goto(0, 0)

# ==========================================
# 2. CAÇAPAS (Calculadas dinamicamente)
# ==========================================
meio_l = largura_mesa / 2
meio_a = altura_mesa / 2

cacapas = [
    (-meio_l + 10, meio_a - 10), (0, meio_a - 10), (meio_l - 10, meio_a - 10), 
    (-meio_l + 10, -meio_a + 10), (0, -meio_a + 10), (meio_l - 10, -meio_a + 10)
]

for x, y in cacapas:
    c = turtle.Turtle()
    c.speed(0)
    c.shape("circle")
    c.color("#0a2b20")
    c.shapesize(2.2, 2.2)
    c.penup()
    c.goto(x, y)

# ==========================================
# 3. MOTOR DE FÍSICA
# ==========================================
class Bola(turtle.Turtle):
    def __init__(self, cor, x, y, tipo):
        super().__init__()
        self.shape("circle")
        self.color(cor)
        self.tipo = tipo # "branca", "azul", "vermelha", "preta"
        self.penup()
        self.goto(x, y)
        self.dx = 0
        self.dy = 0
        self.raio = 10 

    def mover(self):
        self.dx *= 0.985
        self.dy *= 0.985
        
        if abs(self.dx) < 0.05: self.dx = 0
        if abs(self.dy) < 0.05: self.dy = 0
        
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)
        
        # Limites das bordas baseados no tamanho dinâmico da mesa
        limite_x = meio_l - 15
        limite_y = meio_a - 15

        if self.xcor() > limite_x:
            self.setx(limite_x)
            self.dx *= -0.8
        elif self.xcor() < -limite_x:
            self.setx(-limite_x)
            self.dx *= -0.8
            
        if self.ycor() > limite_y:
            self.sety(limite_y)
            self.dy *= -0.8
        elif self.ycor() < -limite_y:
            self.sety(-limite_y)
            self.dy *= -0.8

# ==========================================
# 4. INSTANCIANDO AS BOLAS
# ==========================================
bolas = []
branca = Bola("white", -200, 0, "branca")
bolas.append(branca)

cores_triangulo = [
    "red", 
    "blue", "red", 
    "red", "black", "blue", 
    "blue", "red", "blue", "red", 
    "red", "blue", "red", "blue", "blue"
]

idx_cor = 0
inicio_x = 120
for coluna in range(5):
    x = inicio_x + coluna * 17.32 
    y_inicio = -10 * coluna
    for linha in range(coluna + 1):
        y = y_inicio + linha * 20 
        cor = cores_triangulo[idx_cor]
        tipo = "preta" if cor == "black" else cor
        bolas.append(Bola(cor, x, y, tipo))
        idx_cor += 1

# ==========================================
# 5. PLACAR E TURNOS
# ==========================================
jogador_atual = 1 
jogo_ativo = True

placar = turtle.Turtle()
placar.hideturtle()
placar.penup()
placar.color("white")
placar.goto(0, 225)

def atualizar_placar(mensagem=""):
    placar.clear()
    if mensagem:
        placar.write(mensagem, align="center", font=("Courier", 20, "bold"))
    else:
        cor_texto = "Cyan" if jogador_atual == 1 else "Tomato"
        nome_jogador = "Jogador 1 (Azul)" if jogador_atual == 1 else "Jogador 2 (Vermelho)"
        placar.write(f"Vez de: {nome_jogador}", align="center", font=("Courier", 18, "bold"))

atualizar_placar()

# ==========================================
# 6. TACO E MIRA
# ==========================================
taco = turtle.Turtle()
taco.shape("square")
taco.color("#DEB887")
taco.shapesize(stretch_wid=0.2, stretch_len=10)
taco.penup()

mouse_x = 0
mouse_y = 0

def rastrear_mouse(event):
    global mouse_x, mouse_y
    canvas = tela.getcanvas()
    mouse_x = event.x - canvas.winfo_width() / 2
    mouse_y = canvas.winfo_height() / 2 - event.y

tela.getcanvas().bind('<Motion>', rastrear_mouse)

def dar_tacada(x, y):
    global jogo_ativo
    if not jogo_ativo: return
    
    if branca.dx == 0 and branca.dy == 0:
        dx = x - branca.xcor()
        dy = y - branca.ycor()
        distancia = math.hypot(dx, dy)
        
        if distancia > 0:
            forca = min(distancia / 8, 30)
            branca.dx = (dx / distancia) * forca
            branca.dy = (dy / distancia) * forca

tela.onscreenclick(dar_tacada)

# ==========================================
# 7. LOOP PRINCIPAL
# ==========================================
movendo_anterior = False
bolas_encaçapadas_nesta_rodada = []

try:
    while True:
        time.sleep(0.015) 
        tela.update()
        
        bolas_em_movimento = False
        
        for bola in bolas:
            if bola.dx != 0 or bola.dy != 0:
                bola.mover()
                bolas_em_movimento = True
                
        if jogo_ativo:
            if not bolas_em_movimento:
                if movendo_anterior:
                    preta_caiu = any(b.tipo == "preta" for b in bolas_encaçapadas_nesta_rodada)
                    bolas_coloridas_restantes = sum(1 for b in bolas if b.tipo in ["azul", "vermelha"])
                    
                    if preta_caiu:
                        if bolas_coloridas_restantes > 0:
                            atualizar_placar(f"JOGADOR {jogador_atual} PERDEU! (Preta antes da hora)")
                            jogo_ativo = False
                        else:
                            atualizar_placar(f"JOGADOR {jogador_atual} VENCEU O JOGO!")
                            jogo_ativo = False
                    else:
                        acertou_sua_bola = False
                        caiu_errada = False
                        
                        for b in bolas_encaçapadas_nesta_rodada:
                            if jogador_atual == 1 and b.tipo == "azul": acertou_sua_bola = True
                            if jogador_atual == 2 and b.tipo == "vermelha": acertou_sua_bola = True
                            if jogador_atual == 1 and b.tipo == "vermelha": caiu_errada = True
                            if jogador_atual == 2 and b.tipo == "azul": caiu_errada = True
                        
                        # Penalidade por encaçapar a bola do adversário: Perde a vez, mas não o jogo
                        if caiu_errada:
                            jogador_atual = 2 if jogador_atual == 1 else 1
                            atualizar_placar(f"FALTA! Caiu bola adversária. Vez do Jogador {jogador_atual}")
                            time.sleep(1.5) # Pausa rápida para ler o aviso
                        elif acertou_sua_bola:
                            pass # Joga de novo
                        else:
                            jogador_atual = 2 if jogador_atual == 1 else 1
                        
                        if jogo_ativo:
                            atualizar_placar()
                            
                    bolas_encaçapadas_nesta_rodada.clear()

                taco.showturtle()
                dx_mira = mouse_x - branca.xcor()
                dy_mira = mouse_y - branca.ycor()
                angulo = math.degrees(math.atan2(dy_mira, dx_mira))
                
                distancia_taco = 110
                taco_x = branca.xcor() - math.cos(math.radians(angulo)) * distancia_taco
                taco_y = branca.ycor() - math.sin(math.radians(angulo)) * distancia_taco
                
                taco.goto(taco_x, taco_y)
                taco.setheading(angulo)
            else:
                taco.hideturtle()
                
        movendo_anterior = bolas_em_movimento
            
        # Colisões
        for i in range(len(bolas)):
            for j in range(i + 1, len(bolas)):
                b1 = bolas[i]
                b2 = bolas[j]
                
                if b1.dx == 0 and b1.dy == 0 and b2.dx == 0 and b2.dy == 0:
                    continue
                
                dx = b2.xcor() - b1.xcor()
                dy = b2.ycor() - b1.ycor()
                distancia = math.hypot(dx, dy)
                
                if distancia < 20: 
                    if distancia == 0: distancia = 0.1 
                    
                    sobreposicao = 0.5 * (20 - distancia)
                    nx = dx / distancia
                    ny = dy / distancia
                    
                    b1.setx(b1.xcor() - nx * sobreposicao)
                    b1.sety(b1.ycor() - ny * sobreposicao)
                    b2.setx(b2.xcor() + nx * sobreposicao)
                    b2.sety(b2.ycor() + ny * sobreposicao)
                    
                    v1_normal = b1.dx * nx + b1.dy * ny
                    v2_normal = b2.dx * nx + b2.dy * ny
                    v1_tang = b1.dx - v1_normal * nx
                    v1_tang_y = b1.dy - v1_normal * ny
                    v2_tang = b2.dx - v2_normal * nx
                    v2_tang_y = b2.dy - v2_normal * ny
                    
                    restituicao = 0.9 
                    
                    b1.dx = v1_tang + v2_normal * nx * restituicao
                    b1.dy = v1_tang_y + v2_normal * ny * restituicao
                    b2.dx = v2_tang + v1_normal * nx * restituicao
                    b2.dy = v2_tang_y + v1_normal * ny * restituicao

        # Encaçapamento
        bolas_para_remover = []
        for bola in bolas:
            for cx, cy in cacapas:
                if math.hypot(bola.xcor() - cx, bola.ycor() - cy) < 25: 
                    if bola == branca:
                        bola.goto(-200, 0)
                        bola.dx = 0
                        bola.dy = 0
                    else:
                        bola.goto(1000, 1000) 
                        bola.hideturtle()
                        bolas_para_remover.append(bola)
                        bolas_encaçapadas_nesta_rodada.append(bola)
                    break
        
        for bola in bolas_para_remover:
            if bola in bolas:
                bolas.remove(bola)

except turtle.Terminator:
    pass