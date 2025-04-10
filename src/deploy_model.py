#!/usr/bin/env python
# Script para implantar manualmente o modelo de previsão de vendas de sorvete

import os
import argparse
import time
import pandas as pd
import numpy as np
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration
)

def authenticate_azure_ml(resource_group, workspace):
    """Autentica com o Azure ML."""
    try:
        # Tenta usar DefaultAzureCredential (funciona em ambientes automatizados)
        credential = DefaultAzureCredential()
        credential.get_token("https://management.azure.com/.default")
    except Exception:
        # Fallback para autenticação interativa
        print("Autenticação padrão falhou, iniciando autenticação interativa...")
        credential = InteractiveBrowserCredential()
    
    # Conecta ao workspace do Azure ML
    try:
        ml_client = MLClient(
            credential=credential,
            subscription_id=None,  # Será obtido via CLI configurada
            resource_group_name=resource_group,
            workspace_name=workspace
        )
        print(f"Conectado ao workspace {workspace} no grupo de recursos {resource_group}")
        return ml_client
    except Exception as e:
        print(f"Erro ao conectar ao workspace: {e}")
        return None

def create_or_get_endpoint(ml_client, endpoint_name):
    """Cria um endpoint de inferência online ou obtém um existente."""
    try:
        # Tenta obter o endpoint existente
        endpoint = ml_client.online_endpoints.get(endpoint_name)
        print(f"Endpoint existente encontrado: {endpoint_name}")
    except Exception:
        # Cria um novo endpoint
        print(f"Criando novo endpoint: {endpoint_name}")
        endpoint = ManagedOnlineEndpoint(
            name=endpoint_name,
            description="Endpoint para previsão de vendas de sorvete",
            auth_mode="key"
        )
        ml_client.online_endpoints.begin_create_or_update(endpoint).result()
        print(f"Endpoint {endpoint_name} criado com sucesso")
    
    return endpoint

def register_model(ml_client, model_name, model_path, version=None):
    """Registra o modelo no Azure ML."""
    try:
        if version:
            # Verifica se o modelo com esta versão já existe
            try:
                existing_model = ml_client.models.get(model_name, version)
                print(f"Modelo {model_name}:{version} já existe, usando existente")
                return existing_model
            except Exception:
                pass
        
        # Registra o modelo
        model = Model(
            name=model_name,
            path=model_path,
            description="Modelo para prever vendas de sorvete baseado na temperatura",
            type="mlflow_model"  # Para modelos salvos no formato MLflow
        )
        
        registered_model = ml_client.models.create_or_update(model)
        print(f"Modelo registrado: {registered_model.name} (versão {registered_model.version})")
        return registered_model
    
    except Exception as e:
        print(f"Erro ao registrar modelo: {e}")
        return None

def create_deployment(ml_client, endpoint_name, deployment_name, model, instance_type="Standard_DS2_v2"):
    """Cria uma implantação do modelo no endpoint."""
    try:
        # Define a implantação
        deployment = ManagedOnlineDeployment(
            name=deployment_name,
            endpoint_name=endpoint_name,
            model=model.id,
            instance_type=instance_type,
            instance_count=1
        )
        
        # Cria ou atualiza a implantação
        ml_client.online_deployments.begin_create_or_update(deployment).result()
        print(f"Implantação {deployment_name} criada/atualizada com sucesso")
        
        # Atualiza o tráfego para o endpoint
        endpoint = ml_client.online_endpoints.get(endpoint_name)
        endpoint.traffic = {deployment_name: 100}
        ml_client.online_endpoints.begin_create_or_update(endpoint).result()
        print(f"Tráfego atualizado: 100% para {deployment_name}")
        
        return True
    except Exception as e:
        print(f"Erro ao criar implantação: {e}")
        return False

def get_endpoint_details(ml_client, endpoint_name):
    """Obtém detalhes do endpoint implantado."""
    try:
        # Obter endpoint
        endpoint = ml_client.online_endpoints.get(endpoint_name)
        
        # Obter chave de acesso
        keys = ml_client.online_endpoints.get_keys(endpoint_name)
        
        print("\n==== Detalhes do Endpoint ====")
        print(f"Nome: {endpoint_name}")
        print(f"URL de Pontuação: {endpoint.scoring_uri}")
        print(f"Chave Primária: {keys.primary_key}")
        
        print("\nExemplo de como invocar o endpoint:")
        print(f"curl -X POST {endpoint.scoring_uri} -H \"Authorization: Bearer {keys.primary_key}\" -H \"Content-Type: application/json\" -d @sample_input.json")
        
        print("\nOu usando o CLI do Azure ML:")
        print(f"az ml online-endpoint invoke --name {endpoint_name} --request-file sample_input.json")
        
        # Criar um arquivo de exemplo de entrada
        input_sample = {
            "input_data": {
                "columns": ["temperatura", "temperatura_squared"],
                "data": [
                    [25.0, 625.0],
                    [30.0, 900.0]
                ]
            }
        }
        
        import json
        with open("sample_input.json", "w") as f:
            json.dump(input_sample, f, indent=2)
        
        print("\nArquivo de exemplo 'sample_input.json' criado")
        
        return endpoint.scoring_uri, keys.primary_key
    except Exception as e:
        print(f"Erro ao obter detalhes do endpoint: {e}")
        return None, None

def test_model(endpoint_url, endpoint_key):
    """Testa o modelo implantado com alguns dados."""
    try:
        import requests
        
        # Dados de teste
        test_data = {
            "input_data": {
                "columns": ["temperatura", "temperatura_squared"],
                "data": [
                    [25.0, 625.0],
                    [30.0, 900.0],
                    [35.0, 1225.0]
                ]
            }
        }
        
        # Headers da requisição
        headers = {
            "Authorization": f"Bearer {endpoint_key}",
            "Content-Type": "application/json"
        }
        
        # Fazer a requisição
        print("\nTestando o modelo com dados de exemplo...")
        response = requests.post(endpoint_url, json=test_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("\nResultado da previsão:")
            predictions = result["result"] if "result" in result else result
            
            for i, temp in enumerate([25.0, 30.0, 35.0]):
                print(f"Temperatura: {temp}°C → Vendas previstas: {predictions[i]:.0f} unidades")
            
            return True
        else:
            print(f"Erro na requisição: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Erro ao testar o modelo: {e}")
        return False

def create_train_model_if_needed(ml_client, compute_name="cpu-cluster"):
    """Verifica se existe um modelo treinado ou cria um job de treinamento."""
    try:
        # Verificar se existe um modelo
        try:
            models = list(ml_client.models.list(name="sorvete-vendas-model"))
            if models:
                print(f"Modelo existente encontrado: {models[0].name} (versão {models[0].version})")
                return models[0]
        except Exception:
            print("Nenhum modelo existente encontrado")
        
        # Verificar se o cluster de computação existe
        try:
            compute = ml_client.compute.get(compute_name)
            print(f"Usando cluster de computação existente: {compute_name}")
        except Exception:
            print(f"Criando cluster de computação: {compute_name}")
            from azure.ai.ml.entities import AmlCompute
            compute = AmlCompute(
                name=compute_name,
                size="Standard_DS3_v2",
                min_instances=0,
                max_instances=2,
                idle_time_before_scale_down=120
            )
            ml_client.compute.begin_create_or_update(compute).result()
        
        # Verificar/criar o dataset
        try:
            datasets = list(ml_client.data.list(name="sorvetes-dataset"))
            if not datasets:
                # Gerar dados de exemplo
                print("Gerando dataset de exemplo...")
                np.random.seed(42)
                dates = pd.date_range(start="2023-01-01", periods=100)
                temperatures = 25 + 5 * np.sin(np.arange(100)/30*np.pi) + np.random.normal(0, 2, 100)
                temperatures = np.clip(temperatures, 15, 38)
                sales = 100 + 10 * (temperatures - 20) + np.random.normal(0, 15, 100)
                sales = np.clip(sales, 10, None).astype(int)
                
                df = pd.DataFrame({
                    "data": dates.strftime("%Y-%m-%d"),
                    "temperatura": temperatures,
                    "vendas": sales
                })
                
                df.to_csv("sorvete_ml.csv", index=False)
                
                # Registrar o dataset
                from azure.ai.ml.entities import Data
                from azure.ai.ml.constants import AssetTypes
                
                data_asset = Data(
                    path="sorvete_ml.csv",
                    type=AssetTypes.URI_FILE,
                    description="Dados de vendas de sorvete baseados na temperatura",
                    name="sorvetes-dataset"
                )
                ml_client.data.create_or_update(data_asset)
                print("Dataset criado e registrado")
            else:
                print(f"Dataset existente encontrado: {datasets[0].name}")
        except Exception as e:
            print(f"Erro ao verificar/criar dataset: {e}")
            return None
        
        # Criar e executar o job de pipeline
        print("Criando job de pipeline para treinamento...")
        
        # Aqui você precisaria criar um job para o Azure ML, que é mais complexo
        # do que podemos mostrar aqui. Para simplificar, vamos apenas criar um modelo localmente.
        print("Para fins de demonstração, criando um modelo simples localmente...")
        
        # Criar modelo simples
        from sklearn.linear_model import LinearRegression
        import joblib
        import mlflow.sklearn
        
        X = temperatures.reshape(-1, 1)
        y = sales
        model = LinearRegression().fit(X, y)
        
        # Salvar como MLflow
        os.makedirs("mlflow_model", exist_ok=True)
        mlflow.sklearn.save_model(model, "mlflow_model")
        
        # Registrar o modelo
        registered_model = register_model(ml_client, "sorvete-vendas-model", "mlflow_model")
        return registered_model
        
    except Exception as e:
        print(f"Erro ao verificar/criar modelo: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Script para implantar o modelo de previsão de vendas de sorvete")
    parser.add_argument("--resource-group", type=str, default="rg-dio-projeto-01", help="Nome do grupo de recursos")
    parser.add_argument("--workspace", type=str, default="ml-dio-projeto-01", help="Nome do workspace do Azure ML")
    parser.add_argument("--endpoint-name", type=str, default="sorveteria-endpoint", help="Nome do endpoint")
    parser.add_argument("--deployment-name", type=str, default="sorvete-deployment", help="Nome da implantação")
    parser.add_argument("--model-name", type=str, default="sorvete-vendas-model", help="Nome do modelo")
    parser.add_argument("--model-path", type=str, help="Caminho para o modelo (se já existir)")
    
    args = parser.parse_args()
    
    # Autenticar com o Azure ML
    ml_client = authenticate_azure_ml(args.resource_group, args.workspace)
    if not ml_client:
        print("Falha na autenticação com o Azure ML")
        return
    
    # Obter ou treinar modelo
    model = None
    if args.model_path:
        model = register_model(ml_client, args.model_name, args.model_path)
    else:
        model = create_train_model_if_needed(ml_client)
    
    if not model:
        print("Falha ao obter/criar modelo")
        return
    
    #