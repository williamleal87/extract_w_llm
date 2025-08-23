from dotenv import load_dotenv
import os 
from typing import List, Literal, Optional

import pandas as pd
from pydantic import Field, BaseModel
from langchain.chat_models import init_chat_model

load_dotenv(dotenv_path='.setup/.env')

model = os.getenv('MODEL')
provider = os.getenv('PROVIDER')

llm = init_chat_model(model=model, model_provider=provider, temperature=0)

class Collect(BaseModel):
    sentimento:Literal['Positivo', 'Neutro', 'Negativo'] = Field(..., description='Avaliar o sentimento predominante da mensagem', examples=['Positivo', 'Neutro', 'Negativo'])
    produtos:List[str] =  Field(..., description='Identificar quais produtos são mencionados na mensagem', examples=['televisão', 'sofá'])
    justificativa: Optional[str] = Field(None,description='Fornecer uma justificativa para o sentimento, como "prazo de entrega", "mau atendimento", "preço alto", "baixa qualidade" (para sentimento negativo) ou "bom atendimento", "qualidade do produto", "entrega rápida" (para sentimento positivo).')

llm_coletor = llm.with_structured_output(Collect)

def call_llm(input):
    result = llm_coletor.invoke(input)
    df = pd.DataFrame(result.model_dump())
    return result