############################################################
# EKS ADDONS
# Required and Recommended for Production
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
# REQUIRED for IRSA + REQUIRED before installing EBS CSI Driver
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
# 5) Amazon EBS CSI Driver Add-on
# REQUIRED for PostgreSQL StatefulSets using EBS
# NOW FIXED: includes service_account_role_arn
############################################################

resource "aws_eks_addon" "ebs_csi" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "aws-ebs-csi-driver"

  # FIX: Attach IAM role — this prevents DEGRADED state
  service_account_role_arn = aws_iam_role.ebs_csi_role.arn

  resolve_conflicts_on_create = "OVERWRITE"
  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_addon.pod_identity,
    aws_iam_role_policy_attachment.ebs_csi_driver_policy
  ]
}
