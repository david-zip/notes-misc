# SageMaker Pipelines: 

## Introduction to MLOps

Machine Learning Operations (MLOps) is a branch of machine learning engineering which focuses on methods that streamlines the deployment of machine learning model to production, monitoring the models, and maintaining their quality. By implementing MLOps methodologies, engineers can continually deploy high-quality models quickly through the use of Continuous Integration and Deployment (CI/CD) methods.

One methodology that ML engineers can apply is a Machine Leaning Pipeline. A machine learning pipeline will allow ML engineering to automate the workflow of model creation, model training, model evaluation, and model deployment. This moves the engineers focus to develop high-quality pipelines and therefore high-quality models will be produces. Thus, machine learning pipelines improves teh scalability of machine learning .

https://www.databricks.com/glossary/mlops
https://valohai.com/machine-learning-pipeline/

### Machine Learning Life Cycle
All machine learning projects will 

#### Data gathering 

#### Data analysis 

#### Data transformation/preparation 

#### Model training & development  

#### Model validation  

### Model serving  

### Model monitoring  

### Model re-training

## Model Creation Steps
1. Data processing step
    - Runs a SageMaker Processing job using the input raw data in S3 and outputs training, validation, and test splits to S3. 

2. Training step
    - Trains an XGBoost model using SageMaker training jobs with training and validation data in S3 as inputs and stores the trained model artifact in S3. 

3. Evaluation step
    - Evaluates the model on the test dataset by running a SageMaker Processing job using the test data and the model artifact in S3 as inputs, and stores the output model performance evaluation report in S3. 

4. Conditional step 
    - Compares model performance on the test dataset against the threshold. Runs a SageMaker Pipelines predefined step using the model performance evaluation report in S3 as input and stores the output list of pipeline steps that will be executed if model performance is acceptable. 

5. Create model step
    - Runs a SageMaker Pipelines predefined step using the model artifact in S3 as an input and stores the output SageMaker model in S3. 

6. Bias check step
    - Checks for model bias using SageMaker Clarify with the training data and model artifact in S3 as inputs and stores the model bias report and baseline metrics in S3. 

7. Model explainability step
    - Runs SageMaker Clarify with the training data and model artifact in S3 as inputs and stores the model explainability report and baseline metrics in S3. 

8. Register step
    - Runs a SageMaker Pipelines predefined step using the model, bias, and explainability baseline metrics as inputs to register the model in the SageMaker Model Registry. 

9. Deploy step
    - Runs a SageMaker Pipelines predefined step using an AWS Lambda handler function, the model, and the endpoint configuration as inputs to deploy the model to a SageMaker Real-Time Inference endpoint. 

## Model Monitoring 

Amazon SageMaker Model Monitor monitors the quality of Amazon SageMaker machine learning models in production. 

After a model has been trained and deployed, it must be continuously monitored to ensure it maintains production criteria and gets re-trained if it does not. 

Amazon SageMaker Model Monitor allows one to log the input, output, and metadata of every invocation of a model after deployment. This enables the user to constantly analyse and evaluate whether the model is still fit for deployment. Amazon CloudWatch Logs collects all monitoring logs and will notify the user when set thresholds are triggered. Model monitoring can be conducted using real-time endpoints or in batch using a scheduler. 

To monitor the inputs, endpoints, and inference outputs from the deployed model, users can utilise a feature known as Data Capture. Data Capture can be implemented either in real-time or batch using AWS SDK `boto3`.  

To capture real-time inference data for monitoring model data quality, `DataCaptureConfig` must be defined as a new capture option when the model is deployed to the endpoint. This instance can be passed as an object to the `DataCaptureConfig` paramter in `Model.deploy()`. 

### Model decay
Model Drift (or model decay) is the degradation of an ML model’s predictive ability. Caused by changes in the digital environment, and the subsequent changes in variables such as concept and data, model drift is prominent in ML models simply by the nature of the machine language model as a whole. 

### Data Drift
The most common type of model drift, occurs when the statistical properties of certain predictors change. As the variables change, the model is subject to failure as a result. A model that might work during one time period might not see the same efficacy when applied to a different environment, simply because the data is not tailored to the changing variables. 

### Concept Drift
When the statistical attributes of target variables in a model change, concept drift occurs. Simply put, if the very nature of the model’s variables change then the model cannot function as intended. 

### Overfitting
Your model is overfitting your training data when you see that the model performs well on the training data but does not perform well on the evaluation data. This is because the model is memorizing the data it has seen and is unable to generalize to unseen examples. 

### Model Aging  

### Threshold  

## Model retraining:   

Steps involved in model retraining: 

Data Collection:  

Data Preprocessing. 

Model Selection:  

Hyperparameter Tuning:. 

Training:. 

Evaluation:  

Deployment:  

Monitoring:. 

## Inference
Inference Machine learning entails running the model on real data to get actionable results. During this stage, the inference system takes end-user inputs, analyzes the information, feeds it into the model, and returns outputs to users. 

### How does it work? 

In addition to the model, 3 key components are required to construct an ML inference environment: 

Data sources – A data source is often a system that collects live data from the mechanism that creates the data. A data source might, for example, be a cluster that stores data. A data source might also be a simple web application that captures user clicks and provides data to the server that contains the ML model. 

Host system – The ML model’s host system takes data from sources and feeds it all into the model. The infrastructure required to transform the inference code in machine learning into a completely running application is provided by the host system. After the ML model generates an output, the host system delivers that production to the data endpoints. 

Data destinations – are the locations to which the host system should send the ML model’s output score. An endpoint can be any form of data storage, from which downstream applications act on the scores. 

## Deployment Strategies 

Deployment strategies are methodologies to replaces older versions of applications with newer version whilst minimising application downtime and rollback risk. 

### Blue/Green Deployment 

Blue/Green Deployment (also known as Red/Black Deployment) strategy is a deployment strategy in which two separate, yet identical environments are created and deployed to the user. The blue (current) environment is the current version of the application whilst the green (new) environment is the new application version. Users will be gradually relocated onto the green environment as other users will still be using the blue environment. 

One benefit of Blue/Green Deployment is that as the blue environment remains in deployment, if the green environment encounters any step-backs or is pulled from production, the blue environment will be on standby to completely replace the green environment. This results in reduced deployment risk as it simplifies the rollback if deployment fails. Another benefit is that it reduces the downtime during application updates, further mitigating the risk surrounding downtime and rollback functionality. 

### A/B Deployment 

A/B deployment is a variant of Blue/Green deployment where the new version of the application can be test on in a limited production environment. Here, the stable version will get most of the user request while the new version will get some of the user request. 

As testing progress, if the product does not experience many issues, more users can be deployed on the new version. This continues until the stable version is ultimately replaced by the new version. 

By implementing this strategy, new features can be experimented upon a subset of the general userbase to gather reactions to the changes. 

For this method to be effective, both version must be able to run simultaneously. 

### All-At-Once Deployment 

In All-At-Once Deployment, all traffic and users will be transferred immediately from the old environment to the new environment. 

This deployment strategy may be preferred if there may be a security update to the application. by forcing everyone to update their versions simultaneously, one can get rid of all security risk and therefore ensure that their product is safe. However, if there is a bug or issue with the new version, re-deploying the previously version can increase application downtime. 

### Canary Deployment 

During Canary Deployment, the new version is incrementally released to new users gradually. These new features will continue to replace old features after being tested. As trust and insurance grows in the deployment, the new version will eventually replace the current version in its entirety. 

If at any point a new feature/implementation fails during testing, the feature can be immediately rolled back and be worked upon. 

Canary deployment strategies are particularly useful when there should be little downtime during an application update and when the application can support both the old code and new code being deployed on production. 

### Linear Deployment 

Linear Deployment is the process of shifting traffic in equal increments with an equal number of minutes between increments between versions. 

### In-Place Deployment 
