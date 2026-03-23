# infrastructure/terraform/environments/dev/terraform.tfvars
environment              = "dev"
db_allocated_storage     = 20
db_instance_class        = "db.t3.micro"
db_password              = "your-dev-db-password-here"
db_multi_az              = false
redis_node_type          = "cache.t3.micro"
redis_num_clusters       = 1
eks_worker_instance_type = "t3.small"
eks_worker_desired_count = 1
eks_worker_min_count     = 1
eks_worker_max_count     = 3