**overview** 

4 resources in terraform:   
storage bucket to store files   
bigquery dataset   
temp storage bucket for dataproc   
dataproc cluster   


**steps**
> 1, grant roles

storage admin, compute storage admin, bigquery admin, dataproc admin roles. enable dataproc API

> 2, `terraform init`

and then enter credential path, since i put credentials out of this folder.

> 3, `terraform plan`

type in credential path

> 4, `terraform apply`
