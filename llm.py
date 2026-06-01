import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def responder(pergunta, contexto):
    prompt = f"""
Você é um especialista em análise de código-fonte.

Responda perguntas com base no código enviado pelo usuário.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}

Responda SOMENTE com base no código fornecido.
Não invente funcionalidades.
Seja técnico e objetivo.
"""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content


def resumir_projeto(contexto):
    prompt = f"""
Você é um arquiteto de software.

Analise os arquivos fornecidos.

Explique:

1. Qual é o objetivo do projeto
2. Principais módulos
3. Fluxo geral da aplicação
4. Tecnologias identificadas
5. Possíveis melhorias

Código:

{contexto}

Seja objetivo.
"""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content


def gerar_readme(contexto):
    prompt = f"""
Você é um especialista em documentação de software.

Analise o código abaixo e gere um README.md completo.

Inclua:

# Nome do Projeto

## O que faz

## Como funciona

## Estrutura do Projeto

## Principais Classes

## Principais Funções

## Tecnologias Utilizadas

## Como Executar

Código:

{contexto}
"""
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    return response.choices[0].message.content

def documentar_codigo(codigo):

    prompt = f"""
Você é um especialista em documentação Python.

Analise o código abaixo.

Explique:

1. Objetivo
2. Parâmetros
3. Retorno
4. Como funciona
5. Possíveis melhorias

Código:

{codigo}
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content

def explicar_arquitetura(contexto):

    prompt = f"""
Você é um arquiteto de software.

Analise o projeto abaixo.

Explique:

1. Objetivo geral
2. Fluxo da aplicação
3. Principais módulos
4. Como os módulos se comunicam
5. Responsabilidades de cada arquivo

Projeto:

{contexto}
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content