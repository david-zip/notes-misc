# SageMaker Pipelines

SageMaker pipelines ae composed of various steps. Each step defines a set of procedures are that conducted to deploy a (well)trained machine learning model. 

## Processing Step

The processing step defines the processing jobs required to apply feature engineering to the dataset. A well-defined processing step requires a processor,  Python script that details the transformation actions, and job arguments.

```py
sagemaker.workflow.steps.ProcessingStep(
    name='str',
    step_args=JobStepArguments,
    processor=class,
    display_name='str'
)
```

## Training Step

Training step will create the training job to train the machine learning model. A training step requires an estimator, and the validation data inputs.

The algorithm that can be used to train the model can be one of the pre-defined built-in SageMaker training algorithms or custom-made algorithms.

Available training algorihtms

## Evaluation Step

The evaluation step does not exist in SageMaker. Instead, the evaluation procedure is defined in a `ProcessingStep` instance. 

## RegisterModel Step

`RegisterModel` step can be used to register a SageMaker model to the Amazon SageMaker model registry.