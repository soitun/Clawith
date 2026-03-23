# terraform/backend.tf
terraform {
  backend "s3" {
    bucket         = "clawith-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "clawith-terraform-state-lock"
  }
}