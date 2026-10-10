/**
 * TECHDIM - GCP Sovereign Landing Zone
 * Provisionamento determinístico de VPC isolada, Cloud NAT, IAP e KMS.
 */

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.20"
    }
  }
}

# 1. VPC Soberana (Sem criação automática de sub-redes)
resource "google_compute_network" "sovereign_vpc" {
  name                    = var.network_name
  auto_create_subnetworks = false
  routing_mode            = "GLOBAL"
  description             = "VPC Privada Corporativa TECHDIM - Zero Public IPs"
}

# 2. Sub-rede Privada Corporativa
resource "google_compute_subnetwork" "private_subnet" {
  name                     = "${var.network_name}-subnet-private"
  ip_cidr_range            = var.subnet_cidr
  region                   = var.region
  network                  = google_compute_network.sovereign_vpc.id
  private_ip_google_access = true

  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# 3. Cloud Router & Cloud NAT para saída à internet controlada
resource "google_compute_router" "nat_router" {
  name    = "${var.network_name}-router"
  region  = var.region
  network = google_compute_network.sovereign_vpc.id
}

resource "google_compute_router_nat" "sovereign_nat" {
  name                               = "${var.network_name}-nat"
  router                             = google_compute_router.nat_router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}

# 4. Regra de Firewall para permitir acesso administrativo via IAP (Identity-Aware Proxy)
resource "google_compute_firewall" "allow_iap" {
  name    = "${var.network_name}-allow-iap-ingress"
  network = google_compute_network.sovereign_vpc.id

  allow {
    protocol = "tcp"
    ports    = ["22", "3389"]
  }

  # Bloco CIDR oficial e exclusivo do Google Cloud IAP
  source_ranges = ["35.235.240.0/20"]
  description   = "Permite acesso SSH e RDP exclusivamente atraves do Google Identity-Aware Proxy"
}
