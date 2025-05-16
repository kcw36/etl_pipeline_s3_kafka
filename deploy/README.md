# Deploy

- This is Terraform deploy scripts for deploying an AWS RDS instance on the cloud
- It uses the variables defined in a `terraform.tfvars` file that are used by `variables.tf`

## Install dependencies

- Terraform with brew
    - `brew tap hashicorp/tap`
    - `brew install hashicorp/tap/terraform`
- If `brew` is not installed but still on Mac run:
    - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- If not on mac, go to:
    - [Terraform download page](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

## Deploy Resources

- `terraform init`
    - Inititiate the terraform directory
- `terraform plan`
    - Show execution plan for main.tf
- `terraform apply`
    - Execute main.tf
    - Creates resources

## Output

- `terraform output`
    - Query output data from execution
    - Defined outputs in `outputs.tf`

## Clean Up

- `terraform destroy`
    - Deletes all resources that are made with the `apply`