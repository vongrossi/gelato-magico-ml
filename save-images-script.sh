#!/bin/bash

# Criar diretório para imagens se não existir
mkdir -p data

# Mensagem de início
echo "Salvando imagens para o projeto Gelato Mágico..."

# Planilha approach (exemplo da imagem 1)
cat > data/planilha-approach.jpg << 'EOL'
# Este arquivo será substituído pela imagem real
# Salve o Screenshot do Excel/Google Sheets aqui
EOL
echo "✅ Placeholder para planilha-approach.jpg criado"

# Notebook approach (exemplo da imagem 2)
cat > data/notebook-approach.jpg << 'EOL'
# Este arquivo será substituído pela imagem real
# Salve o Screenshot do notebook Jupyter aqui
EOL
echo "✅ Placeholder para notebook-approach.jpg criado"

# Forecast example (gráfico de exemplo)
cat > data/forecast-example.jpg << 'EOL'
# Este arquivo será substituído pela imagem real
# Salve o gráfico de previsão aqui
EOL
echo "✅ Placeholder para forecast-example.jpg criado"

# Instruções
echo ""
echo "Instruções:"
echo "1. Substitua os arquivos placeholder na pasta 'data/' pelas imagens reais"
echo "2. Para o arquivo planilha-approach.jpg, use o screenshot da planilha (Imagem 1)"
echo "3. Para o arquivo notebook-approach.jpg, use o screenshot do notebook (Imagem 2)"
echo "4. Para o arquivo forecast-example.jpg, use um screenshot do gráfico de previsão"
echo ""
echo "Depois de salvar as imagens, atualize o README.md com o caminho correto para as imagens."
