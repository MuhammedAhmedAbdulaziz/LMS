###############################################
# Root module calling VPC + EKS modules
###############################################

module "vpc" {
  source = "./modules/vpc"
}

module "eks" {
  source      = "./modules/eks"
  cluster_name = var.cluster_name
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.public_subnet_ids   # using public subnets for both control-plane ENIs & nodes (learning)
}
