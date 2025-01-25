#SITUAÇÃO PROBLEMA: CÁLCULO DE HORAS TRABALHADAS EM UM ESCRITÓRIO DE ADVOCACIA

import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# conectar ou criar o banco 
def conectar():
    return sqlite3.connect('usuarios.db')

# criar tabela se ela não existir
def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
      CREATE TABLE IF NOT EXISTS usuarios(
             id INTEGER PRIMARY KEY,
             cliente TEXT, 
             hinicio INTEGER, 
             hsaida INTEGER,   
             htotal INTEGER, 
             atividade TEXT, 
             advogado TEXT           
        )
    ''')
    conn.commit()
    conn.close()

#formula calculadora horas

# h1 = int(input('?'))
# h2 = int(input('?'))

#print(h1 - h2)

# inserindo dados no banco de dados
def agregar_usuarios():
    cliente = entry_cliente.get()
    hinicio = float(entry_hinicio.get())
    hsaida = float(entry_hsaida.get())
    htotal = hsaida-hinicio
    atividade = entry_atividade.get()
    advogado = entry_advogado.get()
    

    if cliente and hinicio and hsaida and htotal and atividade and advogado:
       conn = conectar()
       c = conn.cursor()
       c.execute('INSERT INTO usuarios(cliente, hinicio, hsaida, htotal, atividade, advogado) VALUES(?, ?, ?, ?, ?, ?)', (cliente, hinicio, hsaida, htotal, atividade, advogado))
       conn.commit()
       conn.close()
       messagebox.showinfo('Inseridos', 'Os dados estão no banco de dados') 
       mostrar_usuarios()
    else:
       messagebox.showerror('Erro', 'Ocorreu um erro, os dados não foram inseridos')

# mostrar dados 
def mostrar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * from usuarios')
    usuarios = c.fetchall()
    for usuario in usuarios:
        tree.insert("", "end", values=(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4], usuario [5], usuario [6]))
    conn.close()

# deletar dados 
def eliminar_usuario():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        conn = conectar() 
        c = conn.cursor()
        c.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Exito', 'DADOS DELETADOS')
        mostrar_usuarios()
    else:
        messagebox.showerror('Erro', 'Dados não deletados')

def atualizar_usuario():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        novo_cliente = entry_cliente.get()
        nova_hinicio = entry_hinicio.get()
        nova_hsaida = entry_hsaida.get()
        nova_atividade = entry_atividade.get ()
        novo_advogado = entry_advogado.get()

        if novo_cliente and nova_hinicio and nova_hsaida and nova_atividade and novo_advogado:
            conn = conectar() 
            c = conn.cursor()
            c.execute('UPDATE usuarios SET cliente = ?, hinicio = ?, hsaida= ?, atividade = ?, advogado = ?  WHERE id = ?',
                     (novo_cliente, nova_hinicio, novo_advogado, nova_atividade, novo_advogado, user_id)) 
            conn.commit()
            conn.close()
            messagebox.showinfo('Exito', 'Dados alterados')
            mostrar_usuarios()
        else:
            messagebox.showerror('Erro', 'Dados não inseridos')
    else:
        messagebox.showwarning('Atenção', 'O dado não foi selecionado')

janela = tk.Tk()
janela.title('CRUD USUARIOS')

label_cliente = tk.Label(janela, text='CLIENTE')
label_cliente.grid(row=0, column=0, padx=10, pady=10)
entry_cliente = tk.Entry(janela)
entry_cliente.grid(row=0, column=1, padx=10, pady=10)

label_hinicio = tk.Label(janela, text='H/INICIO')
label_hinicio.grid(row=1, column=0, padx=10, pady=10)
entry_hinicio = tk.Entry(janela)
entry_hinicio.grid(row=1, column=1, padx=10, pady=10)

label_hsaida = tk.Label(janela, text='H/SAIDA')
label_hsaida.grid(row=2, column=0, padx=10, pady=10)
entry_hsaida = tk.Entry(janela)
entry_hsaida.grid(row=2, column=1, padx=10, pady=10)


label_atividade = tk.Label(janela, text='ATIVIDADE')
label_atividade.grid(row=3, column=0, padx=10, pady=10)
entry_atividade = tk.Entry(janela)
entry_atividade.grid(row=3, column=1, padx=10, pady=10)

label_advogado = tk.Label(janela, text='ADVOGADO')
label_advogado.grid(row=4, column=0, padx=10, pady=10)
entry_advogado = tk.Entry(janela)
entry_advogado.grid(row=4, column=1, padx=10, pady=10)


btn_agregar = tk.Button(janela, text='INSERIR DADOS', command=agregar_usuarios)
btn_agregar.grid(row=1, column=6, columnspan=2, padx=10, pady=10)

btn_atualizar = tk.Button(janela, text='ATUALIZAR DADOS', command=atualizar_usuario)
btn_atualizar.grid(row=2, column=6, columnspan=2, padx=10, pady=10)

btn_deletar = tk.Button(janela, text='DELETAR DADOS', command=eliminar_usuario)
btn_deletar.grid(row=3, column=6, columnspan=2, padx=10, pady=10)

columns = ('ID', 'CLIENTE', 'H/INICIO', 'H/SAIDA', 'H/TOTAL', 'ATIVIDADE', 'ADVOGADO')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_usuarios()

janela.mainloop()