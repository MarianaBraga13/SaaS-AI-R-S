import os
import fitz  # PyMuPDF
import json
from groq import Groq
from dotenv import load_dotenv

# Carrega a API KEY do seu arquivo .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extrair_texto_pdf(caminho_arquivo):
    """Lê o PDF e transforma em texto puro."""
    try:
        doc = fitz.open(caminho_arquivo)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto
    except Exception as e:
        return f"Erro ao ler PDF: {str(e)}"

def extrair_termos_busca(jd_texto):
    """Usa IA para transformar uma vaga gigante em 3 palavras-chave de busca."""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Você é um expert em recrutamento. Extraia APENAS as 3 tecnologias ou cargos principais para busca de currículos. Sem frases, apenas palavras."},
                {"role": "user", "content": jd_texto}
            ]
        )
        return completion.choices[0].message.content.strip()
    except:
        return "Python Developer" # Fallback caso a API falhe

def analisar_cv_completo(texto_cv, jd_texto):
    """A lógica principal: compara o currículo com a vaga e gera o diagnóstico."""
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192", # Modelo mais forte para análise profunda
            messages=[
                {"role": "system", "content": "Você é um recrutador. Analise o CV vs Vaga e retorne APENAS um JSON."},
                {"role": "user", "content": f"Vaga: {jd_texto}\n\nCV: {texto_cv}\n\nRetorne JSON: {{\"score\": int, \"match_msg\": \"resumo\", \"fraquezas\": [\"lista\"]}}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}