// ============================================================
// AI Risk Classifier — Infrastructure as Code
// Author: Louiza Boujida | TheGovernAI.io
// Domain: AI-300 Domain 1 — MLOps Infrastructure
// ============================================================

@description('Environment name: dev or prod')
@allowed(['dev', 'prod'])
param environment string = 'dev'

@description('Azure region for all resources')
param location string = 'canadacentral'

@description('Project name used for resource naming')
param projectName string = 'ai-risk-classifier'

// ── Variables ──────────────────────────────────────────────
var prefix = '${projectName}-${environment}'
var searchServiceName = 'search-${replace(prefix, '-', '')}${uniqueString(resourceGroup().id)}'

// ── Azure AI Search ────────────────────────────────────────
resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
  }
  tags: {
    project: projectName
    environment: environment
    owner: 'TheGovernAI'
  }
}

// ── Application Insights ───────────────────────────────────
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${prefix}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
  tags: {
    project: projectName
    environment: environment
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${prefix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
  tags: {
    project: projectName
    environment: environment
    owner: 'TheGovernAI'
  }
}

// ── Outputs ────────────────────────────────────────────────
output searchServiceName string = aiSearch.name
output searchServiceEndpoint string = 'https://${aiSearch.name}.search.windows.net'
output appInsightsName string = appInsights.name
output appInsightsConnectionString string = appInsights.properties.ConnectionString
