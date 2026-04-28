import flet as ft
import time
import seek
import core

def main(page: ft.Page):
    page.title = "RecrutAI - Triagem Inteligente"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = "adaptive"

    # --- Lógica de Seleção de Arquivo ---
    def handle_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_name_text.value = f"Arquivo selecionado: {e.files[0].name}"
            file_name_text.color = ft.colors.BLUE
            page.session.set("pdf_path", e.files[0].path)
        else:
            file_name_text.value = "Nenhum arquivo selecionado"
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=handle_file_result)
    page.overlay.append(pick_files_dialog)
    
    file_name_text = ft.Text("Nenhum arquivo selecionado", size=12, italic=True)

    # --- UI Components ---
    header = ft.Text("RecrutAI 🤖", size=32, weight="bold", color=ft.colors.BLUE_700)
    
    jd_input = ft.TextField(
        label="Insira a Descrição da Vaga (Job Description)",
        multiline=True,
        min_lines=5,
        hint_text="Ex: Requisitos: Python, SQL..."
    )

    # Componente visual para os Resultados
    resultado_card = ft.Column(visible=False, controls=[
        ft.Divider(),
        ft.Row([
            ft.Icon(ft.icons.ANALYTICS, color="blue"),
            ft.Text("Diagnóstico do Candidato", size=22, weight="bold"),
        ]),
        ft.Container(
            content=ft.Row([
                ft.Stack([
                    ft.ProgressRing(value=0.0, stroke_width=8, width=80, height=80, color="green"),
                    ft.Container(
                        content=ft.Text("0%", size=16, weight="bold"),
                        alignment=ft.alignment.center,
                        width=80, height=80
                    )
                ]),
                ft.Column([
                    ft.Text("Match Score", size=18, weight="bold", color="green"),
                    ft.Text("", size=14, width=300), # Mensagem de match
                ], spacing=2)
            ], spacing=20),
            padding=20, bgcolor=ft.colors.GREY_50, border_radius=15
        ),
        ft.Text("⚠️ Pontos de Atenção (Fraquezas)", size=16, weight="bold"),
        ft.Column([]) # Espaço para as fraquezas
    ])

    # --- Funções de Clique ---

    def analisar_click(e):
        if not jd_input.value or not page.session.get("pdf_path"):
            page.snack_bar = ft.SnackBar(ft.Text("Selecione um PDF e cole a vaga!"))
            page.snack_bar.open = True
            page.update()
            return
        
        progress_bar.visible = True
        btn_analisar.disabled = True
        page.update()

        try:
            caminho_pdf = page.session.get("pdf_path")
            texto_cv = core.extrair_texto_pdf(caminho_pdf)
            resultado = core.analisar_cv_completo(texto_cv, jd_input.value)

            # Atualizar UI com dados da IA
            score = resultado.get("score", 0)
            score_decimal = score / 100
            
            # Acessando os controles internos do card para atualizar
            resultado_card.controls[2].content.controls[0].controls[0].value = score_decimal
            resultado_card.controls[2].content.controls[0].controls[1].content.value = f"{score}%"
            resultado_card.controls[2].content.controls[1].controls[1].value = resultado.get("match_msg")

            # Atualiza lista de fraquezas
            lista_f = resultado_card.controls[4]
            lista_f.controls.clear()
            for f in resultado.get("fraquezas", []):
                lista_f.controls.append(ft.ListTile(leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="orange"), title=ft.Text(f)))

            resultado_card.visible = True

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"))
            page.snack_bar.open = True
        finally:
            progress_bar.visible = False
            btn_analisar.disabled = False
            page.update()

    def tratar_busca(e):
        if not jd_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Cole uma Job Description primeiro!"))
            page.snack_bar.open = True
            page.update()
            return
        
        progress_bar.visible = True
        page.update()
        
        # IA extrai termos e o seek faz a busca
        termos = core.extrair_termos_busca(jd_input.value)
        seek.buscar_cvs_na_web(page, termos)
        
        progress_bar.visible = False
        page.update()

    # --- Botões ---
    progress_bar = ft.ProgressBar(width=400, color=ft.colors.BLUE, visible=False)
    btn_analisar = ft.ElevatedButton("Analisar Currículo", on_click=analisar_click, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE)
    btn_pesquisa = ft.TextButton("Buscar candidatos na Web", icon=ft.icons.SEARCH, on_click=tratar_busca)

    page.add(
        header,
        ft.Text("Otimize sua triagem de candidatos com IA."),
        ft.Container(height=10),
        jd_input,
        ft.Row([
            ft.ElevatedButton("Selecionar PDF", icon=ft.icons.UPLOAD_FILE, on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["pdf"])),
            file_name_text
        ]),
        ft.Container(height=20),
        ft.Row([btn_analisar, btn_pesquisa]),
        progress_bar,
        resultado_card
    )

if __name__ == "__main__":
    ft.app(target=main)

# import flet as ft
# import time
# import seek
# import core

# def main(page: ft.Page):
#     page.title = "RecrutAI - Triagem Inteligente"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.padding = 30
#     page.scroll = "adaptive"

#     # --- Lógica de Seleção de Arquivo ---
#     def handle_file_result(e: ft.FilePickerResultEvent):
#         if e.files:
#             file_name_text.value = f"Arquivo selecionado: {e.files[0].name}"
#             file_name_text.color = ft.colors.BLUE
#             page.session.set("pdf_path", e.files[0].path)
#         else:
#             file_name_text.value = "Nenhum arquivo selecionado"
#         page.update()

#     pick_files_dialog = ft.FilePicker(on_result=handle_file_result)
#     page.overlay.append(pick_files_dialog)
    
#     file_name_text = ft.Text("Nenhum arquivo selecionado", size=12, italic=True)

#     # --- UI Components ---
#     header = ft.Text("RecrutAI 🤖", size=32, weight="bold", color=ft.colors.BLUE_700)
    
#     jd_input = ft.TextField(
#         label="Insira a Descrição da Vaga (Job Description)",
#         multiline=True,
#         min_lines=5,
#         hint_text="Ex: Requisitos: Python, SQL..."
#     )

#     # Componente visual para os Resultados
#     resultado_card = ft.Column(visible=False, controls=[
#         ft.Divider(),
#         ft.Row([
#             ft.Icon(ft.icons.ANALYTICS, color="blue"),
#             ft.Text("Diagnóstico do Candidato", size=22, weight="bold"),
#         ]),
#         ft.Container(
#             content=ft.Row([
#                 ft.Stack([
#                     ft.ProgressRing(value=0.85, stroke_width=8, width=80, height=80, color="green"),
#                     ft.Container(
#                         content=ft.Text("85%", size=16, weight="bold"),
#                         alignment=ft.alignment.center,
#                         width=80, height=80
#                     )
#                 ]),
#                 ft.Column([
#                     ft.Text("Match Score Alto", size=18, weight="bold", color="green"),
#                     ft.Text("O candidato possui as tecnologias principais.", size=14),
#                 ], spacing=2)
#             ], spacing=20),
#             padding=20, bgcolor=ft.colors.GREY_50, border_radius=15
#         ),
#         ft.Text("⚠️ Pontos de Atenção (Fraquezas)", size=16, weight="bold"),
#         ft.Column([
#             ft.ListTile(
#                 leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="red"),
#                 title=ft.Text("Falta de Inglês Fluente"),
#             ),
#         ])
#     ])

#     # --- Funções de Clique ---

#     def analisar_click(e):
#         if not jd_input.value or not page.session.get("pdf_path"):
#             page.snack_bar = ft.SnackBar(ft.Text("Selecione um PDF e cole a vaga!"))
#             page.snack_bar.open = True
#             page.update()
#             return
        
#         # 1. Mostrar carregamento
#         progress_bar.visible = True
#         btn_analisar.disabled = True # Evita cliques duplicados
#         page.update()

#         try:
#             # 2. Extrair texto do PDF usando seu core.py
#             caminho_pdf = page.session.get("pdf_path")
#             texto_cv = core.extrair_texto_pdf(caminho_pdf)

#             # 3. Chamar a análise da IA (Groq)
#             resultado = core.analisar_cv_completo(texto_cv, jd_input.value)

#             # 4. Atualizar a UI com os dados REAIS
#             score_decimal = resultado.get("score", 0) / 100
            
#             # Atualiza o anel de progresso e o texto do score
#             resultado_card.controls[2].content.controls[0].controls[0].value = score_decimal
#             resultado_card.controls[2].content.controls[0].controls[1].content.value = f"{resultado.get('score')}%"
            
#             # Atualiza a mensagem de match
#             resultado_card.controls[2].content.controls[1].controls[1].value = resultado.get("match_msg")

#             # Atualiza as fraquezas (limpa as antigas e adiciona novas)
#             lista_fraquezas = resultado_card.controls[4]
#             lista_fraquezas.controls.clear()
#             for f in resultado.get("fraquezas", []):
#                 lista_fraquezas.controls.append(
#                     ft.ListTile(
#                         leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="orange"),
#                         title=ft.Text(f),
#                     )
#                 )

#             resultado_card.visible = True

#         except Exception as ex:
#             page.snack_bar = ft.SnackBar(ft.Text(f"Erro na análise: {ex}"))
#             page.snack_bar.open = True

#         finally:
#             progress_bar.visible = False
#             btn_analisar.disabled = False
#             page.update()
        
#         # Chama a função do seu arquivo seek.py
#         seek.buscar_cvs_na_web(page, jd_input.value[:30]) # Pegamos o começo da vaga como termo

#     # --- Botões e Barras ---
#     progress_bar = ft.ProgressBar(width=400, color=ft.colors.BLUE, visible=False)
    
#     btn_analisar = ft.ElevatedButton(
#         "Analisar Currículo", 
#         on_click=analisar_click,
#         bgcolor=ft.colors.BLUE_700,
#         color=ft.colors.WHITE
#     )

#     btn_pesquisa = ft.TextButton(
#         "Buscar candidatos na Web", 
#         icon=ft.icons.SEARCH, 
#         on_click=tratar_busca
#     )

#     # --- Montagem Final da Página (APENAS UM PAGE.ADD) ---
#     page.add(
#         header,
#         ft.Text("Otimize sua triagem de candidatos com IA."),
#         ft.Container(height=10),
#         jd_input,
#         ft.Row([
#             ft.ElevatedButton(
#                 "Selecionar PDF", 
#                 icon=ft.icons.UPLOAD_FILE,
#                 on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["pdf"])
#             ),
#             file_name_text
#         ]),
#         ft.Container(height=20),
#         ft.Row([btn_analisar, btn_pesquisa]),
#         progress_bar,
#         resultado_card
#     )


# if __name__ == "__main__":
#     ft.app(target=main)

