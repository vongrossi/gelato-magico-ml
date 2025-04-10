# Tutorial: Implementando o Modelo de Previsão no Excel

Este tutorial mostra como criar um modelo de regressão linear para prever vendas de sorvete com base na temperatura usando o Microsoft Excel.

## Pré-requisitos

- Microsoft Excel (versão 2010 ou superior)
- O arquivo CSV com os dados históricos de vendas e temperatura

## Passo 1: Preparar a Planilha

1. Abra o Excel e crie uma nova planilha
2. Adicione cabeçalhos nas seguintes colunas:
   - Coluna A: "Data"
   - Coluna B: "Temperatura (°C)"
   - Coluna C: "Vendas (unidades)"
   - Coluna D: "Vendas Previstas"
   - Coluna E: "Erro"
   - Coluna F: "Erro²"

## Passo 2: Importar os Dados

1. Vá para a guia "Dados" > "Obter Dados" > "De Texto/CSV"
2. Selecione seu arquivo CSV e importe os dados
3. Configure para que os dados comecem na célula A2 (abaixo dos cabeçalhos)

## Passo 3: Calcular Regressão com Função SLOPE e INTERCEPT

1. Em uma célula separada (ex: H2), adicione o rótulo "Parâmetros da Regressão"
2. Na célula H3, adicione "Beta (coeficiente)"
3. Na célula I3, insira a fórmula: `=SLOPE(C2:C101,B2:B101)`
4. Na célula H4, adicione "Alfa (intercepto)"
5. Na célula I4, insira a fórmula: `=INTERCEPT(C2:C101,B2:B101)`

## Passo 4: Calcular as Previsões e Erros

1. Na célula D2, insira a fórmula: `=$I$4+$I$3*B2`
2. Na célula E2, insira a fórmula: `=C2-D2`
3. Na célula F2, insira a fórmula: `=E2^2`
4. Arraste todas as fórmulas para baixo

## Passo 5: Adicionar o Gráfico de Dispersão

1. Selecione os dados de Temperatura e Vendas (colunas B e C)
2. Vá para a guia "Inserir" > "Gráficos" > "Dispersão"
3. Clique com o botão direito nos pontos do gráfico e selecione "Adicionar Linha de Tendência"
4. Marque as opções "Exibir Equação no gráfico" e "Exibir valor de R-quadrado no gráfico"

## Passo 6: Usar o Solver para Otimização (Opcional)

1. Acesse o Solver (guia "Dados" > "Solver")
2. Defina a célula de destino como a soma dos erros quadrados
3. Selecione "Min" (minimizar)
4. Defina as células variáveis como os parâmetros alfa e beta
5. Clique em "Resolver"

## Passo 7: Criar Ferramenta de Previsão

1. Em uma área separada da planilha, crie uma ferramenta simples:
   - H10: "Ferramenta de Previsão de Vendas"
   - H11: "Digite a Temperatura (°C):"
   - I11: [célula vazia para entrada]
   - H12: "Vendas Previstas:"
   - I12: `=$I$4+$I$3*I11`

---

Para resultados mais precisos, considere usar o Solver do Excel para otimizar os parâmetros alfa e beta.
