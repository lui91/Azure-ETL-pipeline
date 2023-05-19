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
