############################################################
# EKS ADDONS
# Required for Production
############################################################

###############################
# 1) Amazon VPC CNI Add-on
###############################
resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "vpc-cni"

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
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "coredns"

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
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "kube-proxy"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

############################################################
# 4) Amazon EKS Pod Identity Agent
# REQUIRED before installing EBS CSI Driver
############################################################
resource "aws_eks_addon" "pod_identity" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "eks-pod-identity-agent"

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_cluster.this
  ]
}

############################################################
# REQUIRED BLOCK (MUST EXIST FOR EBS CSI TO WORK)
# EKS Pod Identity → IAM Role Association
############################################################
resource "aws_eks_pod_identity_association" "ebs_csi_assoc" {
  cluster_name    = aws_eks_cluster.this.name
  namespace       = "kube-system"
  service_account = "ebs-csi-controller-sa"
  role_arn        = aws_iam_role.ebs_csi_role.arn

  depends_on = [
    aws_iam_role.ebs_csi_role,
    aws_iam_role_policy_attachment.ebs_csi_driver_policy,
    aws_eks_addon.pod_identity
  ]
}


############################################################
# 5) Amazon EBS CSI Driver Add-on
# REQUIRED for PostgreSQL StatefulSets using EBS
############################################################
resource "aws_eks_addon" "ebs_csi" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "aws-ebs-csi-driver"

  # Role is now safely attached AFTER pod identity association
  #service_account_role_arn = aws_iam_role.ebs_csi_role.arn

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_pod_identity_association.ebs_csi_assoc
  ]
}
