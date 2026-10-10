variable "project_id" {
  type        = string
  description = "ID do projeto no Google Cloud Platform"
  default     = "techdim-sovereign-prod"
}

variable "region" {
  type        = string
  description = "Região padrão para implantação dos recursos"
  default     = "southamerica-east1"
}

variable "network_name" {
  type        = string
  description = "Nome base da VPC soberana"
  default     = "techdim-sovereign-vpc"
}

variable "subnet_cidr" {
  type        = string
  description = "Faixa de endereçamento CIDR para a sub-rede privada"
  default     = "10.100.0.0/20"
}
