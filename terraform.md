# Terraform

## Introduction

Infrastucture as Code (IaC) tools allows users to manage their infrastucture with configuration files rather than graphical user interfaces. IaC provides a reliable and safe method of building and modifying resource configurations. Terraform is a HashiCorp IaC tool that lets you define your architecture in a human-readable format.

Terraform plugins (known as providers) lets Terraform communicate with various cloud platforms. Providers define individual units of infrastructure .

## Commands

### Plan

Creates an execution plan that allows the users to preview the changes made to the infrastructure via Terraform code. The `plan` command does not perform the actual changes but only showcases the differences between the two states. If not differences are detected then `terraform plan` will not do anything.

When Terraform creates a plan, it does the three following actions:

* Reads the current state of any already existing remote objects to ensure that the Terraform state is up-to-date
* Creates a note of any difference in the new configuration and priot state
* Proposes a set of change actions that should, if applied, make the remote objects match the configuration.

Users can provide the `-out=FILE` parameter to store the plan output in a file.
