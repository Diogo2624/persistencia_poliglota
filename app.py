import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from db_sqlite import criar_tabela, inserir_cidade, listar_cidades
from db_mongo import inserir_local, listar_locais
from geoprocessamento import locais_proximos

# Criar tabelas no SQLite
criar_tabela()

st.title("Persistência Poliglota: SQLite + MongoDB + Geoprocessamento")

menu = st.sidebar.selectbox("Menu", ["Cadastro Cidade", "Cadastro Local", "Consultar", "Mapa"])

if menu == "Cadastro Cidade":
    st.subheader("Cadastrar Cidade (SQLite)")
    nome = st.text_input("Nome da cidade")
    estado = st.text_input("Estado")
    if st.button("Salvar"):
        inserir_cidade(nome, estado)
        st.success("Cidade cadastrada!")

elif menu == "Cadastro Local":
    st.subheader("Cadastrar Local (MongoDB)")
    nome_local = st.text_input("Nome do local")
    cidade = st.text_input("Cidade")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição")
    if st.button("Salvar"):
        inserir_local(nome_local, cidade, latitude, longitude, descricao)
        st.success("Local cadastrado!")

elif menu == "Consultar":
    st.subheader("Consultar Locais")
    cidades = listar_cidades()
    if cidades:
        opcao = st.selectbox("Selecione a cidade", [c[1] for c in cidades])
        locais = listar_locais()
        locais_cidade = [l for l in locais if l["cidade"] == opcao]
        st.write(locais_cidade)
    else:
        st.warning("Nenhuma cidade cadastrada.")

elif menu == "Mapa":
    st.subheader("Visualizar Locais no Mapa")
    locais = listar_locais()
    if locais:
        m = folium.Map(location=[-15.793889, -47.882778], zoom_start=5)
        for local in locais:
            folium.Marker(
                [local["coordenadas"]["latitude"], local["coordenadas"]["longitude"]],
                popup=f"{local['nome_local']} - {local['descricao']}"
            ).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.warning("Nenhum local cadastrado.")