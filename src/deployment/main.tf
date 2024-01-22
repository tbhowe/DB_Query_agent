provider "azurerm" {
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id

  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = var.location
}

resource "azurerm_container_group" "example" {
  name                = "example-container-group"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  os_type             = "Linux"
  ip_address_type     = "Public"
  dns_name_label      = "example-container-group-dns"

  container {
    name   = "gradio-app"
    image  = "your_dockerhub_username/your_image_name:your_tag"
    cpu    = 0.5
    memory = 1.5

    ports {
      port     = 7860
      protocol = "TCP"
    }

    environment_variables = {
      "OpenAI_API_Key" = azurerm_key_vault_secret.openai_api_key.value
      "RDS_HOST"       = azurerm_key_vault_secret.rds_host.value
      "RDS_PASSWORD"   = azurerm_key_vault_secret.rds_password.value
      "RDS_DATABASE"   = azurerm_key_vault_secret.rds_database.value
      "RDS_PORT"       = azurerm_key_vault_secret.rds_port.value
    }
  }

  identity {
    type = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.example.id]
  }
}


resource "azurerm_key_vault" "example" {
  name                        = "example-key-vault"
  location                    = azurerm_resource_group.example.location
  resource_group_name         = azurerm_resource_group.example.name
  tenant_id                   = var.tenant_id
  sku_name                    = "standard"
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
}

resource "azurerm_key_vault_secret" "openai_api_key" {
  name         = "OpenAI-API-Key"
  value        = var.OPENAI_API_KEY
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "rds_host" {
  name         = "RDS-HOST"
  value        = var.RDS_HOST
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "rds_password" {
  name         = "RDS-PASSWORD"
  value        = var.RDS_PASSWORD
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "rds_database" {
  name         = "RDSDATABASE"
  value        = var.RDS_DATABASE
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_key_vault_secret" "rds_port" {
  name         = "RDS_PORT"
  value        = var.RDS_PORT
  key_vault_id = azurerm_key_vault.example.id
}

resource "azurerm_user_assigned_identity" "example" {
  name                = "example-user-assigned-identity"
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
}

resource "azurerm_key_vault_access_policy" "example" {
  key_vault_id = azurerm_key_vault.example.id

  tenant_id = var.tenant_id
  object_id = azurerm_user_assigned_identity.example.principal_id

  key_permissions    = []
  secret_permissions = ["get"]
  certificate_permissions = []
}
