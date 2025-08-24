import pandas as pd
import streamlit as st 
from html_css import CSS_RODAPE, HTML_RODAPE
from utils import call_llm
import os

st.set_page_config(layout="wide")
st.title('📋Extrator de texto')
st.divider()

# Declaração inicial das variáveis
result = None
sentimento = None
emoji = None
justificativa_lista = []
produto_lista = []

if 'llm_results' not in st.session_state:
    st.session_state['llm_results'] = None

txt_input, txt_output, list_just, list_prod = st.columns([0.4, 0.2, 0.2, 0.2])

with txt_input:
    st.markdown('#### **Entrada de texto:**')
    user_text = st.text_area(label='Insira aqui o comentário para ver a LLm em ação', height=150)

    btn_exe = st.button('Analisar Texto')

    if btn_exe:
        if user_text:
            with st.spinner('Analisando, aguarde...'):
                result = call_llm(user_text)

            # Verifica se a chamada da LLM retornou um resultado válido
            if result:
                st.session_state['llm_results'] = result
                sentimento = result.sentimento
                justificativa_lista = [i for i in result.justificativa]
                produto_lista = [i for i in result.produtos]

                if sentimento == 'Positivo':
                    emoji = '😃'
                elif sentimento == 'Neutro':
                    emoji = '😐'
                elif sentimento == 'Negativo':
                    emoji = '🤬'
            else:
                # Se o resultado for nulo, exibe uma mensagem de erro
                st.error("Não foi possível obter um resultado da LLM. Verifique as configurações e a chave da API.")

        else:
            st.warning('Insira um texto')

with txt_output:
    # Usa o estado da sessão para evitar erros
    if st.session_state.llm_results:
        st.markdown('#### **Sentimento:**')
        sentimento_display = st.session_state.llm_results.sentimento
        emoji_display = ''
        if sentimento_display == 'Positivo':
            emoji_display = '😃'
        elif sentimento_display == 'Neutro':
            emoji_display = '😐'
        elif sentimento_display == 'Negativo':
            emoji_display = '🤬'
        
        st.markdown(f'# {sentimento_display}{emoji_display}')

with list_just:
    # Usa o estado da sessão para exibir as listas
    if st.session_state.llm_results:
        justificativa_lista_display = [i for i in st.session_state.llm_results.justificativa]        
        st.markdown('#### **Justificativas:**')
        for i in justificativa_lista_display:
            st.markdown(f'- {i}')
        

with list_prod:
    # Usa o estado da sessão para exibir as listas
    if st.session_state.llm_results:
        produto_lista_display = [i for i in st.session_state.llm_results.produtos]
        
        st.markdown('#### **Produtos:**')
        for i in produto_lista_display:
            st.markdown(f'- {i}')

# CSS para fixar o rodapé no final da página
st.markdown(CSS_RODAPE, unsafe_allow_html=True)
st.markdown(HTML_RODAPE, unsafe_allow_html=True)
