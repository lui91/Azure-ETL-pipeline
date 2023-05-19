variable "RESOURCE_GROUP" {
  type = string
}

variable "BLOB_STORAGE" {
  type = string
}

variable "FACTORY_NAME" {
  type = string
}

variable "POSTGRE_DB" {
  type = string
}

variable "POSTGRE_HOST" {
  type      = string
  sensitive = true
}

variable "POSTGRE_LOGIN" {
  type      = string
  sensitive = true
}

variable "POSTGRE_PASSWORD" {
  type      = string
  sensitive = true
}
