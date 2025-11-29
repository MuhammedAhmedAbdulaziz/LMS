###############################################
# EKS control plane
###############################################

resource "aws_eks_cluster" "this" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster_role.arn

  version = "1.30"

  vpc_config {
    subnet_ids = var.subnet_ids

    # Public access to API for learning; in prod consider private access + VPN/Bastion
    endpoint_public_access = true
    endpoint_private_access = false
  }

  tags = {
    Name = var.cluster_name
  }

  # ensure IAM role is attached before cluster creation
  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_AmazonEKSClusterPolicy
  ]
}
