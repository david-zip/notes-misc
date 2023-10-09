# Deployment Strategies

Deployment strategies are methodologies to replaces older versions of applications with newer version whilst minimising application downtime and rollback risk. 

## Blue/Green Deployment

Blue/Green Deployment (also known as Red/Black Deployment) strategy is a deployment strategy in which two separate, yet identical environments are created and deployed to the user. The blue (current) environment is the current version of the application whilst the green (new) environment is the new application version. Users will be gradually relocated onto the green environment as other users will still be using the blue environment. 

A benefit of Blue/Green Deployment is that as the blue environment remains in deployment, if the green environment encounters any step-backs or is pulled from production, the blue environment will be on standby to completely replace the green environment. This results in reduced deployment risk as it simplifies the rollback if deployment fails. Another benefit is that it reduces the downtime during application updates, further mitigating the risk surrounding downtime and rollback functionality.

## A/B Deployment

A/B deployment is a variant of Blue/Green deployment where the new version of the application can be test on in a limited production environment. Here, the stable version will get most of the user request while the new version will get some of the user request.

As testing progress, if the product does not experience many issues, more users can be deployed on the new version. This continues until the stable version is ultimately replaced by the new version.

By implementing this strategy, new features can be experimented upon a subset of the general userbase to gather reactions to the changes.

For this method to be effective, both veresion must be able to run simultaneously. 

## All-At-Once Deployment

In All-At-Once Deployment, all traffic and users will be transferred immediately from the old environment to the new environment.

This deployment strategy may be preferred if there may be a security update to the application. by forcing everyone to update their versions simultaneously, one can get rid of all security risk and therefore ensure that their product is safe. However, if there is a bug or issue with the new version, re-deploying the previously version can increase application downtime.

## Canary Deployment

During Canary Deployment, the new version is incrementally released to new users gradually. These new features will continue to replace old features after being tested. As trust and insurance grows in the deployment, the new version will eventually replace the current version in its entirety. 

If at any point a new feature/implementatino fails during testing, the feature can be immediately rolled back and be worked upon.

Canary deployment strategies are partically useful when there should be little downtime during an application update and when the application can support both the old code and new code being deployed on production.

## Linear Deployment
Linear Deployment is the process of shifting traffic in equal increments with an equal number of minutes between increments between versions.

## In-Place Deployment



## References:
https://docs.aws.amazon.com/pdfs/whitepapers/latest/overview-deployment-options/overview-deployment-options.pdf