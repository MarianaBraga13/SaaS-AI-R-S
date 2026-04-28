import requests
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_cvs_na_web(termos):
    """Apenas busca os dados e retorna para quem pediu."""
    url = "https://google.serper.dev/search"
    query = f'filetype:pdf (intitle:curriculo OR "CV") "{termos}" -inurl:vagas'
    
    payload = {"q": query, "num": 10}
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        resultados = response.json()
        # Retorna apenas a lista de links encontrados
        return [item["link"] for item in resultados.get("organic", [])]
    except Exception as e:
        print(f"Erro no Seek: {e}")
        return []

# import urllib.parse

# def buscar_cvs_na_web(page, termos):
#     """Abre o navegador com uma busca avançada baseada nos termos da IA."""
    
#     filtro_cv = 'filetype:pdf (intitle:curriculo OR intitle:resume OR "CV")'
#     negativas = '-inurl:vagas -inurl:jobs -inurl:learning -inurl:udemy'
    
#     query = f'{filtro_cv} "{termos}" {negativas}'
    
#     url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
#     page.launch_url(url)