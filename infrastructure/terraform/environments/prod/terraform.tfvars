# infrastructure/terraform/environments/prod/terraform.tfvars
environment              = "prod"
db_allocated_storage     = 100
db_instance_class        = "db.t3.medium"
db_password              = "your-prod-db-password-here"
db_multi_az              = true
redis_node_type          = "cache.t3.medium"
redis_num_clusters       = 2
eks_worker_instance_type = "t3.medium"
eks_worker_desired_count = 3
eks_worker_min_count     = 2
eks_worker_max_count     = 10