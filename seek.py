import urllib.parse

# def buscar_cvs_na_web(page, termos):
#     query = f'filetype:pdf "curriculo" {termos}'
#     url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
#     page.launch_url(url)

import urllib.parse

def buscar_cvs_na_web(page, termos):
    # O segredo está nos operadores:
    # filetype:pdf -> Apenas arquivos PDF (padrão de CV)
    # intitle:curriculo -> O arquivo TEM que ser um currículo
    # -inurl:(vagas|jobs|cursos) -> Remove sites que vendem cursos ou anunciam vagas
    
    filtro_cv = 'filetype:pdf (intitle:curriculo OR intitle:resume OR "CV")'
    negativas = '-inurl:vagas -inurl:jobs -inurl:learning -inurl:udemy'
    
    query = f'{filtro_cv} "{termos}" {negativas}'
    
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    page.launch_url(url)

# import urllib.parse

# def buscar_cvs_na_web(page, termos):
#     # O filtro 'intitle' e 'filetype' isola currículos reais de blogs ou cursos
#     query = f'filetype:pdf (intitle:curriculo OR intitle:resume) "{termos}" -inurl:jobs -inurl:vagas'
    
#     url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
#     page.launch_url(url)