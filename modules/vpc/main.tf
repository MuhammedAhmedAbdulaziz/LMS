###############################################
# VPC module - main.tf
#
# Creates:
#  - VPC 10.0.0.0/16
#  - 2 public subnets (10.0.1.0/24, 10.0.2.0/24)
#  - 2 private subnets (10.0.3.0/24, 10.0.4.0/24)
#  - Internet Gateway, Public route table, NAT Gateways
#  - Route table associations
#
# Subnets are placed in different AZs (eu-west-1a & eu-west-1b).
###############################################

resource "aws_vpc" "this" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = { Name = "azoz-vpc" }
}

# Internet Gateway for public subnets
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "azoz-igw" }
}

# Public route table -> IGW
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "azoz-public-rt" }
}

resource "aws_route" "public_default_route" {
  route_table_id         = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

# Public subnets
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-west-1a"
  tags                    = { Name = "azoz-public-1" }
}

resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "eu-west-1b"
  tags                    = { Name = "azoz-public-2" }
}

# Associate public subnets with the public route table
resource "aws_route_table_association" "public_1_assoc" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public_rt.id
}
resource "aws_route_table_association" "public_2_assoc" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public_rt.id
}

# Allocate EIPs for NATs
resource "aws_eip" "nat_a_eip" {
  vpc = true
  tags = { Name = "azoz-nat-a-eip" }
}
resource "aws_eip" "nat_b_eip" {
  vpc = true
  tags = { Name = "azoz-nat-b-eip" }
}

# NAT Gateways (placed in public subnets)
resource "aws_nat_gateway" "nat_a" {
  allocation_id = aws_eip.nat_a_eip.id
  subnet_id     = aws_subnet.public_1.id
  tags          = { Name = "azoz-nat-a" }
  depends_on    = [aws_internet_gateway.igw]
}

resource "aws_nat_gateway" "nat_b" {
  allocation_id = aws_eip.nat_b_eip.id
  subnet_id     = aws_subnet.public_2.id
  tags          = { Name = "azoz-nat-b" }
  depends_on    = [aws_internet_gateway.igw]
}

# Private subnets
resource "aws_subnet" "private_1" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.3.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "eu-west-1a"
  tags                    = { Name = "azoz-private-1" }
}

resource "aws_subnet" "private_2" {
  vpc_id                  = aws_vpc.this.id
  cidr_block              = "10.0.4.0/24"
  map_public_ip_on_launch = false
  availability_zone       = "eu-west-1b"
  tags                    = { Name = "azoz-private-2" }
}

# Private route tables for each AZ → NAT
resource "aws_route_table" "private_rt_a" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "azoz-private-rt-a" }
}
resource "aws_route_table" "private_rt_b" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "azoz-private-rt-b" }
}

resource "aws_route" "private_a_to_nat" {
  route_table_id         = aws_route_table.private_rt_a.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_a.id
}

resource "aws_route" "private_b_to_nat" {
  route_table_id         = aws_route_table.private_rt_b.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat_b.id
}

resource "aws_route_table_association" "private_1_assoc" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private_rt_a.id
}
resource "aws_route_table_association" "private_2_assoc" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private_rt_b.id
}
