# Tutorial: Implementando o Modelo de Previsão no Google Sheets

Este tutorial guiará você passo a passo na implementação de um modelo de regressão linear para prever vendas de sorvete com base na temperatura, usando apenas o Google Sheets.

## Pré-requisitos

- Uma conta Google para acessar o Google Sheets
- O arquivo CSV com os dados históricos de vendas e temperatura

## Passo 1: Preparar a Planilha

1. Acesse [Google Sheets](https://sheets.google.com) e crie uma nova planilha
2. Renomeie a planilha para "Modelo de Previsão de Vendas"
3. Adicione cabeçalhos nas seguintes colunas:
   - Coluna A: "Date"
   - Coluna B: "Temperature (°C)"
   - Coluna C: "Sales (units)"
   - Coluna D: "Predicted Sales"
   - Coluna E: "Error"
   - Coluna F: "Error²"

## Passo 2: Importar os Dados

1. Clique em "File" > "Import"
2. Selecione "Upload" e carregue o arquivo CSV, ou cole os dados diretamente
3. Configure a importação para começar na célula A2 (abaixo dos cabeçalhos)
4. Verifique se os dados de data, temperatura e vendas estão corretamente importados

## Passo 3: Calcular os Parâmetros da Regressão

1. Em uma célula separada (por exemplo, H2), insira o rótulo "Regression Parameters"
2. Na célula H3, insira "LINEST Formula"
3. Na célula H4, insira a fórmula:
   ```
   =LINEST(C2:C101,B2:B101)
   ```
4. Isso retornará dois valores: Beta e Alfa (da esquerda para a direita)
5. Adicione rótulos nas células H5 e I5:
   - Célula H5: "Beta (coefficient)"
   - Célula I5: "Alpha (intercept)"
6. Nas células H6 e I6, extraia os valores:
   - Célula H6: `=INDEX(H4:I4,1,1)`
   - Célula I6: `=INDEX(H4:I4,1,2)`

## Passo 4: Calcular as Previsões

1. Na célula D2 (primeira linha de dados sob "Predicted Sales"), insira a fórmula:
   ```
   =$I$6+$H$6*B2
   ```
2. Arraste esta fórmula para baixo para todas as linhas com dados

## Passo 5: Calcular os Erros

1. Na célula E2 (sob "Error"), insira a fórmula:
   ```
   =C2-D2
   ```
2. Na célula F2 (sob "Error²"), insira a fórmula:
   ```
   =E2^2
   ```
3. Arraste ambas as fórmulas para baixo para todas as linhas com dados

## Passo 6: Avaliar o Modelo

1. Adicione um rótulo na célula H8: "Model Evaluation"
2. Adicione os seguintes rótulos e fórmulas:
   - Célula H9: "Sum of Squared Errors (SSE)"
   - Célula I9: `=SUM(F2:F101)`
   - Célula H10: "Mean Squared Error (MSE)"
   - Célula I10: `=AVERAGE(F2:F101)`
   - Célula H11: "Root Mean Squared Error (RMSE)"
   - Célula I11: `=SQRT(I10)`
   - Célula H12: "Mean Absolute Error (MAE)"
   - Célula I12: `=AVERAGE(ABS(E2:E101))`
   - Célula H13: "R-squared (R²)"
   - Célula I13: `=CORREL(B2:B101,C2:C101)^2`

## Passo 7: Criar o Gráfico de Dispersão

1. Selecione as colunas de Temperature e Sales (colunas B e C)
2. Clique em "Insert" > "Chart"
3. Na janela "Chart editor", selecione "Scatter chart"
4. Clique em "Customize" > "Series"
5. Procure a opção "Trendline" e ative-a
6. Marque as opções "Show equation" e "Show R²"
7. Configure os títulos:
   - Chart title: "Relationship Between Temperature and Ice Cream Sales"
   - Horizontal axis: "Temperature (°C)"
   - Vertical axis: "Sales (units)"

## Passo 8: Implementar Ferramenta de Previsão

1. Em uma nova seção da planilha (por exemplo, a partir da célula H15):
   - Célula H15: "Sales Prediction Tool"
   - Célula H16: "Enter Temperature (°C)"
   - Célula I16: [deixar vazia para entrada do usuário]
   - Célula H17: "Predicted Sales"
   - Célula I17: `=$I$6+$H$6*I16`

2. Formate a célula I17 para melhor visualização (negrito, cor de fundo, etc.)
