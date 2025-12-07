variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

# (We are using hardcoded subnets for this request; in production you may expose them)
