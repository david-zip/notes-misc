# SageMaker Notes

Amazon SageMaker is a fully managed machine learing service. Users can quickly build and train machine learning models and deploy then instantaneously to a production environment. Built-in training algorithms are provided along with the framework to build your own.

Amazon SageMaker notebook instance is a fully managed machine learning EC2 compute instance that runs ina a Juypter Notebook. SageMaker Studios can be used to manage all notebook instances amd allocated computing power without needing to manage servers.

## Overview of SageMaker Machine Learning Process

1. Generate data
    - Data is require to train any model but before using the data for training, it must be:
        - Fetch
            - Data must be retrived either in-house or via an API call
        - Clean
            - Ensures proper and adequate training of model
        - Transform
            - Some data transformation must be applied to improved training performance
2. Train the model
    - Model can be trained using a training algorithm (eg. stochasitic search algorithms, gradient descent algorithms, random forest, etc.)
    - Choice of algorithm will depend on business case
    - Once model is trained, it must be evaluated to determine whether the accuracy is acceptable or not
3. Deploy the model
    - Typically the model would be integrated into an application before deployment but SageMaker allows for independent deployment

## Experiments

Experimenting is the process of varying certain hyperparameters and evaluating how it affects the output. SageMaker Experiments automatically tracks all inputs, parameters, configurations, and results of an iteration (run). These runs can be grouped into an experiment to be compared.


### Run Class
Experiments can be initialised as shown below:
```py
with Run(
    experiment_name='str',
    run_name='str',
    experiment_display_name='str',
    run_display_name='str',
    tags=list(dict('str', 'str')),
    sagemaker_session=class,
    artifact_bucket='str',
    artifact_prefix='str'
) as run
```
where:
- **experiment_name (string)**: unique name of experiment
- **run_name (string)**: name of run (randomly generated if not provided)
- **run_display_name (string)**: display name shown in the Experiment UI
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (one is created if not specified)
- **artifact_bucket (string)**: S3 bucket to upload artifacts 

### Experiment Class
An Amazon SageMaker experiment is a collection of related trials. New experiments are created by calling `experiments.experiments.Experiment.create`. 

Old experiments can be recalled using `experiments.experiments.Experiment.load`. 

```py
sagemaker.experiments.Experiment(
    sagemaker_session=class,
    {
        experiment_name='str',
        display_name='str',
        description='str',
        tags=list(dict('str','str'))
    }
)
```
where:
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)
- **experiment_name (string)**: unique name of experiment
- **display_name (string)**: display name of experimentshown in the Experiment UI
- **description (string)**: description of the experiment
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)

Below are a collection of the `Experiment` class methods.

```py
save()
```
Save the current state of the experiment to SageMaker. Returns a dictionary.

```py
delete()
```
Deletes the experiment from SageMaker. Deleted experiments do not delete any associated Trials and their Trial components. It requires ech Trial in the experiment to be deleted first. Returns a dictionary.

```py
load(
    experiment_name='str',
    sagemaker_session=class
)
```
Load an existing experiment and returns an experiment object representing it.

Parameters:
- **experiment_name (string)**: unique name of experiment
- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)

```py
create(
    experiment_name='str',
    display_name='str',
    description='str',
    tags=list(dict('str','str')),
    sagemaker_session=class
)
```
Creates a new experiment in SageMaker and return an experiment object.

Parameters:
- **experiment_name (string)**: unique name of experiment
- **display_name (string)**: display name of experimentshown in the Experiment UI (default: `None`)
- **description (string)**: description of the experiment (default: `None`)
- **tags (list[dictionary{string, string}])**: list of tags to create calls (default: `None`)

- **sagemaker_session (`sagemaker.session.Session`)**: Session object which manages interactions with the Amazon SageMaker API (default: `None`)

```py
list_trials(
    created_before=datetime,
    created_after=datetime,
    sort_by='str',
    sort_order='str'
)
```
List trials in the experiment matching specified criteria.

Parameters:
- **created_before (datetime.datetime)**: return trials created before this instant (default: `None`)
- **created_after (datetime.datetime)**: return trials created after this instant (default: `None`)
- **sort_by (string)**: sort by either `Name` or `CreationTime` (default: `None`)
- **sort_order (string)**: sort by either `Ascending` or `Descending` (default: `None`)

## Built-In Algorithms

### Tabular
#### AutoGluon
#### CatBoost
#### Factorization Machines
#### K-Nearest Neighbours
#### LightGBM
#### LinearLearner
#### TabTransformer
#### XGBoost

## SageMaker Library

## SageMaker Pipelines

The addition of pipelines into SageMaker has 

### Step-by-Step Guide to Creating a SageMaker CI/CD Pipeline

1. How to create a studio instance and user

2. How to define pipeline parameter

3. How to code the processing step

4. How to train your model

5. How to code the processing step to evaluate the models

