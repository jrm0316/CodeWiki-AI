historico = []

def adicionar_interacao(pergunta, resposta):
    historico.append({
        "pergunta": pergunta,
        "resposta": resposta
    })

def obter_historico(limit=5):
    ultimas = historico[-limit:]
    texto = ""

    for item in ultimas:
        texto += f"Usuário: {item['pergunta']}\n"
        texto += f"IA: {item['resposta']}\n"

    return texto

print("memory carregado")