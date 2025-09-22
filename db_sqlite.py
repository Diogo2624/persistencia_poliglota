import sqlite3

DB_NAME = "dados.db"

def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_cidade(nome, estado):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cidades (nome, estado) VALUES (?, ?)", (nome, estado))
    conn.commit()
    conn.close()

def listar_cidades():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cidades")
    cidades = cursor.fetchall()
    conn.close()
    return cidades