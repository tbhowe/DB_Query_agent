variable "subscription_id" {
  description = "Azure Subscription ID"
}

variable "client_id" {
  description = "Azure Client ID"
}

variable "client_secret" {
  description = "Azure Client Secret"
}

variable "tenant_id" {
  description = "Azure Tenant ID"
}

variable "location" {
  description = "Location for all resources"
  default     = "UK South"
}

variable "openai_api_key" {
  description = "OpenAI API key"
}

variable "rds_host" {
  description = "RDS Host"
}

variable "rds_password" {
  description = "RDS Password"
}

variable "rds_database" {
  description = "RDS Database name"
}

variable "rds_port" {
  description = "RDS Port"
}

