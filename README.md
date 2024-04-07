# Projeto: Engenharia de Machine Learning [24E1_3]

Este repositório contém um código em Python para um projeto final da disciplina Engenharia de Machine Learning.

# Descrição do Projeto Final
O projeto consiste nas seguintes atividades/questões:

1. A solução criada nesse projeto deve ser disponibilizada em repositório git e disponibilizada em servidor de repositórios (Github (recomendado), Bitbucket ou Gitlab). O projeto deve obedecer o Framework TDSP da Microsoft (estrutura de arquivos, arquivo requirements.txt e arquivo README). Todos os artefatos produzidos deverão conter informações referentes a esse projeto (não serão aceitos documentos vazios ou fora de contexto). Escreva o link para seu repositório. 

2. Iremos desenvolver um preditor de arremessos usando duas abordagens (regressão e classificação) para prever se o "Black Mamba" (apelido de Kobe) acertou ou errou a cesta.
Baixe os dados de desenvolvimento e produção aqui (datasets: dataset_kobe_dev.parquet e dataset_kobe_prod.parquet). Salve-os numa pasta /data/raw na raiz do seu repositório.
Para começar o desenvolvimento, desenhe um diagrama que demonstra todas as etapas necessárias em um projeto de inteligência artificial, desde a aquisição de dados, passando pela criação dos modelos, indo até a operação do modelo.

3. Descreva a importância de implementar pipelines de desenvolvimento e produção numa solução de aprendizado de máquinas.

4. Como as ferramentas Streamlit, MLFlow, PyCaret e Scikit-Learn auxiliam na construção dos pipelines descritos anteriormente? A resposta deve abranger os seguintes aspectos:
    - Rastreamento de experimentos;
    - Funções de treinamento;
    - Monitoramento da saúde do modelo;
    - Atualização de modelo;
    - Provisionamento (Deployment).

5. Com base no diagrama realizado na questão 2, aponte os artefatos que serão criados ao longo de um projeto. Para cada artefato, indique qual seu objetivo.

6. Implemente o pipeline de processamento de dados com o mlflow, rodada (run) com o nome "PreparacaoDados":
    - Os dados devem estar localizados em "/data/raw/dataset_kobe_dev.parquet" e "/data/raw/dataset_kobe_prod.parquet" 
    - Observe que há dados faltantes na base de dados! As linhas que possuem dados faltantes devem ser desconsideradas. Você também irá filtrar os dados onde o valor de shot_type for igual à 2PT Field Goal. Ainda, para esse exercício serão apenas consideradas as colunas: 
        - lat
        - lng
        - minutes_remaining
        - period
        - playoffs
        - shot_distance
        - A variável shot_made_flag será seu alvo, onde 0 indica que Kobe errou e 1 que a cesta foi realizada. O dataset resultante será armazenado na pasta "/data/processed/data_filtered.parquet". Ainda sobre essa seleção, qual a dimensão resultante do dataset?

    - Separe os dados em treino (80%) e teste (20 %) usando uma escolha aleatória e estratificada. Armazene os datasets resultantes em "/Data/processed/base_{train|test}.parquet . Explique como a escolha de treino e teste afetam o resultado do modelo final. Quais estratégias ajudam a minimizar os efeitos de viés de dados.
    - Registre os parâmetros (% teste) e métricas (tamanho de cada base) no MlFlow

7. Implementar o pipeline de treinamento do modelo com o MlFlow usando o nome "Treinamento"
    - Com os dados separados para treinamento, treine um modelo com regressão logística do sklearn usando a biblioteca pyCaret.
    - Registre a função custo "log loss" usando a base de teste
    - Com os dados separados para treinamento, treine um modelo de classificação do sklearn usando a biblioteca pyCaret. A escolha do algoritmo de classificação é livre. Justifique sua escolha.
    - Registre a função custo "log loss" e F1_score para esse novo modelo

8. Registre o modelo de classificação e o sirva como uma API local através do MLFlow. Desenvolva um pipeline de aplicação (aplicacao.py) para carregar a base de produção (/data/raw/dataset_kobe_prod.parquet) e para fornecer ao modelo através da biblioteca requests. Nomeie a rodada (run) do mlflow como “PipelineAplicacao” e publique, tanto uma tabela com os resultados obtidos (artefato como .parquet), quanto log as métricas do novo log loss e f1_score do modelo.
    - O modelo é aderente a essa nova base? O que mudou entre uma base e outra? Justifique.
    - Descreva como podemos monitorar a saúde do modelo no cenário com e sem a disponibilidade da variável resposta para o modelo em operação
    - Descreva as estratégias reativa e preditiva de retreinamento para o modelo em operação.

9. Implemente um dashboard de monitoramento da operação usando Streamlit.

10. Crie uma apresentação em formato de Slides com os resultados, figuras, links de interesse (git, Streamlit, etc.) e print-screens que o aluno julgar necessário para demonstrar as atividades.

# Como Usar 
Pré-requisitos: Certifique-se de ter o Python instalado, juntamente com as bibliotecas Pandas, Scikit-learn, Matplotlib, Pycaret, Mlflow, streamlit, seaborn, shap, dagster, langchain, 
warnings, plotly, ipywidgets, requests

Clonando o Repositório: Clone este repositório em seu ambiente local.

Configurar um Ambiente Virtual (Opcional, mas Recomendado).

Instale as Dependências.

Executando o Código: Leia o arquivo Python ComoExecutarAmbiente.md (VER Ordem de execução por dentro do Visual Code)

# Estrutura do Código

PreparacaoDados.py: Contém as informações de preparação das bases de teste e treino para execução do projeto.

Treinamento.py: Contém as etapas de treinamento e validação do melhor modelo (Regressão Logistica/Árvore de Decisão) no projeto.

Aplicacao.py: Contém as etapas de utilização do melhor modelo nos dados da base original do projeto.

Dashboard.py: Contém a elaboração do dashboard a partir do uso do streamlit.

README.md: Este arquivo, fornecendo informações sobre o projeto e instruções para utilização.

AnaliseExploratoria.ipynb: Este arquivo possui uma série de etapas para avaliação de métricas e elaboração de plots para o trabalho.


# Ordem de execução por dentro do Visual Code:
A. Terminal -> New Terminal e executar: mlflow server --host 127.0.0.1 --port 5000

B. Executar o script: PreparacaoDados.py

C. Executar o script: Treinamento.py

D. Dentro do UI do MLFlow, pegar o ID do Run "Treinamento" do model_decision_tree

E. Executar o comando para servir o modelo por API da MLFlow

Visual Code -> Terminal -> New Terminal e executar: 

mlflow models serve -m "runs:/[ID Treinamento]/model_decision_tree" --no-conda -p 6000
F. Executar o script: Aplicacao.py

G. Executar o comando para iniciar o Streamlit:

Visual Code -> Terminal -> New Terminal e executar:

streamlit run d:/Documentos/Infnet/Repositorio/Code/Dashboard.py
H. Automaticamente vai abrir a página do Streamlit

