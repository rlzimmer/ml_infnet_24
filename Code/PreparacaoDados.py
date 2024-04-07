import mlflow
import warnings
import pandas as pd
from sklearn.model_selection import train_test_split

##---------------------------------------------------------------------------
warnings.filterwarnings('ignore')
randomState = 13
pteste = 0.2 #Exemplo: 0.2 equivale a 20%
#Montando o experimento para o MLFlow
mlflow.set_experiment("Kobe Bryant - Rafael Zimmer")
##---------------------------------------------------------------------------

#Lendo o parquet de DEV
bd = pd.read_parquet("Data/Raw/dataset_kobe_dev.parquet")

#Colunas importantes da base
cols = ['lat', 'lon', 'minutes_remaining', 'period', 'playoffs', 'shot_distance']

#Ver qual(is) tem dados nulos
dados_faltantes_por_coluna = bd.isnull().sum()
colunas_com_dados_faltantes = dados_faltantes_por_coluna[dados_faltantes_por_coluna > 0]
if colunas_com_dados_faltantes.empty:
    print("Não há dados faltantes na base de dados BD.")
else:
    print("Dados faltantes na base de dados BD:")
    print(colunas_com_dados_faltantes)

#Filtra os registros que tem a definição do shot_made_flag
bd_filtrado = bd[bd['shot_made_flag'].notnull()]

#Filtra somente os arremeços de 2 pontos
bd_filtrado = bd_filtrado[bd_filtrado['shot_type'] == '2PT Field Goal']

#Deixa no dataframe somente as colunas importantes
bd_dados = bd_filtrado[cols]

#Salva o dataframe filtrado
bd_dados.to_parquet("Data/Processed/data_filtered.parquet")

##---------------------------------------------------------------------------
#print(df["shot_type"].unique())
#print(df_dados.columns)
print(f"Dimensão do Base de Dados Original: {len(bd)}")
print(f"Dimensão do Base de Dados Filtrada: {len(bd_dados)}")
##---------------------------------------------------------------------------

#Início da separação dos dados
X = bd_dados.copy()
Y = bd_filtrado[['shot_made_flag']]

#print(X.shape)
#print(Y.shape)

#Separando treino e teste - com estratificação 80%-20%
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=(pteste), stratify=Y, random_state=randomState)

#Salva os dataframes de treino e teste
x_train.join(y_train).to_parquet("Data/Processed/base_train.parquet")
x_test.join(y_test).to_parquet("Data/Processed/base_test.parquet")

##---------------------------------------------------------------------------
#Criando o PreparacaoDados
##***************************************************************************
#Iniciando uma run do MlFlow para o pipeline de preparação de dados
with mlflow.start_run(run_name='PreparacaoDados'):
    mlflow.log_param("teste_percentual", pteste)
    mlflow.log_param("colunas_selecionadas", cols)
    mlflow.log_metric("base_treino_tamanho", len(x_train))
    mlflow.log_metric("base_teste_tamanho", len(x_test))

