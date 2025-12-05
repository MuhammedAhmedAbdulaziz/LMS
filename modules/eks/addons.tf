############################################################
# EKS ADDONS
# This file installs all required and recommended add-ons:
# - Amazon VPC CNI (Networking)
# - CoreDNS (DNS for cluster)
# - kube-proxy (Kubernetes service networking)
# - Amazon EKS Pod Identity Agent (REQUIRED for IRSA)
# - Amazon EBS CSI Driver (REQUIRED for dynamic EBS volumes)
############################################################

###############################
# 1) Amazon VPC CNI Add-on
###############################
resource "aws_eks_addon" "vpc_cni" {
  cluster_name            = aws_eks_cluster.this.name
  addon_name              = "vpc-cni"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

###############################
# 2) CoreDNS Add-on
###############################
resource "aws_eks_addon" "coredns" {
  cluster_name      = aws_eks_cluster.this.name
  addon_name        = "coredns"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

###############################
# 3) kube-proxy Add-on
###############################
resource "aws_eks_addon" "kube_proxy" {
  cluster_name      = aws_eks_cluster.this.name
  addon_name        = "kube-proxy"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

############################################################
# 4) Amazon EKS Pod Identity Agent
# REQUIRED for IRSA + REQUIRED before installing EBS CSI Driver
############################################################
resource "aws_eks_addon" "pod_identity" {
  cluster_name      = aws_eks_cluster.this.name
  addon_name        = "eks-pod-identity-agent"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

############################################################
# 5) Amazon EBS CSI Driver Add-on
# REQUIRED for dynamic PV provisioning in PostgreSQL StatefulSet
############################################################
resource "aws_eks_addon" "ebs_csi" {
  cluster_name               = aws_eks_cluster.this.name
  addon_name                 = "aws-ebs-csi-driver"
  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_addon.pod_identity   # MUST come before EBS CSI driver
  ]
}
