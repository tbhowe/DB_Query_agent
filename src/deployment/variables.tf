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
