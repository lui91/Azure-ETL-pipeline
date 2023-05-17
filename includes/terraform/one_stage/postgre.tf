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
  name      = var.POSTGRE_DB
  server_id = azurerm_postgresql_flexible_server.terra_posgre_server.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}
