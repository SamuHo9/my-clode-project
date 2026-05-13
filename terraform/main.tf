terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

resource "local_file" "deployment_info" {
  content  = "App: ${var.app_name}\nEnvironment: ${var.environment}\nStatus: Provisioned by Terraform"
  filename = "${path.module}/../ansible/shared_env.txt"
}