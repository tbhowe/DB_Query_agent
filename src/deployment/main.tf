provider "azurerm" {
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id

  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_container_group" "example" {
  name                = "example-containergroup"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  os_type             = "Linux"

  container {
    name   = "example-container"
    image  = "yourdockerhubusername/yourimage:yourtag"
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 7860
      protocol = "TCP"
    }
  }

  ip_address {
    type              = "Public"
    dns_name_label    = "example-app"
    ports {
      protocol      = "TCP"
      port          = 7860
    }
  }
}
