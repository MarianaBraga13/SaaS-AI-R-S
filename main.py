import flet as ft
import time
import seek

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
        label="Insira palavras-chave da vaga",
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
                    ft.ProgressRing(value=0.85, stroke_width=8, width=80, height=80, color="green"),
                    ft.Container(
                        content=ft.Text("85%", size=16, weight="bold"),
                        alignment=ft.alignment.center,
                        width=80, height=80
                    )
                ]),
                ft.Column([
                    ft.Text("Match Score Alto", size=18, weight="bold", color="green"),
                    ft.Text("O candidato possui as tecnologias principais.", size=14),
                ], spacing=2)
            ], spacing=20),
            padding=20, bgcolor=ft.colors.GREY_50, border_radius=15
        ),
        ft.Text("⚠️ Pontos de Atenção (Fraquezas)", size=16, weight="bold"),
        ft.Column([
            ft.ListTile(
                leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="red"),
                title=ft.Text("Falta de Inglês Fluente"),
            ),
        ])
    ])

    # --- Funções de Clique ---
    def analisar_click(e):
        if not jd_input.value or not page.session.get("pdf_path"):
            page.snack_bar = ft.SnackBar(ft.Text("Selecione um PDF e cole a vaga!"))
            page.snack_bar.open = True
            page.update()
            return
        
        progress_bar.visible = True
        page.update()
        time.sleep(2) # Simulando IA
        progress_bar.visible = False
        resultado_card.visible = True
        page.update()

    def tratar_busca(e):
        if not jd_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Cole uma Job Description primeiro!"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Chama a função do seu arquivo seek.py
        seek.buscar_cvs_na_web(page, jd_input.value[:30]) # Pegamos o começo da vaga como termo

    # --- Botões e Barras ---
    progress_bar = ft.ProgressBar(width=400, color=ft.colors.BLUE, visible=False)
    
    btn_analisar = ft.ElevatedButton(
        "Analisar Currículo", 
        on_click=analisar_click,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE
    )

    btn_pesquisa = ft.TextButton(
        "Buscar candidatos na Web", 
        icon=ft.icons.SEARCH, 
        on_click=tratar_busca
    )

    # --- Montagem Final da Página (APENAS UM PAGE.ADD) ---
    page.add(
        header,
        ft.Text("Otimize sua triagem de candidatos com IA."),
        ft.Container(height=10),
        jd_input,
        ft.Row([
            ft.ElevatedButton(
                "Selecionar PDF", 
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: pick_files_dialog.pick_files(allowed_extensions=["pdf"])
            ),
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
# from core import extrair_termos_busca # Importando a inteligência

# def main(page: ft.Page):
#     page.title = "RecrutAI - Triagem Inteligente"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.padding = 30
#     page.window_width = 500
#     page.window_height = 800
#     page.scroll = "adaptive"

#     # --- Lógica de Seleção de Arquivo ---
#     def handle_file_result(e: ft.FilePickerResultEvent):
#         if e.files:
#             file_name_text.value = f"Arquivo selecionado: {e.files[0].name}"
#             file_name_text.color = ft.colors.BLUE_700
#             page.session.set("pdf_path", e.files[0].path)
#         else:
#             file_name_text.value = "Nenhum arquivo selecionado"
#         page.update()

#     pick_files_dialog = ft.FilePicker(on_result=handle_file_result)
#     page.overlay.append(pick_files_dialog)
    
#     file_name_text = ft.Text("Nenhum arquivo selecionado", size=12, italic=True)

#     # --- UI Components ---
#     header = ft.Column([
#         ft.Text("RecrutAI 🤖", size=32, weight="bold", color=ft.colors.BLUE_700),
#         ft.Text("Otimize sua triagem de candidatos com IA.", size=16, color=ft.colors.GREY_700),
#     ], spacing=5)
    
#     jd_input = ft.TextField(
#         label="Job Description",
#         placeholder="Cole aqui os requisitos da vaga...",
#         multiline=True,
#         min_lines=5,
#         max_lines=8,
#         border_radius=10
#     )

#     # Card de Resultado (Inicia invisível)
#     resultado_card = ft.Column(visible=False, controls=[
#         ft.Divider(height=30),
#         ft.Row([
#             ft.Icon(ft.icons.ANALYTICS, color="blue"),
#             ft.Text("Diagnóstico do Candidato", size=20, weight="bold"),
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
#         ft.Text("⚠️ Pontos de Atenção", size=16, weight="bold"),
#         ft.Column([
#             ft.ListTile(
#                 leading=ft.Icon(ft.icons.ERROR_OUTLINE, color="red"),
#                 title=ft.Text("Falta de Inglês Fluente"),
#                 subtitle=ft.Text("Requisito obrigatório não identificado no CV.")
#             ),
#         ])
#     ])

#     # --- Funções de Evento ---
#     def analisar_click(e):
#         if not jd_input.value or not page.session.get("pdf_path"):
#             page.snack_bar = ft.SnackBar(ft.Text("Erro: Selecione um PDF e cole a vaga!"), bgcolor="red")
#             page.snack_bar.open = True
#             page.update()
#             return
        
#         progress_bar.visible = True
#         btn_analisar.disabled = True
#         page.update()
        
#         # Simulação de processamento (Aqui entrará a chamada da Groq no futuro)
#         time.sleep(2) 
        
#         progress_bar.visible = False
#         btn_analisar.disabled = False
#         resultado_card.visible = True
#         page.update()

#     def tratar_busca(e):
#         if not jd_input.value:
#             page.snack_bar = ft.SnackBar(ft.Text("Cole uma vaga para gerar a busca inteligente!"))
#             page.snack_bar.open = True
#             page.update()
#             return
        
#         page.snack_bar = ft.SnackBar(ft.Text("Groq analisando termos de busca... 🔍"))
#         page.snack_bar.open = True
#         page.update()

#         # IA extrai termos e Seek abre o Google Dorking
#         termos = extrair_termos_busca(jd_input.value)
#         seek.buscar_cvs_na_web(page, termos)

#     # --- Botões ---
#     progress_bar = ft.ProgressBar(width=400, color="blue", visible=False)
    
#     btn_analisar = ft.ElevatedButton(
#         "Analisar Currículo", 
#         on_click=analisar_click,
#         bgcolor=ft.colors.BLUE_700,
#         color=ft.colors.WHITE,
#         height=50,
#         expand=True
#     )

#     btn_pesquisa = ft.TextButton(
#         "Buscar candidatos na Web", 
#         icon=ft.icons.SEARCH, 
#         on_click=tratar_busca,
#         style=ft.ButtonStyle(color=ft.colors.BLUE_700)
#     )

#     # --- Layout ---
#     page.add(
#         header,
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
#         ft.Container(height=15),
#         ft.Row([btn_analisar]),
#         ft.Row([btn_pesquisa], alignment=ft.MainAxisAlignment.CENTER),
#         progress_bar,
#         resultado_card
#     )

# if __name__ == "__main__":
#     ft.app(target=main)