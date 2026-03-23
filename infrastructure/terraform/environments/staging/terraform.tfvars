# infrastructure/terraform/environments/staging/terraform.tfvars
environment              = "staging"
db_allocated_storage     = 50
db_instance_class        = "db.t3.small"
db_password              = "your-staging-db-password-here"
db_multi_az              = true
redis_node_type          = "cache.t3.small"
redis_num_clusters       = 1
eks_worker_instance_type = "t3.medium"
eks_worker_desired_count = 2
eks_worker_min_count     = 1
eks_worker_max_count     = 5