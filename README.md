# Projeto Gelato Mágico 🍦 - Previsão de Vendas com Machine Learning

<div align="center">
  <!-- <img src="img/logo.svg" alt="Logo Gelato Mágico" width="300"> -->
  <h1>Gelato Mágico 🍦</h1>
  <em>Transformando dados em sorvetes: Otimizando produção, reduzindo desperdícios e aumentando lucros</em>
</div>

## 📋 O que é este projeto?

O **Projeto Gelato Mágico** é uma solução que ajuda sorveterias a prever quantos sorvetes venderão em cada dia, baseando-se na temperatura prevista. Imagine ser dono de uma sorveteria e todo dia precisar decidir: "Quantos sorvetes devo produzir hoje?"

- Se você produzir **sorvetes demais**, o excesso estraga e você perde dinheiro.
- Se você produzir **sorvetes de menos**, os clientes vão embora sem comprar, e você perde vendas.

Este projeto usa inteligência artificial para analisar dados de vendas anteriores e temperaturas para fazer previsões precisas. Assim, você sempre produz a quantidade certa de sorvetes - nem demais, nem de menos!

## 🎯 Principais vantagens do projeto

- ✅ **Previsões precisas**: Saiba quantos sorvetes venderá com base na previsão do tempo
- ✅ **Menos desperdício**: Economize dinheiro reduzindo produtos não vendidos
- ✅ **Mais vendas**: Nunca perca uma venda por falta de estoque
- ✅ **Automatizado**: Uma vez configurado, funciona sozinho, sem intervenção constante
- ✅ **Adaptável**: Funciona para qualquer tamanho de sorveteria - do carrinho de sorvete à grande rede

## 🛣️ Três caminhos para usar o projeto

Oferecemos três abordagens diferentes, cada uma adaptada a um perfil específico de usuário:

### 1. Abordagem com planilhas - Para pequenos negócios

**Ideal para**: Pequenas sorveterias, carrinhos de sorvete, empreendedores iniciantes.

**Como funciona**: Uma planilha simples no [Google Sheets](https://docs.google.com/spreadsheets/d/1D8aMCXt_ey43jGPT1zkiUouV8HiNT6u0diily--SG_w/edit?usp=sharing) ou Excel onde você insere a temperatura prevista e recebe uma estimativa de vendas.

**Benefícios**:
- 🔧 Não exige conhecimentos técnicos
- 💰 Custo zero (planilha gratuita)
- 🚀 Implementação em minutos
- 📱 Acesso pelo celular ou computador

[**Acesse o Tutorial do Google Sheets →**](local/tutorial_google_sheets.md)  
[**Acesse o Tutorial do Excel →**](local/tutorial_excel.md)

### 2. Notebook com AutoML - Para analistas de dados

**Ideal para**: Analistas de dados, entusiastas de ciência de dados, empresas médias.

**Como funciona**: Um notebook Jupyter que usa Azure AutoML para testar automaticamente vários algoritmos e encontrar o melhor modelo de previsão.

**Benefícios**:
- 📊 Análise de dados visual e interativa
- 🧠 Experimentação com diferentes algoritmos
- 📈 Gráficos detalhados e métricas avançadas
- 🔄 Facilidade para refinar e adaptar o modelo

[**Ver Notebook com AutoML →**](src/Sorvete_AutoML.ipynb)

### 3. Pipeline completo na Azure - Para grandes empresas

**Ideal para**: Redes de sorveterias, empresas maiores, equipes de TI/dados.

**Como funciona**: Um sistema completo e automatizado na nuvem Azure que atualiza as previsões diariamente e pode se integrar a outros sistemas da empresa.

**Benefícios**:
- 🤖 Totalmente automatizado (set-it-and-forget-it)
- 🔄 Retreinamento automático com novos dados
- 🔌 Integração com sistemas existentes (ERP, BI)
- 🌐 Acessível de qualquer lugar via API
- 🛡️ Segurança e escalabilidade empresarial

[**Ver Detalhes da Infraestrutura →**](infrastructure/pipeline-completo.json)  
[**Instruções para Implantação →**](INSTRUCOES-GITHUB.md)

## 📊 Como funciona a previsão?

Em termos simples, o sistema funciona assim:

1. **Coleta dados históricos**: Quanto vendemos em dias anteriores e qual era a temperatura
2. **Encontra padrões**: Descobre como a temperatura afeta as vendas (por exemplo: cada 5°C a mais = 30 sorvetes a mais)
3. **Faz previsões**: Com base na temperatura prevista para amanhã, calcula quantos sorvetes provavelmente venderá
4. **Gera recomendações**: Sugere quanto produzir e outras estratégias (como promoções em dias frios)

## 💡 Insights valiosos descobertos

Analisando os dados, descobrimos padrões importantes que podem ajudar no negócio:

| Faixa de Temperatura | Padrão de Vendas | Recomendação Estratégica |
|----------------------|------------------|--------------------------|
| Abaixo de 25°C | Vendas 40% abaixo da média | Implementar promoção "Compre 1, Leve 2" |
| Entre 25-30°C | Vendas na média | Produção normal |
| Acima de 30°C | Vendas 60% acima da média | Aumentar produção e equipe |

**Impacto financeiro estimado**:
- Redução de 30% no desperdício = Economia de R$ 1.500/mês
- Aumento de 25% nas vendas em dias frios = + R$ 2.000/mês
- Aumento de 15% nas vendas em dias quentes = + R$ 3.000/mês

## 🚀 Como começar a usar

### Para iniciantes (abordagem com planilhas):

1. Clique [neste link](https://docs.google.com/spreadsheets/d/1D8aMCXt_ey43jGPT1zkiUouV8HiNT6u0diily--SG_w/edit?usp=sharing) para acessar a planilha
2. Faça uma cópia para sua conta Google (Arquivo > Fazer uma cópia)
3. Insira a temperatura prevista e veja a estimativa de vendas instantaneamente!

### Para analistas de dados (notebook com AutoML):

1. Clone este repositório: `git clone https://github.com/vongrossi/gelato-magico-ml.git`
2. Instale as dependências: `pip install -r src/requirements.txt`
3. Abra o notebook: `jupyter notebook src/Sorvete_AutoML.ipynb`
4. Siga as instruções no notebook para treinar e avaliar o modelo

### Para implementação empresarial (pipeline na Azure):

1. Clone este repositório
2. Siga as instruções detalhadas em [INSTRUCOES-GITHUB.md](INSTRUCOES-GITHUB.md)
3. Execute o script de implantação: `python src/deploy_model.py`
4. Teste o endpoint: `python src/test_endpoint.py`

## 🧠 Entendendo os termos técnicos

Para quem não está familiarizado com tecnologia, aqui estão explicações simples dos termos usados:

- **Machine Learning**: É como ensinar um computador a reconhecer padrões nos dados e fazer previsões, assim como ensinamos uma criança a reconhecer animais mostrando fotos repetidamente.

- **Azure**: É a plataforma de nuvem (servidores online) da Microsoft, onde o modelo é hospedado e executado.

- **Pipeline**: É como uma linha de produção automatizada, onde os dados passam por várias etapas (limpeza, análise, treinamento) sem intervenção manual.

- **AutoML (Machine Learning Automatizado)**: É como ter um cientista de dados robô que testa dezenas de abordagens diferentes e escolhe a melhor.

- **Endpoint**: É como um balcão de atendimento virtual onde você pode enviar perguntas (qual será a venda com temperatura X?) e receber respostas.

## 📂 O que tem neste repositório?

```
.
├── data/                  # Dados de exemplo de vendas e temperaturas
├── infrastructure/        # Arquivos para criar a infraestrutura na Azure
├── local/                 # Abordagem simplificada com planilhas
├── src/                   # Códigos fonte e notebooks
├── INSTRUCOES-GITHUB.md   # Guia para implementação com GitHub Actions
└── README.md              # Este documento que você está lendo
```

## 🤔 Perguntas frequentes

### Precisamos ser especialistas em tecnologia para usar?
Não! A abordagem com planilhas foi criada justamente para pequenos negócios sem conhecimento técnico.

### Funciona para outros produtos além de sorvete?
Sim! A mesma técnica pode ser adaptada para qualquer produto sensível à temperatura, como bebidas geladas, picolés, sorvetes, açaí, etc.

### Como começar com investimento mínimo?
Comece pela abordagem com planilhas, que é gratuita e simples. Conforme seu negócio crescer, você pode evoluir para as abordagens mais avançadas.

### E se meu negócio for afetado por outros fatores além da temperatura?
O modelo pode ser expandido para incluir outros fatores como dia da semana, feriados, eventos locais, etc. Isso é mais facilmente implementado nas abordagens de notebook e pipeline.

## 📞 Precisa de ajuda?

Se você encontrar dificuldades ou tiver dúvidas:

1. Consulte a documentação específica de cada abordagem:
   - [Tutorial para Google Sheets](local/tutorial_google_sheets.md)
   - [Tutorial para Excel](local/tutorial_excel.md)
   - [Notebook com AutoML](src/Sorvete_AutoML.ipynb)
   - [Implementação na Azure](INSTRUCOES-GITHUB.md)

2. Abra uma "Issue" neste repositório com sua dúvida

3. Entre em contato com a comunidade da DIO para suporte adicional

## 🤝 Contribuindo para o projeto

Adoraríamos ter sua ajuda para melhorar este projeto! Algumas formas de contribuir:

1. Reportar bugs ou sugerir melhorias abrindo issues
2. Enviar correções ou novos recursos através de pull requests
3. Melhorar a documentação
4. Compartilhar sua experiência usando o projeto

Para contribuir com código, siga o processo padrão:
1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  Desenvolvido como projeto para o desafio de Machine Learning da DIO.<br>
  <strong>Transforme dados em resultados para o seu negócio!</strong>
</div>
