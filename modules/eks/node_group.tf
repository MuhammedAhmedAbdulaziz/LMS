###############################################
# Managed Node Group
###############################################

resource "aws_eks_node_group" "this" {
  cluster_name    = aws_eks_cluster.this.name
  node_group_name = "${var.cluster_name}-node-group"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = var.desired_size
    min_size     = var.min_size
    max_size     = var.max_size
  }

  instance_types = [var.node_instance_type]

  tags = {
    Name = "${var.cluster_name}-nodegroup"
  }

  # Ensure cluster exists first
  depends_on = [
    aws_eks_cluster.this
  ]
}
