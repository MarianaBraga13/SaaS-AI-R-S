import flet as ft
import time

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
            # Guardamos o caminho no ambiente da sessão
            page.session.set("pdf_path", e.files[0].path)
        else:
            file_name_text.value = "Nenhum arquivo selecionado"
        page.update()

    pick_files_dialog = ft.FilePicker(on_result=handle_file_result)
    page.overlay.append(pick_files_dialog)
    
    file_name_text = ft.Text("Nenhum arquivo selecionado", size=12, italic=True)

    # --- UI ---
    header = ft.Text("RecrutAI 🤖", size=32, weight="bold", color=ft.colors.BLUE_700)
    
    jd_input = ft.TextField(
        label="Cole a Job Description aqui",
        multiline=True,
        min_lines=5,
        hint_text="Ex: Requisitos: Python, SQL..."
    )

    resultado_card = ft.Column(visible=False, controls=[
        ft.Divider(),
        ft.Text("Diagnóstico do Candidato", size=22, weight="bold"),
        ft.Container(
            content=ft.Text("Resultado da análise aparecerá aqui...", size=14),
            padding=20, 
            bgcolor=ft.colors.GREY_50,
            border_radius=15
        )
    ])

    def analisar_click(e):
        if not jd_input.value or "Nenhum arquivo" in file_name_text.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos!"))
            page.snack_bar.open = True
            page.update()
            return
        
        progress_bar.visible = True
        page.update()
        time.sleep(2) 
        progress_bar.visible = False
        resultado_card.visible = True
        page.update()

    progress_bar = ft.ProgressBar(width=400, color=ft.colors.BLUE, visible=False)
    
    btn_analisar = ft.ElevatedButton(
        "Analisar Currículo", 
        on_click=analisar_click,
        bgcolor=ft.colors.BLUE_700,
        color=ft.colors.WHITE
    )

    page.add(
        header,
        ft.Text("Otimize sua triagem de candidatos com IA."),
        ft.Container(height=10), # Espaçador
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
        btn_analisar,
        progress_bar,
        resultado_card
    )

if __name__ == "__main__":
    ft.app(target=main)