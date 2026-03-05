import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os
import platform
import subprocess
import datetime
import math
import pathlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageTk
from itertools import count

def selecionaFonte(file_path):
    file_path.set(filedialog.askopenfilename(title="pega um .ttf ae pra tu ver como q é o esquema",filetypes=[("Fontes TrueType", "*.ttf")]))
    nome_letra=Path(file_path.get()).name
    if nome_letra:
        legenda_fonte.config(text=f"letra: {nome_letra}")
    return

def resetaFonte(file_path):
    file_path.set('Comic Sans MS')
    legenda_fonte.config(text=f"letra: padrão da firma!!")
    return

def getImages(path):
    images = []
    for file in ['*.png', '*.jpg', '*.jpeg', '*.JPEG', '*.JPG', '*.PNG']:
        images.extend(path.glob(f'**/{file}'))
    return images

def getDataMod(filepath):
    path = pathlib.Path(filepath)
    timestamp = path.stat().st_mtime
    time = datetime.datetime.fromtimestamp(timestamp)
    return str(time)

def stampImages(images, destino):
    img_qtd = len(images)
    for i, image in enumerate(images):
        img = Image.open(image)
        
        exif_data = img.getexif()
        date_time = exif_data.get(306, "Unknown")

        text = "magodavos esteve aqui..."

        try:
            date_time_array = date_time.split()
            date_array = date_time_array[0].split(':')
            time_array = date_time_array[1].split(':')
        except:
            date_time_array = getDataMod(img.filename).split()
            date_array = date_time_array[0].split('-')
            time_array = date_time_array[1].split(':')

        text = (f"{date_array[2]}/{date_array[1]}/{date_array[0]} {time_array[0]}:{time_array[1]}")

        porcentagem=int((i)/img_qtd*100)
        legenda_status.config(text=f"{porcentagem}%\n\ncarimbando {text} em: {img.filename}")
        legenda_status.update()

        nome = f'{image.stem}-MagoStamper2000{image.suffix}'

        img = ImageOps.exif_transpose(img)

        width, height = img.size

        big_side = max(width, height)

        font_size = math.ceil(big_side/35.45)
        font_stroke = math.ceil(font_size/21.66)
        margin = math.ceil(big_side/13.55)

        try:
            font = ImageFont.truetype(font_path.get(), font_size)
        except:
            font = ImageFont.truetype('Comic Sans MS', font_size)
 
        draw = ImageDraw.Draw(img)

        bbox = draw.textbbox((0, 0), text=text, font=font)
        textwidth = bbox[2] - bbox[0]
        textheight = bbox[3] - bbox[1]

        x = width - textwidth - margin
        y = height - textheight - margin

        draw.text((x, y), text, font = font, fill=(253, 162, 0), stroke_width=font_stroke, stroke_fill=(0, 0, 0))
        
        try:
            path_rel = image.relative_to(Path(origem_var.get()))
            subpasta = path_rel.parent
        except:
            subpasta = Path("")

        path_subpasta = Path(destino) / subpasta
        path_subpasta.mkdir(parents=True, exist_ok=True) 
        
        path_inteiro = path_subpasta / nome

        img.save(path_inteiro)

    legenda_status.config(text=f"terminei aq, tuas imagens tao em: {destino}")
    legenda_status.update()

    abrePasta(destino)

def abrePasta(path):
    if platform.system() == "Windows":
        os.startfile(path) 
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def selecionaPasta(path_var, legenda_var, prefix):
    pasta = filedialog.askdirectory(title=f"Selecionar {prefix}")
    if pasta:
        path_var.set(pasta)
        legenda_var.config(text=f"{prefix}: {pasta}")

def autoDestino(origem):
    nome_destino=f"{Path(origem).name} - MagoStamper2000"
    destino = Path(origem).parent / nome_destino
    destino.mkdir(exist_ok=True)

    destino_var.set(str(destino))
    legenda_destino.config(text=f"destino padrão po ta sem criatividade ne: {destino}")
    return str(destino)

def executar():
    try:
        origem = origem_var.get()
        if not origem: raise Exception("faltou a pasta de origem aklsjdyhfkjashdf poxa não é possível que vc esqueceu disso to até decepcionado papo reto")
        images = getImages(Path(origem))
        if not images: raise Exception("po aí tu me lança uma pasta sem imagens? qq tu quer q eu faça bruuuuhhhhhhh")
        destino = destino_var.get()
        if not destino: 
            destino = autoDestino(origem)
    except Exception as e:
        messagebox.showerror("deu erro kasjdkjhaskhdikhasdkjh", f"{e}")
        return
    
    stampImages(images, destino)

janela = tk.Tk()
janela.title("MagoStamper2000")

fonte_padrao = "Comic Sans MS"
origem_var = tk.StringVar()
destino_var = tk.StringVar()
font_path = tk.StringVar()

titulo = tk.Label(janela, text="MagoStamper2000", font=(fonte_padrao, 16, "bold"), fg="#5C0086")
titulo.pack(pady=10)

div_paths = tk.Frame(janela)
div_paths.pack(pady=10)

legenda_origem = tk.Label(div_paths, font=(fonte_padrao, 10), text="seleciona uma origem ae", wraplength=200, justify=tk.CENTER)
legenda_origem.grid(row=1, column=0, padx=10, pady=5)

legenda_destino = tk.Label(div_paths, font=(fonte_padrao, 10), text="nao esquece de selecionar o destino tbm ne durrrr, ou nao escolhe memo nao e deixa ser o destino padrão tlgd vc q sabe", wraplength=200, justify=tk.CENTER)
legenda_destino.grid(row=1, column=1, padx=10, pady=5)

legenda_fonte = tk.Label(div_paths, font=(fonte_padrao, 10), text="escolhe uma fonte senao vai a padrão também", wraplength=200, justify=tk.CENTER)
legenda_fonte.grid(row=2, column=2, padx=10, pady=5)

botao_origem = tk.Button(div_paths, font=(fonte_padrao, 10), text="escolhe a origem aq", command=lambda: selecionaPasta(origem_var, legenda_origem, "origem"), width=25, height=2)
botao_origem.grid(row=0, column=0, padx=10, pady=5)

botao_destino = tk.Button(div_paths, font=(fonte_padrao, 10), text="escolhe o destino aq", command=lambda: selecionaPasta(destino_var, legenda_destino, "destino"), width=25, height=2)
botao_destino.grid(row=0, column=1, padx=10, pady=5)

botao_fonte = tk.Button(div_paths, font=(fonte_padrao, 10), text="escolhe a fonte", command=lambda: selecionaFonte(font_path), width=25, height=2)
botao_fonte.grid(row=0, column=2, padx=10, pady=5)

botao_fonte = tk.Button(div_paths, font=(fonte_padrao, 10), text="reseta a letra", command=lambda: resetaFonte(font_path), width=25, height=2)
botao_fonte.grid(row=1, column=2, padx=10, pady=5)


legenda_status = tk.Label(font=(fonte_padrao, 10), text="fazendo bulhufas,,", wraplength=400, justify=tk.CENTER)
legenda_status.pack(pady=10)

div_coisar = tk.Frame(janela)
div_coisar.pack(pady=10)

botao_executar = tk.Button(div_coisar, font=(fonte_padrao, 10), text="carimbar!!", command=executar, width=10, height=1)
botao_executar.grid(row=0, column=0, padx=5)

botao_sair = tk.Button(div_coisar, font=(fonte_padrao, 10), text="adeus..", command=janela.destroy, width=10, height=1)
botao_sair.grid(row=0, column=1, padx=5)

div_magodavos = tk.Label(janela, font=(fonte_padrao, 8), text="código insalubre e más práticas - magodavos")
div_magodavos.pack(side=tk.BOTTOM, fill=tk.X)

janela.mainloop()