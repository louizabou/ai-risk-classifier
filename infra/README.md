# Infrastructure as Code — Bicep

## Resources Provisioned
- Azure AI Search (Basic)
- Log Analytics Workspace
- Application Insights

## Deploy

### Validate (dry run)
```bash
az deployment group validate \
  --resource-group <your-rg> \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json
```

### Deploy Dev
```bash
az deployment group create \
  --resource-group <your-rg> \
  --template-file infra/main.bicep \
  --parameters infra/parameters.dev.json \
  --name bicep-deploy-dev
```

### Validate Prod (dry run only)
```bash
az deployment group validate \
  --resource-group <your-rg> \
  --template-file infra/main.bicep \
  --parameters infra/parameters.prod.json \
  --name bicep-deploy-prod
```