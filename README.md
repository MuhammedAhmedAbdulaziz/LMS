# AWS EKS  (Terraform)

A compact, opinionated Terraform project that provisions a VPC and a small Amazon EKS cluster for learning and demonstration purposes.

This repository contains a root Terraform configuration that composes two local modules:

- `modules/vpc` — creates the VPC, subnets (public/private), NAT gateways, and routing.
- `modules/eks` — creates an EKS cluster and a managed node group.

This README documents the project layout, inputs/outputs, recommended workflow, verification steps, and troubleshooting notes.

## Quick facts / contract

- Inputs: Terraform variables (see `variables.tf` and `terraform.tfvars`) — primary inputs are `aws_region` and `cluster_name`.
- Outputs: VPC ID, subnet IDs, and EKS cluster endpoint/name via the root `outputs.tf`.
- Success criteria: `terraform apply` completes without API errors and an EKS control plane and node group appear in the AWS Console.
- Error modes: AWS credentials/permissions, exhausted IP address space, insufficient EC2 quotas, or conflicting resources in the target account/region.

## Files & structure

Root files:

- `main.tf` — root module wiring `modules/vpc` and `modules/eks` together.
- `providers.tf` — provider configuration; default region is `eu-west-1` and is overridable by `terraform.tfvars` or environment variables.
- `variables.tf` — root-level variables used by the root module.
- `terraform.tfvars` — example values used for local development (region and cluster name).
- `outputs.tf` — root-level outputs, re-exposing module outputs like `vpc_id` and `eks_cluster_endpoint`.
- `terraform.tfstate` / `.backup` — local state files (if present). Avoid committing sensitive state to public repos.

Modules:

- `modules/vpc` — responsible for VPC creation and subnets. Exposes `vpc_id`, `public_subnet_ids`, and `private_subnet_ids`.
- `modules/eks` — EKS cluster + managed node group. Important variables: `cluster_name`, `vpc_id`, `subnet_ids`, and node group sizing (`desired_size`, `min_size`, `max_size`).

Provider versions:

- This project uses the AWS provider pinned (in the workspace) to `~> 5.0` (see `.terraform.lock.hcl`).

## Variables (high-level)

The module-level defaults are tuned for a small learning cluster:

- `cluster_name` — default `azoz-eks` (root and module default). Change via `terraform.tfvars` or CLI.
- `aws_region` — default `eu-west-1` in `terraform.tfvars`.
- Node sizing: `node_instance_type` default `t3.small` and default node counts are small (1–2 nodes). These are intentionally conservative for demos.

See `modules/eks/variables.tf` and `variables.tf` for the full list and types.

## Prerequisites

- Terraform >= 1.4.0 (project indicates required_version). Install from https://www.terraform.io.
- AWS CLI (optional but useful for kubeconfig integration): https://aws.amazon.com/cli/
- An AWS account and credentials configured locally. The terraform AWS provider will honor the usual environment variables, `~/.aws/credentials`, or other supported auth methods.
- Sufficient AWS quotas (EC2 instances, EIP, NAT gateways, EKS cluster limits) in the chosen region.

Important security note: this project stores state locally by default. For multi-user or production scenarios, use a remote backend (S3 + DynamoDB) and avoid committing state files.

## Typical workflow

1. Inspect variables and adjust as needed:

   - Edit `terraform.tfvars` or create an override file, e.g. `production.tfvars`.

2. Initialize the working directory:

   terraform init

3. Validate & format (optional but recommended):

   terraform fmt -recursive
   terraform validate

4. Create an execution plan:

   terraform plan -out=plan.tfplan

5. Apply the plan:

   terraform apply "plan.tfplan"

6. After apply, inspect outputs:

   terraform output

   Example outputs provided by the root module include `vpc_id`, `public_subnet_ids`, `private_subnet_ids`, `eks_cluster_endpoint`, and `eks_cluster_name`.

## Configure kubectl for the created EKS cluster

Once the cluster is created, get cluster credentials (AWS CLI must be configured):

   aws eks --region <region> update-kubeconfig --name <cluster_name>

Example using defaults in this repo:

   aws eks --region eu-west-1 update-kubeconfig --name azoz-eks

Verify nodes and cluster objects with `kubectl get nodes` and `kubectl get pods --all-namespaces`.

## Teardown / destroy

To remove everything this project created, run:

   terraform destroy

Be careful: this will delete the EKS cluster and all EC2 instances, NAT gateways, and associated resources. Expect EIP/NAT cleanup to take a few minutes due to AWS resource lifecycle.

## Testing & verification checklist

- Terraform init & plan succeed.
- Terraform apply finishes with no AWS API errors.
- `terraform output` shows the expected values for VPC and EKS resources.
- `aws eks update-kubeconfig` produces a kubeconfig entry and `kubectl get nodes` shows worker nodes in Ready state.

## Troubleshooting

- AWS auth errors: ensure environment variables (AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY), named profiles, or an EC2 role provide the necessary permissions.
- Quota errors: check EC2 service quotas (instances, ENIs) and request increases if necessary.
- VPC CIDR overlaps: if you already have a VPC in the account/region using the same CIDR ranges, create in a different region or adjust module configuration.
- Long NAT gateway deletions: deleting NAT gateways and associated EIPs can sometimes take a few minutes; wait and re-run `terraform apply`/`destroy` if necessary.

## Extending this project

- Add a remote state backend (recommended: S3 + DynamoDB for locking).
- Add module tests using `terraform validate` and `tflint` or `checkov`.
- Add an IAM/OIDC provider and RBAC mappings if you want to manage cluster roles and service accounts.
- Replace public subnet usage for nodes with private subnets and NAT gateway egress for production clusters.

## Notes / Caveats

- The example root module currently passes `module.vpc.public_subnet_ids` into the EKS module, which places both control-plane ENIs and nodes into the public subnets — this is intended for learning and convenience only and is not recommended for production workloads.
- Keep the `terraform.tfvars` values and any secrets out of version control.

## Useful commands reference

- terraform init
- terraform plan -out=plan.tfplan
- terraform apply "plan.tfplan"
- terraform output
- terraform destroy
- aws eks --region <region> update-kubeconfig --name <cluster_name>

## License & contributions

This repository is provided as-is for learning purposes. If you want to contribute, open a PR or file an issue describing the change.

---

If you'd like, I can also:

- Add a minimal `README` badge/status or a `Makefile` with helpers for `init/plan/apply/destroy`.
- Add a `backend.tf` example for S3 remote state (non-destructive).

If you want any of that, tell me which option you prefer and I'll add it.
