import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from spacytest import buscar_texto
from OCR2 import extrair_texto


class Aplicacao:
    def __init__(self):
        self.atributos = []

    def adicionar_atributo(self, frame):
        frame_ind = tk.Frame()
        frame_ind.pack(pady=5)
        lbl_atributo = tk.Label(frame_ind, text="Atributo: ")
        lbl_atributo.pack(padx=10, side=tk.LEFT)
        campo_atributo = tk.Entry(frame_ind)
        campo_atributo.pack(side=tk.RIGHT)

    def procurar_atributo(self):
        pass

    def selecionar_imagem(self):
        # Abre uma janela de diálogo para selecionar um arquivo
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        )

        # Verifica se um arquivo foi selecionado
        if caminho_arquivo:
            try:
                extrair_texto(caminho_arquivo, "testeInterface")
                buscar_texto("IPAP min.", "testeInterface")
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
        janela.geometry("500x500")
        janela.title("Detecção de atributos")

        # Cria e posiciona o botão para selecionar a imagem
        botao_selecionar = tk.Button(
            janela, text="Selecionar Imagem", command=self.selecionar_imagem
        )
        botao_selecionar.pack(pady=10)

        # Cria e posiciona um label para exibir a imagem
        self.label_imagem = tk.Label(janela)
        self.label_imagem.pack(pady=10)

        # Cria e posiciona um label para mostrar o caminho do arquivo selecionado
        self.label_caminho = tk.Label(janela, text="Nenhum arquivo selecionado")
        self.label_caminho.pack(pady=10)

        separator = tk.Frame(janela, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill="x", padx=5, pady=5)

        frame_info = tk.Frame()
        frame_info.pack(pady=10)

        label_informacoes = tk.Label(frame_info, text="Informações para buscar")
        label_informacoes.pack(side=tk.LEFT)

        frame_atributos = tk.Frame()
        frame_atributos.pack(pady=10, padx=20)

        botao_procurar_info = tk.Button(
            frame_info,
            text="Procurar atributo(s)",
            command=self.procurar_atributo,
        )
        botao_procurar_info.pack(
            padx=10,
            side=tk.RIGHT,
        )

        botao_add_info = tk.Button(
            frame_info,
            text="Adicionar atributo",
            command=lambda: self.adicionar_atributo(frame_atributos),
        )
        botao_add_info.pack(
            padx=10,
            side=tk.RIGHT,
        )

        # Inicia o loop principal do Tkinter
        janela.mainloop()


if __name__ == "__main__":
    app = Aplicacao()
    app.run()
