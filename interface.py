import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from deteccao_texto_spacy import buscar_texto
from ocr_relatorio import extrair_texto
from pdf2image import convert_from_path
import os
import shutil


class Atributo:
    def __init__(self):
        self.nome = None
        self.valor = None

    def inicializar_nome(self):
        self.nome = self.campo_atributo.get()

    def desenhar_painel(self, frame):
        frame_ind = tk.Frame(frame)
        frame_ind.pack(pady=5)

        lbl_atributo = tk.Label(frame_ind, text="Atributo: ")
        lbl_atributo.pack(padx=20, side=tk.LEFT)

        self.campo_atributo = tk.Entry(frame_ind)
        self.campo_atributo.pack(side=tk.LEFT)

        self.campo_valor = tk.Entry(frame_ind)
        self.campo_valor.pack(side=tk.RIGHT)

        lbl_valor = tk.Label(frame_ind, text="Valor: ")
        lbl_valor.pack(padx=20, side=tk.RIGHT)

    def procurar_no_txt(self):
        busca = buscar_texto(self.nome, "relatorioTranscrito")
        self.campo_valor.delete(0, tk.END)  # Limpa o conteúdo atual
        self.campo_valor.insert(0, busca)  # Insere o novo valor


class Aplicacao:
    def __init__(self):
        self.atributos = []

    def adicionar_atributo(self):
        atributo = Atributo()
        self.atributos.append(atributo)
        atributo.desenhar_painel(self.frame_atributos)

    def procurar_atributos(self):
        for atributo in self.atributos:
            atributo.inicializar_nome()
            if atributo.nome not in ["", None]:
                atributo.procurar_no_txt()

    def selecionar_pdf(self):
        # Abre uma janela de diálogo para selecionar um arquivo PDF
        caminho_pdf = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf")],
        )

        # Verifica se um arquivo foi selecionado
        if caminho_pdf:
            try:
                # Converte o PDF em imagens
                paginas = convert_from_path(
                    caminho_pdf,
                    poppler_path=r"C:\Users\mateu\Downloads\poppler-24.02.0\Library\bin",
                )
                num_paginas = len(paginas)

                # Cria a pasta para armazenar os resultados da extração de texto
                pasta_resultados = "relatorioTranscrito"

                if os.path.exists(pasta_resultados):
                    try:
                        shutil.rmtree(pasta_resultados)
                    except OSError as e:
                        print(f"Erro: {pasta_resultados} : {e.strerror}")
                os.makedirs(pasta_resultados)
                file = open(f"{pasta_resultados}/relatorioEmTexto.txt", "w+")
                file.write("")
                file.close()

                # Processa todas as páginas
                for numero_pagina, pagina in enumerate(paginas, start=1):
                    caminho_imagem = os.path.join(
                        pasta_resultados, f"pagina_{numero_pagina}.jpg"
                    )
                    pagina.save(caminho_imagem, "JPEG")

                    extrair_texto(caminho_imagem, pasta_resultados)

                # Exibe a primeira página do PDF como imagem na interface
                imagem = paginas[0]
                imagem = imagem.resize(
                    (250, 250), Image.Resampling.LANCZOS
                )  # Redimensiona a imagem

                imagem_tk = ImageTk.PhotoImage(imagem)
                self.label_imagem.config(image=imagem_tk)
                self.label_imagem.image = imagem_tk  # Mantém uma referência da imagem

                # Atualiza o rótulo do caminho do arquivo
                self.label_caminho.config(
                    text=f"PDF: {caminho_pdf} - {num_paginas} páginas processadas"
                )

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o PDF: {e}")

    def selecionar_imagem(self):
        # Abre uma janela de diálogo para selecionar um arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        )

        # Verifica se um arquivo foi selecionado
        if caminho_arquivo:
            try:
                # Cria a pasta para armazenar os resultados da extração de texto
                pasta_resultados = "relatorioTranscrito"
                if os.path.exists(pasta_resultados):
                    try:
                        shutil.rmtree(pasta_resultados)
                    except OSError as e:
                        print(f"Erro: {pasta_resultados} : {e.strerror}")
                os.makedirs(pasta_resultados)
                file = open(f"{pasta_resultados}/relatorioEmTexto.txt", "w+")
                file.write("")
                file.close()
                extrair_texto(caminho_arquivo, "relatorioTranscrito")
                # Carrega a imagem usando PIL
                imagem = Image.open(caminho_arquivo)
                imagem = imagem.resize(
                    (250, 250), Image.Resampling.LANCZOS
                )  # Redimensiona a imagem

                # Converte a imagem para um formato que o Tkinter pode exibir
                imagem_tk = ImageTk.PhotoImage(imagem)

                # Exibe a imagem no label
                self.label_imagem.config(image=imagem_tk)
                self.label_imagem.image = imagem_tk  # Mantém uma referência da imagem

                # Atualiza o rótulo do caminho do arquivo
                self.label_caminho.config(text=caminho_arquivo)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")

    def run(self):
        # Cria a janela principal
        janela = tk.Tk()
        janela.geometry("500x700")
        janela.iconbitmap("icone.ico")
        janela.title("Detecção de atributos em relatório")

        # Cria um Canvas
        self.canvas = tk.Canvas(janela)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Adiciona barras de rolagem
        self.scrollbar_vertical = tk.Scrollbar(
            janela, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuração do Canvas
        self.canvas.configure(
            yscrollcommand=self.scrollbar_vertical.set,
        )
        self.canvas.bind("<Configure>", self.on_canvas_configure_client)

        # Adiciona um frame para o conteúdo
        self.frame_conteudo = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_conteudo, anchor="nw")

        # Cria e posiciona o botão para selecionar a imagem
        botao_selecionar = tk.Button(
            self.frame_conteudo,
            text="Selecionar Imagem",
            command=self.selecionar_imagem,
        )
        botao_selecionar.pack(pady=10)

        botao_selecionar_pdf = tk.Button(
            self.frame_conteudo,
            text="Selecionar PDF",
            command=self.selecionar_pdf,
        )
        botao_selecionar_pdf.pack(pady=10)

        # Cria e posiciona um label para exibir a imagem
        self.label_imagem = tk.Label(self.frame_conteudo)
        self.label_imagem.pack(pady=10)

        # Cria e posiciona um label para mostrar o caminho do arquivo selecionado
        self.label_caminho = tk.Label(
            self.frame_conteudo, text="Nenhum arquivo selecionado"
        )
        self.label_caminho.pack(pady=10)

        separator = tk.Frame(self.frame_conteudo, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=20, pady=5)

        frame_info = tk.Frame(self.frame_conteudo)
        frame_info.pack(
            pady=10,
            padx=30,
        )

        label_informacoes = tk.Label(frame_info, text="Informações para buscar")
        label_informacoes.pack(side=tk.LEFT)

        self.frame_atributos = tk.Frame(self.frame_conteudo)
        self.frame_atributos.pack(
            pady=10,
            padx=30,
        )

        botao_procurar_info = tk.Button(
            frame_info,
            text="Procurar atributo(s)",
            command=self.procurar_atributos,
        )
        botao_procurar_info.pack(
            padx=10,
            side=tk.RIGHT,
        )

        botao_add_info = tk.Button(
            frame_info,
            text="Adicionar atributo",
            command=self.adicionar_atributo,
        )
        botao_add_info.pack(
            padx=10,
            side=tk.RIGHT,
        )

        # Inicia o loop principal do Tkinter
        janela.mainloop()

    def on_canvas_configure_client(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
