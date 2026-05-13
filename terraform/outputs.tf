output "shared_file_path" {
  value       = local_file.deployment_info.filename
  description = "Path of the shared environment file"
}