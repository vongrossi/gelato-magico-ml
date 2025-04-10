# Abordagem Local para Previsão de Vendas de Sorvete 📊🍦

## Visão Geral

Este diretório contém os recursos necessários para implementar um modelo simples de previsão de vendas de sorvete usando planilhas (Excel ou Google Sheets), como alternativa a soluções mais complexas de machine learning.

## Por que usar planilhas?

Embora o projeto principal utilize o Azure Machine Learning para previsões mais avançadas, a abordagem com planilhas oferece várias vantagens para pequenos negócios:

1. **Acessibilidade**: Não requer conhecimentos de programação ou ferramentas especializadas.
2. **Baixo custo**: Utiliza ferramentas que a maioria das empresas já possui.
3. **Simplicidade**: Fácil de entender, modificar e compartilhar.
4. **Velocidade de implementação**: Solução rápida quando não há tempo para desenvolver modelos complexos.
5. **Visualização integrada**: Criação de gráficos e dashboards sem ferramentas adicionais.

## Quando preferir esta abordagem?

A abordagem com planilhas é ideal quando:

- Você tem um conjunto de dados pequeno a médio (menos de 1000 registros)
- A relação entre suas variáveis é relativamente simples e linear
- Você precisa de uma solução rápida que não-técnicos possam utilizar
- Sua empresa não tem recursos para implementar soluções de ML mais complexas
- Você quer uma solução transparente onde cada cálculo pode ser verificado

## Recursos Disponíveis

- [Planilha Google Sheets com o modelo implementado](https://docs.google.com/spreadsheets/d/1D8aMCXt_ey43jGPT1zkiUouV8HiNT6u0diily--SG_w/edit?usp=sharing)
- `tutorial_excel.md` - Tutorial detalhado para implementação no Excel
- `tutorial_google_sheets.md` - Tutorial detalhado para implementação no Google Sheets

## O Modelo de Regressão Linear

Nossa análise resultou na seguinte equação para prever vendas:

**Vendas = -147.0151 + 10.8036 × Temperatura**

Esta equação nos diz que:
- Para cada aumento de 1°C na temperatura, esperamos um aumento de aproximadamente 10.8 unidades nas vendas
- O R² de nosso modelo é aproximadamente 0.89, indicando que 89% da variabilidade nas vendas pode ser explicada pela temperatura
