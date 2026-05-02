---
name: terraform
description: >
  Write, maintain, and debug Terraform infrastructure as code including providers,
  resources, modules, state management, variables, outputs, and provisioning.
  Covers HashiCorp Configuration Language (HCL), remote state, workspaces, and
  cloud provider integrations (Azure, AWS, GCP, Databricks). USE FOR: IaC,
  resource provisioning, state management, modules, variables, outputs, providers,
  remote backends, workspaces, lifecycle management. DO NOT USE FOR: Packer images,
  Consul clusters, Vault configuration, general cloud CLI commands.
location: .roo/skills/terraform/SKILL.md
metadata:
  created: "2026-04-27"
  version: "1.0.0"
  compatibility:
    - terraform>=1.5.0
    - hashicorp/azurerm>=3.0
    - databricks/databricks>=1.0
---

# Terraform Infrastructure as Code Skill

## When to Use This Skill

- Writing Terraform configurations for cloud resources
- Managing Terraform state files and remote backends
- Creating reusable Terraform modules
- Setting up multi-cloud infrastructure
- Configuring provisioners (file, local-exec, remote-exec)
- Debugging Terraform plan/apply errors
- Managing Terraform workspaces

## When NOT to Use This Skill

- Packer image building → use Packer skill
- Consul service mesh → use Consul skill
- Vault secrets management → use Vault skill
- Kubernetes manifests → use Kubernetes skill

## Inputs Required

1. Target cloud provider (Azure, AWS, GCP)
2. Resource specifications
3. Environment configuration
4. State backend configuration

## Workflow

### Step 1: Terraform Configuration Block

From [`src/terraform/conf/main.tf`](src/terraform/conf/main.tf):

```hcl
terraform {
  required_version = ">= 1.5.0, <= 1.5.2"

  # Remote backend for shared state
  backend "azurerm" {
    resource_group_name  = "torro-rg"
    storage_account_name = "torrostate001"
    container_name       = "tfstate"
    key                  = "terraform/terraform.tfstate"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.75.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "1.38.0"
    }
  }
}
```

### Step 2: Provider Configuration

```hcl
# Azure Provider
provider "azurerm" {
  skip_provider_registration = true
  features {}
  # use_msi = true  # For managed identity authentication
}

# Databricks Provider with alias for accounts workspace
provider "databricks" {
  alias      = "accounts"
  host       = "https://accounts.azuredatabricks.net"
  account_id = "{databricks_account_id}"
}

# Databricks Provider for workspace
provider "databricks" {
  # azure_client_id     = var.client_id
  # azure_client_secret = var.client_secret
  # azure_tenant_id     = var.tenant_id
  azure_use_msi = true  # Recommended for production
}
```

### Step 3: Data Sources

From [`src/terraform/template/databricks_workspace.tf`](src/terraform/template/databricks_workspace.tf):

```hcl
# Reference existing Azure resources
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

data "azurerm_storage_account" "torro" {
  name                = var.storage_account_name
  resource_group_name = data.azurerm_resource_group.rg.name
}

# Reference existing Databricks workspace
data "azurerm_databricks_workspace" "existing" {
  name                = var.workspace_name
  resource_group_name = var.resource_group_name
}

# Reference existing Databricks account
data "databricks_account_group" "example" {
  provider = databricks.accounts
  external_id = "{external_group_id}"
}
```

### Step 4: Resource Definitions

From [`src/terraform/template/databricks_workspace.tf`](src/terraform/template/databricks_workspace.tf):

```hcl
# Databricks Workspace
resource "azurerm_databricks_workspace" "workspace" {
  name                        = var.workspace_name
  resource_group_name         = data.azurerm_resource_group.rg.name
  location                    = data.azurerm_resource_group.rg.location
  sku                         = "premium"
  managed_resource_group_name = "${data.azurerm_resource_group.rg.name}-${var.workspace_name}"

  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Access Connector (Managed Identity)
resource "azurerm_databricks_access_connector" "connector" {
  name                = "access_connector_${var.workspace_name}"
  resource_group_name = data.azurerm_resource_group.rg.name
  location            = data.azurerm_resource_group.rg.location

  identity {
    type = "SystemAssigned"
  }
}

# Role Assignment for Storage Access
resource "azurerm_role_assignment" "storage_role" {
  scope                = data.azurerm_storage_account.torro.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_databricks_access_connector.connector.identity[0].principal_id
}
```

### Step 5: Databricks Resources

From [`src/terraform/template/databricks_data_metastore.tf`](src/terraform/template/databricks_data_metastore.tf):

```hcl
# Databricks Metastore
resource "databricks_metastore" "metastore" {
  provider      = databricks.accounts
  name          = "${var.workspace_name}_metastore"
  storage_root  = format("abfss://%s@%s.dfs.core.windows.net", var.container_name, var.storage_account_name)
  owner         = "jnufung@gmail.com"
}

# Metastore Assignment to Workspace
resource "databricks_metastore_assignment" "assignment" {
  provider        = databricks.accounts
  workspace_id    = azurerm_databricks_workspace.workspace.workspace_id
  metastore_id    = databricks_metastore.metastore.id
  default_catalog = "hive_metastore"
}

# Storage Credential (Managed Identity)
resource "databricks_storage_credential" "credential" {
  provider     = databricks.accounts
  name         = azurerm_databricks_access_connector.connector.name
  metastore_id = databricks_metastore.metastore.id
  owner        = "admin@torro.ai"
  
  azure_managed_identity {
    access_connector_id = azurerm_databricks_access_connector.connector.id
  }
  
  comment = "Managed by Terraform"
  
  depends_on = [
    databricks_metastore_assignment.assignment
  ]
}

# External Location
resource "databricks_external_location" "external" {
  provider          = databricks.accounts
  name              = "${var.storage_account_name}_external"
  url               = format("abfss://%s@%s.dfs.core.windows.net", var.container_name, var.storage_account_name)
  credential_name   = databricks_storage_credential.credential.id
  comment           = "Managed by Terraform"
  isolation_mode    = "Open"  # or "Isolated"
}
```

### Step 6: Variables and Outputs

```hcl
# Variables
variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "torro-prod-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus2"
}

variable "workspace_name" {
  description = "Databricks workspace name"
  type        = string
}

variable "storage_account_name" {
  description = "Azure storage account name"
  type        = string
}

variable "container_name" {
  description = "Azure storage container name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# Outputs
output "databricks_workspace_id" {
  description = "Databricks workspace ID"
  value       = azurerm_databricks_workspace.workspace.workspace_id
}

output "databricks_host" {
  description = "Databricks workspace URL"
  value       = "https://${azurerm_databricks_workspace.workspace.workspace_url}/"
}

output "storage_account_id" {
  description = "Storage account resource ID"
  value       = data.azurerm_storage_account.torro.id
}

output "metastore_id" {
  description = "Databricks metastore ID"
  value       = databricks_metastore.metastore.id
}
```

### Step 7: Remote State Data Source

From [`src/terraform/template/databricks_data_metastore.tf`](src/terraform/template/databricks_data_metastore.tf):

```hcl
# Reference state from another Terraform run
data "terraform_remote_state" "torro_system" {
  backend = "local"
  
  config = {
    path = "${path.module}/../system/terraform.tfstate"
  }
}

# Or with remote backend
data "terraform_remote_state" "networking" {
  backend = "azurerm"
  
  config = {
    resource_group_name  = "torro-rg"
    storage_account_name = "torrostate001"
    container_name       = "tfstate"
    key                  = "networking/terraform.tfstate"
  }
}

# Use remote state values
resource "azurerm_databricks_workspace" "workspace" {
  name                = var.workspace_name
  resource_group_name = data.terraform_remote_state.networking.outputs.resource_group_name
  location            = data.terraform_remote_state.networking.outputs.location
  # ...
}
```

### Step 8: Resource Lifecycle Management

```hcl
# Control resource creation/deletion order
resource "azurerm_storage_container" "data" {
  name                  = var.container_name
  storage_account_name  = data.azurerm_storage_account.torro.name
  container_access_type = "private"

  lifecycle {
    prevent_destroy = false  # Set true for production
  }
}

# Ignore specific attribute changes
resource "azurerm_databricks_workspace" "workspace" {
  # ...
  
  lifecycle {
    ignore_changes = [
      tags["LastModifiedBy"],  # Ignore external tag changes
    ]
  }
}

# Create before destroy (for zero-downtime replacements)
resource "azurerm_databricks_workspace" "new" {
  # ...
  
  lifecycle {
    create_before_destroy = true
  }
}
```

### Step 9: Provisioners

From [`src/terraform/conf/`](src/terraform/conf/):

```hcl
# File provisioner - copy files to resource
resource "azurerm_linux_virtual_machine" "example" {
  # ...
  
  provisioner "file" {
    source      = "${path.module}/scripts/setup.sh"
    destination = "/tmp/setup.sh"
    
    connection {
      type        = "ssh"
      host        = self.public_ip_address
      user        = "admin"
      private_key = var.ssh_private_key
    }
  }
}

# Local-exec - run local commands
resource "null_resource" "trigger" {
  provisioner "local-exec" {
    command = "echo 'Infrastructure created' >> ${path.module}/output.log"
  }
}

# Remote-exec - run commands on remote resource
resource "azurerm_linux_virtual_machine" "example" {
  # ...
  
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup.sh",
      "/tmp/setup.sh",
      "systemctl restart app.service"
    ]
    
    connection {
      type        = "ssh"
      host        = self.public_ip_address
      user        = "admin"
      private_key = var.ssh_private_key
    }
  }
}
```

### Step 10: Common Azure Resources

```hcl
# Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  
  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Storage Account
resource "azurerm_storage_account" "data" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  tags = {
    Environment = var.environment
  }
}

# Storage Container
resource "azurerm_storage_container" "data" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.data.name
  container_access_type = "private"
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                        = "${var.environment}-kv-001"
  resource_group_name         = azurerm_resource_group.rg.name
  location                    = azurerm_resource_group.rg.location
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  soft_delete_enabled         = true
  purge_protection_enabled    = false
  
  sku_name = "standard"
  
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = var.admin_object_id
    
    key_permissions    = ["Get", "List", "Create", "Decrypt"]
    secret_permissions = ["Get", "List", "Set", "Delete"]
    storage_permissions = ["Get", "List"]
  }
}
```

### Step 11: State Management

```bash
# Initialize Terraform
terraform init

# Initialize with specific backend config
terraform init -backend-config="storage_account_name=myaccount" \
               -backend-config="container_name=tfstate" \
               -backend-config="key=prod/terraform.tfstate"

# Plan changes
terraform plan -out=plan.tfplan
terraform plan -var="environment=production" -out=plan.tfplan

# Apply changes
terraform apply plan.tfplan
terraform apply -auto-approve

# Show current state
terraform state list
terraform state show azurerm_databricks_workspace.workspace

# Import existing resource
terraform import azurerm_databricks_workspace.workspace /subscriptions/.../resourceGroups/.../providers/Microsoft.Databricks/workspaces/...

# Move resource in state
terraform state mv azurerm_databricks_workspace.old azurerm_databricks_workspace.new

# Remove resource from state (not delete)
terraform state rm azurerm_databricks_workspace.workspace

# Workspaces
terraform workspace new development
terraform workspace select development
terraform workspace list
```

### Step 12: Module Structure

```
infrastructure/
├── main.tf              # Root module
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── providers.tf         # Provider configuration
├── modules/
│   ├── workspace/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── storage/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── networking/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   └── main.tf
│   ├── staging/
│   │   └── main.tf
│   └── production/
│       └── main.tf
└── scripts/
    ├── setup.sh
    └── cleanup.sh
```

## Troubleshooting

### State Lock Issues

```bash
# Force unlock (if lock is stale)
terraform force-unlock LOCK_ID

# Check lock status
terraform state list
```

### Provider Authentication

```bash
# Azure CLI authentication
az login
az account set --subscription "{subscription_id}"

# Verify authentication
az account show
```

### Plan Shows Unexpected Changes

```bash
# Refresh state from cloud
terraform refresh

# Check what's managed vs unmanaged
terraform state list

# Import unmanaged resources
terraform import azurerm_storage_container.data mycontainer
```

## Related Files

- [`src/terraform/conf/main.tf`](src/terraform/conf/main.tf)
- [`src/terraform/template/databricks_workspace.tf`](src/terraform/template/databricks_workspace.tf)
- [`src/terraform/template/databricks_data_metastore.tf`](src/terraform/template/databricks_data_metastore.tf)
- [`src/terraform/template/databricks_storage_credential.tf`](src/terraform/template/databricks_storage_credential.tf)
- [`src/terraform/template/databricks_catalog.tf`](src/terraform/template/databricks_catalog.tf)
- [`/tmp/terraform-repo/internal/builtin/providers/`](/tmp/terraform-repo/internal/builtin/providers/)
- [`/tmp/terraform-repo/internal/builtin/provisioners/`](/tmp/terraform-repo/internal/builtin/provisioners/)
