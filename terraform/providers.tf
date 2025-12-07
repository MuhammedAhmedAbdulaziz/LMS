###############################################
# Provider configuration
# - Use eu-west-1 as default region (you can override via terraform.tfvars)
###############################################

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.4.0"
}

provider "aws" {
  region = var.aws_region
}
