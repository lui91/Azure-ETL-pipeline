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

resource "azurerm_resource_group" "terra_group" {
  name     = "terra-tweets-group"
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

  administrator_login    = "terra_lui"
  administrator_password = "H@Sh1CoR3!"

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

resource "azurerm_postgresql_flexible_server_firewall_rule" "net_rule" {
  name             = "allow_azure_services"
  server_id        = azurerm_postgresql_flexible_server.terra_posgre_server.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

resource "azurerm_postgresql_flexible_server_database" "terra_posgre_db" {
  name = "disaster_data"
  # resource_group_name = azurerm_resource_group.terra_group.name
  # server_name         = azurerm_postgresql_flexible_server.terra_posgre_server.name
  server_id = azurerm_postgresql_flexible_server.terra_posgre_server.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

# Data factory configuration
resource "azurerm_data_factory" "terra-factory" {
  name                = "terra-tweet-factory"
  location            = azurerm_resource_group.terra_group.location
  resource_group_name = azurerm_resource_group.terra_group.name

  # github_configuration {
  #   account_name    = "lui91"
  #   branch_name     = "data_processing"
  #   git_url         = "https://github.com"
  #   repository_name = "airflow_ingestion"
  #   root_folder     = "/"
  # }

  tags = {
    "environment" = "dev"
  }
}

# resource "azurerm_data_factory_integration_runtime_azure" "integration_service" {
#   name            = "factoryIntegrationService"
#   data_factory_id = azurerm_data_factory.terra-factory.id
#   location        = azurerm_resource_group.terra_group.location
# }

resource "azurerm_data_factory_linked_service_azure_blob_storage" "blob_linked_service" {
  name            = "csvsLinkedService"
  data_factory_id = azurerm_data_factory.terra-factory.id
  # integration_runtime_name = azurerm_data_factory_integration_runtime_azure.integration_service.name
  connection_string = azurerm_storage_account.terra_storage.primary_connection_string
}

#TODO: Replace sensitive information with docker env
resource "azurerm_data_factory_linked_service_postgresql" "postgre_linked_service" {
  name              = "postgreLinkedService"
  data_factory_id   = azurerm_data_factory.terra-factory.id
  connection_string = "host=postgres-tweets.postgres.database.azure.com;port=5432;dbname=disaster_data;user=lui91 password=8Y4mhbaemXnJgzm6 sslmode=require"
}

# csvs datasets
resource "azurerm_data_factory_dataset_azure_blob" "messages_source_data" {
  name                = "messages_dataset"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_azure_blob_storage.blob_linked_service.name

  path     = "csvs"
  filename = "messages.csv"
}

resource "azurerm_data_factory_dataset_azure_blob" "categories_source_data" {
  name                = "categories_dataset"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_azure_blob_storage.blob_linked_service.name

  path     = "csvs"
  filename = "categories.csv"
}

# postgre tables
resource "azurerm_data_factory_dataset_postgresql" "date_dim" {
  name                = "date_dim"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_postgresql.postgre_linked_service.name

  table_name = "public.date_dim"
}

resource "azurerm_data_factory_dataset_postgresql" "provider_dim" {
  name                = "provider_dim"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_postgresql.postgre_linked_service.name

  table_name = "public.provider_dim"
}

resource "azurerm_data_factory_dataset_postgresql" "tweets_dim" {
  name                = "tweets_dim"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_postgresql.postgre_linked_service.name

  table_name = "public.tweets_dim"
}

resource "azurerm_data_factory_dataset_postgresql" "tweets_fact" {
  name                = "tweets_fact"
  data_factory_id     = azurerm_data_factory.terra-factory.id
  linked_service_name = azurerm_data_factory_linked_service_postgresql.postgre_linked_service.name

  table_name = "public.tweets_fact"
}

resource "azurerm_data_factory_data_flow" "csv_transformations" {
  name            = "csv_transformations"
  data_factory_id = azurerm_data_factory.terra-factory.id

  source {
    name = "Messages"
    dataset {
      name = azurerm_data_factory_dataset_azure_blob.messages_source_data.name
    }
  }

  source {
    name = "Categories"
    dataset {
      name = azurerm_data_factory_dataset_azure_blob.categories_source_data.name
    }
  }

  sink {
    name = "postgreSink"
    dataset {
      name = azurerm_data_factory_dataset_postgresql.tweets_fact.name
    }
  }

  transformation {
    name = "ModifyColumns1"
  }

  transformation {
    name = "join1"
  }

  transformation {
    name = "select1"
  }

  transformation {
    name = "CategoriesColumnCreation"
  }

  transformation {
    name = "ModifyColumns2"
  }

  transformation {
    name = "select2"
  }

  transformation {
    name = "derivedColumn1"
  }

  script = <<EOT
      "parameters{",
      "     var_date_key as string (\"Var date key\"),",
      "     var_tweet_key as string (\"Var tweet key\"),",
      "     var_provider_key as string (\"Var provider key\")",
      "}",
      "source(output(",
      "          id as integer,",
      "          message as string,",
      "          original as string,",
      "          genre as string",
      "     ),",
      "     allowSchemaDrift: true,",
      "     validateSchema: false,",
      "     ignoreNoFilesFound: false) ~> Messages",
      "source(output(",
      "          id as string,",
      "          categories as string",
      "     ),",
      "     allowSchemaDrift: true,",
      "     validateSchema: false,",
      "     ignoreNoFilesFound: false) ~> Categories",
      "Categories derive(id = toInteger(id)) ~> ModifyColumns1",
      "Messages, ModifyColumns1 join(Messages@id == ModifyColumns1@id,",
      "     joinType:'right',",
      "     matchType:'exact',",
      "     ignoreSpaces: false,",
      "     broadcast: 'auto')~> join1",
      "join1 select(mapColumn(",
      "          id = Messages@id,",
      "          message,",
      "          original,",
      "          genre,",
      "          categories",
      "     ),",
      "     skipDuplicateMapInputs: false,",
      "     skipDuplicateMapOutputs: false) ~> select1",
      "select1 parse(categories_separated = categories ? (related as string,",
      "          request as string,",
      "          offer as string,",
      "          aid_related as string,",
      "          medical_help as string,",
      "          medical_products as string,",
      "          search_and_rescue as string,",
      "          security as string,",
      "          military as string,",
      "          child_alone as string,",
      "          water as string,",
      "          food as string,",
      "          shelter as string,",
      "          clothing as string,",
      "          money as string,",
      "          missing_people as string,",
      "          refugees as string,",
      "          death as string,",
      "          other_aid as string,",
      "          infrastructure_related as string,",
      "          transport as string,",
      "          buildings as string,",
      "          electricity as string,",
      "          tools as string,",
      "          hospitals as string,",
      "          shops as string,",
      "          aid_centers as string,",
      "          other_infrastructure as string,",
      "          weather_related as string,",
      "          floods as string,",
      "          storm as string,",
      "          fire as string,",
      "          earthquake as string,",
      "          cold as string,",
      "          other_weather as string,",
      "          direct_report as string),",
      "     format: 'delimited',",
      "     columnNamesAsHeader: false,",
      "     columnDelimiter: ';',",
      "     nullValue: '0') ~> parse1",
      "parse1 derive(related = split(categories_separated.related, '-')[2],",
      "          request = split(categories_separated.request, '-')[2],",
      "          offer = split(categories_separated.offer, '-')[2],",
      "          aid_related = split(categories_separated.aid_related, '-')[2],",
      "          medical_help = split(categories_separated.medical_help, '-')[2],",
      "          medical_products = split(categories_separated.medical_products, '-')[2],",
      "          search_and_rescue = split(categories_separated.search_and_rescue, '-')[2],",
      "          security = split(categories_separated.security, '-')[2],",
      "          military = split(categories_separated.military, '-')[2],",
      "          child_alone = split(categories_separated.child_alone, '-')[2],",
      "          water = split(categories_separated.water, '-')[2],",
      "          food = split(categories_separated.food, '-')[2],",
      "          shelter = split(categories_separated.shelter, '-')[2],",
      "          clothing = split(categories_separated.clothing, '-')[2],",
      "          money = split(categories_separated.money, '-')[2],",
      "          missing_people = split(categories_separated.missing_people, '-')[2],",
      "          refugees = split(categories_separated.refugees, '-')[2],",
      "          death = split(categories_separated.death, '-')[2],",
      "          other_aid = split(categories_separated.other_aid, '-')[2],",
      "          infrastructure_related = split(categories_separated.infrastructure_related, '-')[2],",
      "          transport = split(categories_separated.transport, '-')[2],",
      "          buildings = split(categories_separated.buildings, '-')[2],",
      "          electricity = split(categories_separated.electricity, '-')[2],",
      "          tools = split(categories_separated.tools, '-')[2],",
      "          hospitals = split(categories_separated.hospitals, '-')[2],",
      "          shops = split(categories_separated.shops, '-')[2],",
      "          aid_centers = split(categories_separated.aid_centers, '-')[2],",
      "          other_infrastructure = split(categories_separated.other_infrastructure, '-')[2],",
      "          weather_related = split(categories_separated.weather_related, '-')[2],",
      "          floods = split(categories_separated.floods, '-')[2],",
      "          storm = split(categories_separated.storm, '-')[2],",
      "          fire = split(categories_separated.fire, '-')[2],",
      "          earthquake = split(categories_separated.earthquake, '-')[2],",
      "          cold = split(categories_separated.cold, '-')[2],",
      "          other_weather = split(categories_separated.other_weather, '-')[2],",
      "          direct_report = split(categories_separated.direct_report, '-')[2]) ~> CategoriesColumnCreation",
      "select2 derive(related = toInteger(related),",
      "          request = toInteger(request),",
      "          offer = toInteger(offer),",
      "          aid_related = toInteger(aid_related),",
      "          medical_help = toInteger(medical_help),",
      "          medical_products = toInteger(medical_products),",
      "          search_and_rescue = toInteger(search_and_rescue),",
      "          security = toInteger(security),",
      "          military = toInteger(military),",
      "          child_alone = toInteger(child_alone),",
      "          water = toInteger(water),",
      "          food = toInteger(food),",
      "          shelter = toInteger(shelter),",
      "          clothing = toInteger(clothing),",
      "          money = toInteger(money),",
      "          missing_people = toInteger(missing_people),",
      "          refugees = toInteger(refugees),",
      "          death = toInteger(death),",
      "          other_aid = toInteger(other_aid),",
      "          infrastructure_related = toInteger(infrastructure_related),",
      "          transport = toInteger(transport),",
      "          buildings = toInteger(buildings),",
      "          electricity = toInteger(electricity),",
      "          tools = toInteger(tools),",
      "          hospitals = toInteger(hospitals),",
      "          shops = toInteger(shops),",
      "          aid_centers = toInteger(aid_centers),",
      "          other_infrastructure = toInteger(other_infrastructure),",
      "          weather_related = toInteger(weather_related),",
      "          floods = toInteger(floods),",
      "          storm = toInteger(storm),",
      "          fire = toInteger(fire),",
      "          earthquake = toInteger(earthquake),",
      "          cold = toInteger(cold),",
      "          other_weather = toInteger(other_weather),",
      "          direct_report = toInteger(direct_report)) ~> ModifyColumns2",
      "CategoriesColumnCreation select(mapColumn(",
      "          id,",
      "          message,",
      "          original,",
      "          genre,",
      "          related,",
      "          request,",
      "          offer,",
      "          aid_related,",
      "          medical_help,",
      "          medical_products,",
      "          search_and_rescue,",
      "          security,",
      "          military,",
      "          child_alone,",
      "          water,",
      "          food,",
      "          shelter,",
      "          clothing,",
      "          money,",
      "          missing_people,",
      "          refugees,",
      "          death,",
      "          other_aid,",
      "          infrastructure_related,",
      "          transport,",
      "          buildings,",
      "          electricity,",
      "          tools,",
      "          hospitals,",
      "          shops,",
      "          aid_centers,",
      "          other_infrastructure,",
      "          weather_related,",
      "          floods,",
      "          storm,",
      "          fire,",
      "          earthquake,",
      "          cold,",
      "          other_weather,",
      "          direct_report",
      "     ),",
      "     skipDuplicateMapInputs: true,",
      "     skipDuplicateMapOutputs: true) ~> select2",
      "ModifyColumns2 derive(tweet_key = $var_tweet_key,",
      "          date_key = $var_date_key,",
      "          provider_key = $var_provider_key) ~> derivedColumn1",
      "derivedColumn1 sink(allowSchemaDrift: true,",
      "     validateSchema: true,",
      "     input(",
      "          tweet_key as integer,",
      "          date_key as integer,",
      "          provider_key as integer,",
      "          id as integer,",
      "          message as string,",
      "          original as string,",
      "          genre as string,",
      "          related as integer,",
      "          request as integer,",
      "          offer as integer,",
      "          aid_related as integer,",
      "          medical_help as integer,",
      "          medical_products as integer,",
      "          search_and_rescue as integer,",
      "          security as integer,",
      "          military as integer,",
      "          child_alone as integer,",
      "          water as integer,",
      "          food as integer,",
      "          shelter as integer,",
      "          clothing as integer,",
      "          money as integer,",
      "          missing_people as integer,",
      "          refugees as integer,",
      "          death as integer,",
      "          other_aid as integer,",
      "          infrastructure_related as integer,",
      "          transport as integer,",
      "          buildings as integer,",
      "          electricity as integer,",
      "          tools as integer,",
      "          hospitals as integer,",
      "          shops as integer,",
      "          aid_centers as integer,",
      "          other_infrastructure as integer,",
      "          weather_related as integer,",
      "          floods as integer,",
      "          storm as integer,",
      "          fire as integer,",
      "          earthquake as integer,",
      "          cold as integer,",
      "          other_weather as integer",
      "     ),",
      "     deletable:false,",
      "     insertable:true,",
      "     updateable:false,",
      "     upsertable:false,",
      "     format: 'table',",
      "     skipDuplicateMapInputs: true,",
      "     skipDuplicateMapOutputs: true) ~> postgreSink"
  EOT
}


resource "azurerm_data_factory_pipeline" "tweets_etl" {
  name            = "tweets_etl"
  data_factory_id = azurerm_data_factory.terra-factory.id

  variables = {
    "pipe_date_key"     = "\"pipeline key\"",
    "pipe_tweet_key"    = "\"pipeline tweet\"",
    "pipe_provider_key" = "\"pipeline provider\""
  }
  # activities_json = <<JSON
  # [
  #   {
  #     "name": "Lookup_date",
  #     "type": "Lookup",
  #     "dependsOn": [],
  #   }
  # ]

}



# resource "azurerm_container_registry" "terra_container_registry" {
#   name                          = "terraContainerReg"
#   resource_group_name           = azurerm_resource_group.terra_group.name
#   location                      = azurerm_resource_group.terra_group.location
#   sku                           = "Standard"
#   public_network_access_enabled = true

#   tags = {
#     "environment" = "dev"
#   }
# }

# resource "azurerm_key_vault" "name" {

# }

# resource "azurerm_machine_learning_workspace" "name" {
#   name                = "terra-ml-workspace"
#   location            = azurerm_resource_group.terra_group.location
#   resource_group_name = azurerm_resource_group.terra_group.name
# }
