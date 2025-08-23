import pandas as pd
import streamlit as st 
from html_css import CSS_RODAPE, HTML_RODAPE
from utils import call_llm

st.set_page_config(layout="wide")
st.title('📋Extrator de texto')
st.divider()

result = None
sentimento = None
emoji = None
justificativa_lista = []
produto_lista = []

if 'llm_results' not in st.session_state:
    st.session_state['llm_results'] = None

txt_input, txt_output, lists = st.columns([0.5, 0.25, 0.25])

with txt_input:
    st.header("Entrada de texto")
    user_text = st.text_area(label='Insira aqui o comentário para ver a LLm em ação', height=300)

    btn_exe = st.button('Analisar Texto')

    if btn_exe:
        if user_text:
            with st.spinner('Analisando, aguarde...'):
                result = call_llm(user_text)
                st.session_state['llm_results'] = result
                sentimento = result.sentimento
                justificativa_lista = [i for i in result.justificativa.split(',')]
                produto_lista = [i for i in result.produtos]

                if sentimento == 'Positivo':
                    emoji = '😃'
                
                elif sentimento == 'Neutro':
                    emoji = '😐'

                elif sentimento == 'Negativo':
                    emoji = '🤬'

        else:
            st.warning(' Insira um texto')



with txt_output:
    st.header("Resultados")
    if st.session_state.llm_results:
        st.metric(label='Sentimento', value=sentimento + emoji)

with lists:
    if st.session_state.llm_results:
        st.markdown('#### **Justificativas:**')
        for i in justificativa_lista:
            st.markdown(f'- {i}')
        
        st.divider()
        st.markdown('#### **Produtos:**')
        for i in produto_lista:
            st.markdown(f'- {i}')


# CSS para fixar o rodapé no final da página
st.markdown(CSS_RODAPE, unsafe_allow_html=True)
st.markdown(HTML_RODAPE, unsafe_allow_html=True)