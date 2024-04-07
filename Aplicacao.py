import mlflow
import warnings
import pandas as pd
import requests
from sklearn.metrics import log_loss, f1_score, recall_score, precision_score, accuracy_score, confusion_matrix
from pycaret.classification import *
import matplotlib.pyplot as plt
import seaborn as sns


##---------------------------------------------------------------------------
warnings.filterwarnings('ignore')
#Montando o experimento para o MLFlow
mlflow.set_experiment("Kobe Bryant - Rafael Zimmer")
##---------------------------------------------------------------------------

#Antes de tudo, precisa executar no console:
#mlflow models serve -m "runs:/[ID_mlflow_treinamento]/model_decision_tree" --no-conda -p 1234

##---------------------------------------------------------------------------

# Carregando a base de produção
bd = pd.read_parquet("Data/Raw/dataset_kobe_prod.parquet")

bd_original = bd.copy()
bd_original = bd_original[bd_original['shot_made_flag'].notnull()]

#Colunas importantes da base
cols = ['lat', 'lon', 'minutes_remaining', 'period', 'playoffs', 'shot_distance']

#Filtra os registros que tem a definição do shot_made_flag
bd = bd[bd['shot_made_flag'].notnull()]

#Deixa no dataframe somente as colunas importantes
bd = bd[cols]

#print(bd)

#Transforma os dados do dataframe em json
dados_json = bd.to_json(orient='split')

#Faz a requisição localmente para a API do MLFlow
responseMLFlow = requests.post(
    'http://127.0.0.1:6000/invocations',
    headers={'Content-Type':'application/json'},
    json={
        "dataframe_split": 
        {
            "columns": bd.columns.tolist(),
            "data": bd.values.tolist()
        }
    }
)

# Verificar a resposta for válida = 200
if responseMLFlow.status_code == 200:
    print("[OK] Dados recebidos do MLFlow")
    predicoes = responseMLFlow.json()
    
    #print(predicoes)

    # Calcula as métricas
    log_loss = log_loss(bd_original['shot_made_flag'].values, predicoes['predictions'])
    f1_score = f1_score(bd_original['shot_made_flag'].values, predicoes['predictions'])
    accuracy_score = accuracy_score(bd_original['shot_made_flag'].values, predicoes['predictions'])
    precision_score = precision_score(bd_original['shot_made_flag'].values, predicoes['predictions'])
    recall_score = recall_score(bd_original['shot_made_flag'].values, predicoes['predictions'])

    print(f"Predição Log Loss: {log_loss}")
    print(f"Predição F1 Score: {f1_score}")
    print(f"Predição accuracy Score: {accuracy_score}")
    print(f"Predição precision Score: {precision_score}")
    print(f"Predição recall Score: {recall_score}")


    #Monta o dataframe com os resultados
   
    bd_results = bd_original.copy()
    bd_results['Prediction'] = predicoes['predictions']
    #bd_results.insert(len(df_results.columns), "Prediction", predicoes['predictions'])
    #print(bd_results)
    
    #Criando gráfico Matriz de Confusão
    # Gerando a matriz de confusão
    matriz_conf = confusion_matrix(bd_original['shot_made_flag'].values, predicoes['predictions'])

    # Plotando a matriz de confusão
    plt.figure(figsize=(10,7))
    sns.heatmap(matriz_conf, annot=True, fmt="d", cmap="Greens", 
                xticklabels=["1.0", "0.0"], yticklabels=["1.0", "0.0"])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Class')
    plt.ylabel('True Class')
    #plt.show()
    plt.savefig("Docs/prod_Confusion_Matrix.png")


    #Agora armazenar no MLFlow
    with mlflow.start_run(run_name="PipelineAplicacao"):
        # Registro das métricas
        mlflow.log_metric("log_loss", log_loss)
        mlflow.log_metric("f1_score", f1_score)
        mlflow.log_metric("Accuracy", accuracy_score)
        mlflow.log_metric("Prec", precision_score)
        mlflow.log_metric("Recall", recall_score)
        mlflow.set_tag('model', 'Decision Tree Classifier')

        #print(mlflow.active_run().info.artifact_uri)

        #Salvando o dataframe com os resultados no mlflow
        bd_results.to_parquet(mlflow.active_run().info.artifact_uri + "/result.parquet")
    
else:
    print("[ERRO] Motivo:", responseMLFlow.text)
