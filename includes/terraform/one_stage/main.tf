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

data "azuread_user" "terra_user" {
  user_principal_name = "luis.ramirezsolis@cinvestav.mx"
}

resource "azurerm_resource_group" "terra_group" {
  name     = var.RESOURCE_GROUP
  location = "East US"
}

resource "azurerm_storage_account" "terra_storage" {
  name                     = var.BLOB_STORAGE
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

resource "azurerm_role_assignment" "blob_contributor_role" {
  scope                = azurerm_storage_account.terra_storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = data.azuread_user.terra_user.object_id
}
