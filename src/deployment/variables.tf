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

variable "OPENAI_API_KEY" {
  description = "OpenAI API key"
}

variable "RDS_HOST" {
  description = "RDS Host"
}

variable "RDS_PASSWORD" {
  description = "RDS Password"
}

variable "RDS_DATABASE" {
  description = "RDS Database name"
}

variable "RDS_PORT" {
  description = "RDS Port"
}

