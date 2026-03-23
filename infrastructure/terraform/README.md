# Terraform Infrastructure for Clawith

This directory contains Terraform configurations to provision cloud infrastructure for the Clawith application.

## Prerequisites

- Terraform v1.0+
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create resources

## Architecture Overview

The infrastructure includes:
- VPC with public and private subnets
- EKS cluster for Kubernetes orchestration
- RDS PostgreSQL instance for primary database
- ElastiCache Redis for caching and sessions
- Security groups and networking components

## Deployment Environments

We support three deployment environments:
- Development (`dev`)
- Staging (`staging`)
- Production (`prod`)

Each environment has its own configuration in the `environments/` directory.

## Getting Started

### Initialize Terraform

```bash
cd infrastructure/terraform
terraform init
```

### Deploy to Development

```bash
cd environments/dev
terraform plan -var-file="../../variables.tf" -var="db_password=your-password"
terraform apply -var-file="../../variables.tf" -var="db_password=your-password"
```

### Deploy to Staging

```bash
cd environments/staging
terraform plan -var-file="../../variables.tf" -var="db_password=your-password"
terraform apply -var-file="../../variables.tf" -var="db_password=your-password"
```

### Deploy to Production

```bash
cd environments/prod
terraform plan -var-file="../../variables.tf" -var="db_password=your-password"
terraform apply -var-file="../../variables.tf" -var="db_password=your-password"
```

## State Management

Terraform state is stored remotely in S3 with DynamoDB for locking to support team collaboration. The configuration can be found in `backend.tf`.

## Module Structure

- `main.tf`: Main infrastructure configuration
- `variables.tf`: Input variables
- `modules/eks/`: EKS cluster module
- `environments/`: Environment-specific configurations

## Security

- All databases and caches are deployed in private subnets
- Security groups restrict traffic to necessary ports
- SSL/TLS encryption in transit for databases
- KMS encryption at rest for sensitive data