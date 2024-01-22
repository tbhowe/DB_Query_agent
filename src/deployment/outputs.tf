output "container_public_ip" {
  value = azurerm_container_group.example.ip_address
  description = "The public IP address of the container instance."
}
