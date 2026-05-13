variable "environment" {
  type        = string
  default     = "production"
  description = "Target deployment environment"
}

variable "app_name" {
  type        = string
  default     = "my-cloud-project"
  description = "Application Name"
}