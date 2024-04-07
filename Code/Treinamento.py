import mlflow
import warnings
import pandas as pd
import pycaret.classification as pc
import shutil
import matplotlib.pyplot as plt
from PIL import Image
from pycaret.classification import setup, create_model, predict_model, save_model, plot_model
from sklearn.metrics import log_loss, f1_score
##---------------------------------------------------------------------------
warnings.filterwarnings('ignore')
rl_modelPKL = 'Data/Modeling/rl_model_treined'
dt_modelPKL = 'Data/Modeling/dt_model_treined'
#Montando o experimento para o MLFlow
mlflow.set_experiment("Kobe Bryant - Rafael Zimmer")
##---------------------------------------------------------------------------

#Carrega os dados de treino e teste
bd_train = pd.read_parquet('Data/Processed/base_train.parquet')
bd_test = pd.read_parquet('Data/Processed/base_test.parquet')

#print(bd_train)
#print(bd_test)

with mlflow.start_run(run_name='Treinamento'):
    #Configurando o setup do PyCaret
    setup(data=bd_train, target='shot_made_flag')
    
    #**********************************************************
    # Regressão Logística
    #**********************************************************
    #Cria o modelo pelo PyCaret
    lr_model = create_model('lr')
    #Faz a predição do modelo
    lr_predicao = predict_model(lr_model, data=bd_test)
    #Salva as metricas no MLFlow
    mlflow.log_metric("logistic_regression_log_loss", log_loss(bd_test['shot_made_flag'], lr_predicao['prediction_score']))
    mlflow.log_metric("logistic_regression_f1_score", f1_score(bd_test['shot_made_flag'], lr_predicao['prediction_label']))
    #Salva as tags no MLFlow
    mlflow.set_tag('model', 'Logistic Regression')
    mlflow.set_tag('algorithm', 'PyCaret')
    #Salva o modelo em Artifacts
    mlflow.sklearn.log_model(lr_model, "model_logistic_regression")
    #Salva o modelo trainado para reutilização
    save_model(lr_model, rl_modelPKL)
    #Salva o pickle no MLFlow
    mlflow.log_artifact(rl_modelPKL + '.pkl')
    #**********************************************************

    #**********************************************************
    # Árvore de Decisão
    #**********************************************************
    #Cria o modelo pelo PyCaret
    dt_model = create_model('dt')
    #Faz a predição do modelo
    dt_predicao = predict_model(dt_model, data=bd_test)
    #Salva as metricas no MLFlow
    mlflow.log_metric("decision_tree_log_loss", log_loss(bd_test['shot_made_flag'], dt_predicao['prediction_score']))
    mlflow.log_metric("decision_tree_f1_score", f1_score(bd_test['shot_made_flag'], dt_predicao['prediction_label']))
    #Salva as tags no MLFlow
    mlflow.set_tag('model', 'Decision Tree Classifier')
    mlflow.set_tag('algorithm', 'PyCaret')
    #Salva o modelo em Artifacts
    mlflow.sklearn.log_model(dt_model, "model_decision_tree")
    #Salva o modelo trainado para reutilização
    save_model(dt_model, dt_modelPKL)
    #Salva o pickle no MLFlow
    mlflow.log_artifact(dt_modelPKL + '.pkl')
  
