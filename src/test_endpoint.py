#!/usr/bin/env python
# Script para testar o endpoint do modelo de vendas de sorvete

import json
import argparse
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

def get_auth_header(endpoint_key=None):
    """
    Obtém o cabeçalho de autenticação para o endpoint.
    Usa uma chave de API se fornecida, ou tenta autenticação via DefaultAzureCredential.
    """
    if endpoint_key:
        return {"Authorization": f"Bearer {endpoint_key}"}
    
    # Se nenhuma chave for fornecida, tentamos autenticação via identidade
    credential = DefaultAzureCredential()
    return {"Authorization": f"Bearer {credential.get_token('https://ml.azure.com/.default').token}"}

def test_endpoint(endpoint_url, endpoint_key=None, workspace_name=None, resource_group=None):
    """
    Testa o endpoint enviando dados de várias temperaturas e visualizando os resultados.
    """
    print("Testando o endpoint do modelo de vendas de sorvete...")
    
    # Criar uma série de temperaturas para teste
    temperatures = np.linspace(15, 38, 24)
    squared_temps = temperatures ** 2
    
    # Preparar os dados para a requisição
    input_data = {
        "input_data": {
            "columns": ["temperatura", "temperatura_squared"],
            "data": [[temp, temp_sq] for temp, temp_sq in zip(temperatures, squared_temps)]
        }
    }
    
    # Fazer a requisição ao endpoint
    headers = get_auth_header(endpoint_key)
    headers["Content-Type"] = "application/json"
    
    try:
        response = requests.post(endpoint_url, json=input_data, headers=headers)
        response.raise_for_status()  # Lança exceção para erros HTTP
        predictions = response.json()
        
        # Converter previsões em um array numpy
        if isinstance(predictions, dict) and "result" in predictions:
            # Formato comum nos endpoints do Azure ML
            predictions = predictions["result"]
        
        if isinstance(predictions, list):
            predictions = np.array(predictions)
        
        # Criar um DataFrame com os resultados
        results = pd.DataFrame({
            "temperatura": temperatures,
            "vendas_previstas": predictions
        })
        
        # Definir limiares para categorização
        low_threshold = np.percentile(predictions, 25)
        high_threshold = np.percentile(predictions, 75)
        
        # Adicionar categoria
        results["categoria"] = pd.cut(
            results["vendas_previstas"],
            bins=[0, low_threshold, high_threshold, float("inf")],
            labels=["Baixa", "Média", "Alta"]
        )
        
        # Mostrar resultados
        print("\nPrevisões de vendas para diferentes temperaturas:")
        for i, row in results.sample(5).iterrows():
            print(f"Temperatura: {row['temperatura']:.1f}°C → Vendas previstas: {row['vendas_previstas']:.0f} unidades ({row['categoria']})")
        
        # Visualizar os resultados
        plt.figure(figsize=(12, 6))
        colors = {"Baixa": "blue", "Média": "green", "Alta": "red"}
        
        for category, group in results.groupby("categoria"):
            plt.scatter(group["temperatura"], group["vendas_previstas"], color=colors[category], label=category, alpha=0.7)
        
        plt.title("Previsão de Vendas de Sorvete por Temperatura")
        plt.xlabel("Temperatura (°C)")
        plt.ylabel("Vendas Previstas (unidades)")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        # Salvar a figura
        plt.savefig("previsao_vendas.png")
        print(f"\nGráfico de previsões salvo como 'previsao_vendas.png'")
        
        # Exibir insights de negócio
        print("\n=== Insights de Negócio ===")
        print(f"1. Vendas baixas (abaixo de {low_threshold:.0f} unidades): Temperaturas abaixo de {results[results['categoria'] == 'Baixa']['temperatura'].max():.1f}°C")
        print(f"   → Recomendação: Implementar promoções especiais em dias com estas temperaturas")
        
        print(f"\n2. Vendas altas (acima de {high_threshold:.0f} unidades): Temperaturas acima de {results[results['categoria'] == 'Alta']['temperatura'].min():.1f}°C")
        print(f"   → Recomendação: Garantir estoque adicional e considerar staff extra")
        
        # Calcular aumento médio de vendas para cada 5°C
        temp_points = [20, 25]
        sales_at_points = results.set_index("temperatura").loc[temp_points, "vendas_previstas"].values
        sales_diff = sales_at_points[1] - sales_at_points[0]
        temp_diff = temp_points[1] - temp_points[0]
        sales_per_5c = sales_diff / temp_diff * 5
        
        print(f"\n3. Para cada aumento de 5°C na temperatura, estima-se um aumento de aproximadamente {sales_per_5c:.0f} unidades nas vendas")
        
        plt.show()
        
        return True
    
    except Exception as e:
        print(f"Erro ao testar o endpoint: {e}")
        return False

def get_endpoint_url(endpoint_name, workspace_name, resource_group):
    """
    Obtém a URL do endpoint a partir do nome do endpoint, workspace e grupo de recursos.
    """
    try:
        # Autenticar com a Azure
        credential = DefaultAzureCredential()
        
        # Inicializar cliente ML
        client = MLClient(
            credential=credential,
            subscription_id=None,  # Será obtido da configuração atual
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        
        # Obter detalhes do endpoint
        endpoint = client.online_endpoints.get(endpoint_name)
        return endpoint.scoring_uri
    
    except Exception as e:
        print(f"Erro ao obter URL do endpoint: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para testar o endpoint do modelo de vendas de sorvete")
    
    parser.add_argument("--endpoint-url", type=str, help="URL do endpoint de teste")
    parser.add_argument("--endpoint-key", type=str, help="Chave de API do endpoint (opcional)")
    parser.add_argument("--endpoint-name", type=str, help="Nome do endpoint no Azure ML")
    parser.add_argument("--workspace-name", type=str, help="Nome do workspace do Azure ML")
    parser.add_argument("--resource-group", type=str, help="Nome do grupo de recursos")
    
    args = parser.parse_args()
    
    # Obter URL do endpoint se não fornecida diretamente
    endpoint_url = args.endpoint_url
    if not endpoint_url and args.endpoint_name and args.workspace_name and args.resource_group:
        endpoint_url = get_endpoint_url(args.endpoint_name, args.workspace_name, args.resource_group)
    
    if not endpoint_url:
        print("Erro: É necessário fornecer a URL do endpoint diretamente ou informações para obtê-la.")
        parser.print_help()
        exit(1)
    
    # Testar o endpoint
    success = test_endpoint(
        endpoint_url=endpoint_url,
        endpoint_key=args.endpoint_key,
        workspace_name=args.workspace_name,
        resource_group=args.resource_group
    )
    
    if success:
        print("\nTeste do endpoint concluído com sucesso!")
    else:
        print("\nFalha no teste do endpoint. Verifique os erros acima.")
        exit(1)
