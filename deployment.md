Deployment

Green/Blue
(https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/bluegreen-deployments.html)
- Releases new applicaiton model that gradually transfers users to the new model
- Create two seperate, identical environments
  - One running current app version
  - One running new application version
- Both are running in production
- old version is old environment
- new version is green environment
- When green is fully deployed - blue will remain on standby 
  - In case of rollback or pulled from production
  - Blue will be updated to be the template of the next update
- Increases applicaiton availability
- Reduces deployment risk by simplifying rollback if deployment fails

One Shot

Canary

