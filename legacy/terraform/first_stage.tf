terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

provider "azurerm" {
  features {

  }
}

# data "external" "postgre_info" {
#   program = [ "${path.module}/get_env.sh" ]
# }

variable "RESOURCE_GROUP" {
  type = string
}

variable "POSTGRE_HOST" {
  type      = string
  sensitive = true
}

variable "POSTGRE_DB" {
  type = string
}

variable "POSTGRE_LOGIN" {
  type      = string
  sensitive = true
}

variable "POSTGRE_PASSWORD" {
  type      = string
  sensitive = true
}


resource "azurerm_resource_group" "terra_group" {
  name     = var.RESOURCE_GROUP
  location = "East US"
}

resource "azurerm_storage_account" "terra_storage" {
  name                     = "terratweetsstorage"
  resource_group_name      = azurerm_resource_group.terra_group.name
  location                 = azurerm_resource_group.terra_group.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    "environment" = "dev"
  }
}

resource "azurerm_storage_container" "terra_blob" {
  name                  = "csvs"
  storage_account_name  = azurerm_storage_account.terra_storage.name
  container_access_type = "private"
}

# Postgre server configuration
# resource "azurerm_postgresql_server" "terra_posgre_server" {
#   name                = "terra-tweets-postgre"
#   location            = azurerm_resource_group.terra_group.location
#   resource_group_name = azurerm_resource_group.terra_group.name

#   administrator_login          = "terra_lui"
#   administrator_login_password = "H@Sh1CoR3!"

#   sku_name   = "B_Gen5_1"
#   version    = "11"
#   storage_mb = 32768

#   backup_retention_days        = 7
#   geo_redundant_backup_enabled = false
#   auto_grow_enabled            = false

#   public_network_access_enabled    = true
#   ssl_enforcement_enabled          = true
#   ssl_minimal_tls_version_enforced = "TLS1_2"

#   tags = {
#     "environment" = "dev"
#   }
# }

resource "azurerm_postgresql_flexible_server" "terra_posgre_server" {
  name                = "terra-tweets-postgre"
  location            = azurerm_resource_group.terra_group.location
  resource_group_name = azurerm_resource_group.terra_group.name

  administrator_login    = var.POSTGRE_LOGIN
  administrator_password = var.POSTGRE_PASSWORD

  sku_name                     = "B_Standard_B1ms"
  version                      = "11"
  storage_mb                   = 32768
  zone                         = 3
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  tags = {
    "environment" = "dev"
  }
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_rule" {
  name             = "allow_azure_services"
  server_id        = azurerm_postgresql_flexible_server.terra_posgre_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "local_rule" {
  name             = "allow_local_pc"
  server_id        = azurerm_postgresql_flexible_server.terra_posgre_server.id
  start_ip_address = "177.226.113.195"
  end_ip_address   = "177.226.113.195"
}

resource "azurerm_postgresql_flexible_server_database" "terra_posgre_db" {
  name = var.POSTGRE_DB
  # resource_group_name = azurerm_resource_group.terra_group.name
  # server_name         = azurerm_postgresql_flexible_server.terra_posgre_server.name
  server_id = azurerm_postgresql_flexible_server.terra_posgre_server.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

output "azurerm_resource_group-terra_group" {
  value       = azurerm_resource_group.terra_group.id
  description = "azurerm_resource_group.terra_group"
  sensitive   = false
}

output "azurerm_storage_account-terra_storage" {
  value       = azurerm_storage_account.terra_storage.id
  description = "azurerm_storage_account.terra_storage"
  sensitive   = false
}
