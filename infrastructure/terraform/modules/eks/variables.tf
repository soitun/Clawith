variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "vpc_id" {
  description = "ID of the VPC to deploy the cluster in"
  type        = string
}

variable "private_subnets" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "public_subnets" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "cluster_sg_id" {
  description = "Security group ID for the cluster control plane"
  type        = string
}

variable "node_sg_id" {
  description = "Security group ID for the worker nodes"
  type        = string
}

variable "worker_instance_type" {
  description = "Instance type for EKS worker nodes"
  type        = string
  default     = "t3.medium"
}

variable "worker_desired_count" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "worker_min_count" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "worker_max_count" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 5
}