# Data factory configuration
resource "azurerm_data_factory" "terra_factory" {
  name                = "terra-tweet-factory"
  location            = azurerm_resource_group.terra_group.location
  resource_group_name = azurerm_resource_group.terra_group.name

  github_configuration {
    account_name    = "lui91"
    branch_name     = "dev_etl"
    git_url         = "https://github.com"
    repository_name = "airflow_ingestion"
    root_folder     = "/"
  }

  tags = {
    "environment" = "dev"
  }
}
