# Configuração do GitHub Actions e Secrets para CI/CD

Este documento fornece instruções para configurar o GitHub Actions e as secrets necessárias para automatizar o pipeline de CI/CD do projeto Gelato Mágico.

## Pré-requisitos

- Uma conta no GitHub
- Uma conta na Azure com permissão para criar recursos
- Azure CLI instalado localmente para configuração inicial

## Estrutura de Pastas

Certifique-se de que seu repositório tenha a seguinte estrutura de pastas:

```
gelato-magico-ml/
├── .github/
│   └── workflows/
│       └── github-workflow.yml
├── infrastructure/
│   └── pipeline-completo.json
├── src/
│   └── ... (arquivos de código fonte)
├── data/
│   └── sorvetes.csv
└── ... (outros arquivos do projeto)
```

## Configuração do Service Principal no Azure

Para que o GitHub Actions possa interagir com a Azure, você precisa criar um Service Principal:

1. Faça login na Azure CLI:
   ```bash
   az login
   ```

2. Liste suas assinaturas e note o ID da assinatura que deseja usar:
   ```bash
   az account list --output table
   ```

3. Defina a assinatura ativa:
   ```bash
   az account set --subscription "<ID-da-sua-assinatura>"
   ```

4. Crie um Service Principal com permissão de Contributor:
   ```bash
   az ad sp create-for-rbac --name "sp-dio-sorvete-projeto" \
                            --role contributor \
                            --scopes /subscriptions/<ID-da-sua-assinatura> \
                            --sdk-auth
   ```

5. Copie a saída JSON completa. Ela será usada como um secret no GitHub.

## Configuração de Secrets no GitHub

1. No seu repositório GitHub, navegue até **Settings > Secrets and variables > Actions**.

2. Clique em **New repository secret** e adicione as seguintes secrets:

   a. **AZURE_CREDENTIALS**:
      - Nome: `AZURE_CREDENTIALS`
      - Valor: [Cole aqui o JSON completo do Service Principal criado anteriormente]

   b. (Opcional) **AZURE_SUBSCRIPTION_ID**:
      - Nome: `AZURE_SUBSCRIPTION_ID`
      - Valor: [ID da sua assinatura Azure]

## Personalizando o Workflow

O arquivo `github-workflow.yml` pode ser personalizado conforme suas necessidades:

1. Modificando o nome do grupo de recursos:
   ```yaml
   env:
     AZURE_RESOURCEGROUP_NAME: seu-resource-group-name
     AZURE_LOCATION: sua-regiao-preferida
   ```

2. Alterando o nome do workspace do Azure ML:
   ```yaml
   az ml job create --file pipeline_job.yml --web
   ```

## Execução Manual do Workflow

Você pode iniciar o workflow manualmente:

1. Navegue até a aba **Actions** do seu repositório
2. Selecione **Deploy Azure ML Infrastructure and Pipeline**
3. Clique em **Run workflow**
4. Selecione a branch (geralmente `main`)
5. Clique em **Run workflow**

## Monitorando a Execução

Após iniciar o workflow:

1. Aguarde a conclusão de todas as etapas
2. Verifique os logs para identificar problemas ou erros
3. Após a conclusão bem-sucedida, acesse o [Azure ML Studio](https://ml.azure.com) para ver:
   - O workspace criado
   - O dataset registrado
   - O experimento de AutoML
   - O pipeline de Machine Learning

## Resolução de Problemas

### Erro de Autenticação

Se ocorrer um erro "Unauthorized" ou problemas de autenticação:
- Verifique se o secret `AZURE_CREDENTIALS` foi configurado corretamente
- Certifique-se de que o Service Principal tem as permissões necessárias
- O Service Principal pode levar alguns minutos para propagar

### Falha na Criação de Recursos

Se a criação de recursos falhar:
- Verifique as cotas disponíveis na sua assinatura Azure
- Confirme se a região selecionada suporta todos os recursos necessários
- Verifique se os nomes dos recursos são únicos e válidos

### Problemas com o Pipeline de ML

Se o pipeline de ML falhar:
- Verifique se o Compute Cluster foi criado corretamente
- Examine os logs detalhados no Azure ML Studio
- Verifique se as dependências do ambiente Python estão disponíveis

## Próximos Passos Após Implantação

Após a implantação bem-sucedida:

1. **Registrar o Modelo Manualmente** (se não for feito automaticamente):
   ```bash
   az ml model create --name sorvete-vendas-model --version 1 \
                      --path runs:/<run-id>/outputs/model \
                      --type mlflow_model
   ```

2. **Criar um Endpoint**:
   ```bash
   az ml online-endpoint create --name sorvete-endpoint \
                               --resource-group rg-dio-projeto-01 \
                               --workspace-name ml-dio-projeto-01
   ```

3. **Implantar o Modelo**:
   ```bash
   az ml online-deployment create --name sorvete-deployment \
                                 --endpoint sorvete-endpoint \
                                 --model azureml:sorvete-vendas-model:1 \
                                 --instance-type Standard_DS2_v2 \
                                 --instance-count 1
   ```

4. **Testar o Endpoint**:
   ```bash
   az ml online-endpoint invoke --name sorvete-endpoint \
                               --request-file sample-request.json
   ```

## Protegendo Credenciais e Chaves

Para proteger credenciais e chaves de API:

1. **Nunca armazene credenciais diretamente no código**:
   - Use sempre GitHub Secrets
   - Não inclua credenciais em arquivos de configuração versionados

2. **Gerencie o acesso ao Azure Key Vault**:
   - Armazene credenciais sensíveis no Azure Key Vault
   - Configure políticas de acesso para restringir quem pode acessar essas credenciais

3. **Rotacione credenciais regularmente**:
   ```bash
   az ad sp credential reset --name "sp-dio-sorvete-projeto" --credential-description "Key-1"
   ```

4. **Monitore o uso de credenciais**:
   - Verifique regularmente os logs de atividade
   - Configure alertas para atividades suspeitas

---

Ao seguir estas instruções, você terá um pipeline de CI/CD completo e seguro para automatizar o treinamento, registro e implantação do seu modelo de previsão de vendas de sorvete.
