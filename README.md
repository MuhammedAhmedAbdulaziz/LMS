# LMS Application – AWS EKS Deployment Guide

## 🚀 Deployment Order Summary (Start Here)

To avoid deployment failures and ensure a smooth setup, follow this order **exactly**:

### **1️⃣ Create Namespace (Required First Step)**

```bash
kubectl apply -f k8s/00-namespace.yml
```

All remaining manifests depend on this namespace.

### **2️⃣ Create EKS Cluster and Node Group**

* Create cluster (EKS Console)
* Create node group (same AZ subnets)
* Connect using kubeconfig

### **3️⃣ Install All Required Add-ons (Before Any Manifests)**

#### Default EKS Add-ons (auto-installed)

* Amazon VPC CNI
* CoreDNS
* kube-proxy

#### Required Production Add-ons (install manually)

* **Amazon EBS CSI Driver** (Required for PostgreSQL PVC)
* **Amazon GuardDuty EKS Runtime Monitoring** (Recommended)

### **4️⃣ Apply StorageClass**

```bash
kubectl apply -f k8s/06-storageclass-ebs.yml
```

### **5️⃣ Deploy PostgreSQL (StatefulSet + PVC)**

```bash
kubectl apply -f k8s/01-postgres-secret.yml
kubectl apply -f k8s/03-postgres-statefulset.yml
```

### **6️⃣ Deploy Flask Application**

```bash
kubectl apply -f k8s/04-flask-app-deployment.yml
```

### **7️⃣ Verify Everything**

```bash
kubectl get all -n library-app
kubectl get pvc -n library-app
kubectl get svc -n library-app
```

### **8️⃣ Access Application**

Use the LoadBalancer URL from:

```bash
kubectl get svc -n library-app
```

---

(Enterprise Edition)

This document provides a **clean, production-ready technical guide** for deploying the LMS application on **AWS Elastic Kubernetes Service (EKS)**. It includes all required steps from environment preparation to cluster deployment, application rollout, persistent storage setup, and cluster access management.

---

# 📌 1. Overview

The LMS application is a Flask-based system backed by PostgreSQL. For production, it runs on:

* **AWS EKS** (Elastic Kubernetes Service)
* **Amazon EBS CSI Driver** for persistent volumes
* **AWS Load Balancer** for external access
* **Kubernetes StatefulSet** for PostgreSQL
* **Kubernetes Deployment** for Flask

This guide describes **how to deploy the application from scratch on AWS EKS**.

---

# 📦 2. Prerequisites

## AWS Requirements

* AWS account
* IAM user with:

  * EKS Full Access
  * EC2 Full Access
  * IAM Access
  * VPC Access
* Installed tools:

  * AWS CLI v2
  * kubectl (latest)
  * Docker (optional for image rebuilds)

Verify AWS and kubectl configuration:

```bash
aws sts get-caller-identity
kubectl version --client
```

---

# ☁️ 3. EKS Cluster Deployment

## Step 1 — Create EKS Cluster (Console)

1. Go to **EKS Console → Create Cluster**.
2. Cluster name: `LMS-cluster`
3. Kubernetes version: latest stable
4. Authentication: **EKS API** (default)
5. Create IAM cluster role → **EKSClusterRole**
6. Create the cluster.

## Step 2 — Configure Networking

* Use the default or custom VPC
* Select **two subnets in the same AZ** for node groups
* Cluster endpoint access: **Public**

## Step 3 — Install Required & Recommended Add-ons

EKS requires several core add-ons to operate correctly. For production clusters (and to avoid deployment issues such as PVC not binding, runtime errors, or missing node agents), all of the following add-ons should be installed **before applying any application manifests**.

### ✅ Default Kubernetes Add-ons (installed by AWS EKS automatically)

* **Amazon VPC CNI** – Manages pod networking
* **CoreDNS** – Cluster DNS service
* **kube-proxy** – Handles Kubernetes Service networking

### ⭐ Recommended Add-ons (must be installed manually)

Installing these early prevents storage, runtime, and monitoring issues.

#### 1. **Amazon EBS CSI Driver** (Required for Postgres)

Enables dynamic provisioning of EBS volumes used by PostgreSQL StatefulSet.

* Navigate to: *EKS Console → LMS-cluster → Add-ons → Add add-on*
* Choose: **Amazon EBS CSI Driver**
* Access type: **EKS Pod Identity**
* Create recommended IAM Role

Without this add-on, your `PersistentVolumeClaim` stays **Pending**, and PostgreSQL will never start.

#### 2. **Amazon GuardDuty EKS Runtime Monitoring** (Recommended for security)

Adds runtime threat detection inside worker nodes.

* Requires GuardDuty enabled in your AWS account
* Access type: **EKS Pod Identity**

Installing this early ensures complete cluster observability and runtime protection.

---

* VPC CNI
* CoreDNS
* kube-proxy

Wait until the cluster shows **Active**.

---

# 👷‍♂️ 4. Node Group Setup

## Step 1 — Create Node Group

* Name: `LMS-NG`
* Node IAM role: **EKSNodeRole**
* Instance type: `t3.small`
* Desired: 1
* Select **same subnets** used by the cluster

Once created, verify:

```bash
aws eks update-kubeconfig --region eu-west-1 --name LMS-cluster
kubectl get nodes
```

---

# 🛢 5. Apply Namespace (Required First Step)

All Kubernetes resources for this project live inside the `library-app` namespace.
This must be created **before applying any other manifest**, otherwise all deployments and services will fail.

Apply namespace:

```bash
kubectl apply -f k8s/00-namespace.yml
```

Verify:

```bash
kubectl get ns
```

You should see:

```
library-app   Active
```

---

# 🛢 6. Storage Setup (EBS CSI Driver) (EBS CSI Driver)

## Step 1 — Install the EBS CSI Driver (Console)

Navigate to:
**EKS → LMS-cluster → Add-ons → Add add-on**

Install:

* **Amazon EBS CSI Driver**
* Use: **EKS Pod Identity**
* Create recommended IAM role

## Step 2 — Apply StorageClass

File: `06-storageclass-ebs.yml`

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
reclaimPolicy: Delete
parameters:
  type: gp3
```

Apply:

```bash
kubectl apply -f k8s/06-storageclass-ebs.yml
```

---

# 🗄️ 6. PostgreSQL Deployment (StatefulSet)

## Step 1 — Create Secret

```bash
kubectl apply -f k8s/01-postgres-secret.yml
```

## Step 2 — Deploy StatefulSet

The StatefulSet:

* Uses the `ebs-sc` StorageClass
* Avoids the `lost+found` issue by setting `PGDATA=/var/lib/postgresql/data/pgdata`

Apply:

```bash
kubectl apply -f k8s/03-postgres-statefulset.yml
```

Verify:

```bash
kubectl get pods -n library-app
kubectl get pvc -n library-app
```

Postgres pod should reach **Running**.

---

# 🐍 7. Deploy Flask Application

Apply Deployment + LoadBalancer service:

```bash
kubectl apply -f k8s/04-flask-app-deployment.yml
```

Check status:

```bash
kubectl get pods -n library-app
kubectl get svc -n library-app
```

You will see:

```
flask-app-service   LoadBalancer   ...   <AWS-ELB-DNS>
```

Access the application at:

```
http://<AWS-ELB-DNS>
```

---

# 🌐 8. Namespace Structure

All resources run inside:

```bash
kubectl apply -f k8s/00-namespace.yml
```

Namespace name: `library-app`

---

# 👤 9. Team Access (IAM + Access Entries)

EKS now uses **Access Entries** instead of aws-auth.

## Step 1 — Create IAM User

Each team member gets an IAM user.

## Step 2 — Add Access Entry

Navigate to:
**EKS → LMS-cluster → Access → Create access entry**

Choose:

* Principal type: **IAM User**
* Access scope: **Cluster**
* Access policy: **AmazonEKSAdminPolicy**

## Step 3 — User connects

User runs:

```bash
aws configure
aws eks update-kubeconfig --region eu-west-1 --name LMS-cluster
kubectl get nodes
```

---

# 🔒 10. Kubernetes RBAC (Optional)

For namespace-restricted access:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-admin
  namespace: dev1
subjects:
  - kind: User
    name: arn:aws:iam::<ACCOUNT-ID>:user/dev1
roleRef:
  kind: ClusterRole
  name: admin
  apiGroup: rbac.authorization.k8s.io
```

Apply:

```bash
kubectl apply -f k8s/07-ns-admin.yaml
```

---

# 🧪 11. Monitoring Deployment

Check all objects:

```bash
kubectl get all -n library-app
```

Logs:

```bash
kubectl logs deployment/flask-app-deployment -n library-app
```

---

# 🧹 12. Cleanup

To delete all resources:

```bash
kubectl delete namespace library-app
```

To delete entire cluster:

* Go to **EKS Console → Delete cluster**

---

# ✔ Final Notes

This deployment guide is designed for **production EKS environments** and includes:

* Secure database deployment with EBS
* Cloud-native microservice design
* Proper access control

