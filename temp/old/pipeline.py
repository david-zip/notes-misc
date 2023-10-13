# import modules
import os
import boto3
import sagemaker

from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.model_metrics import (
    MetricsSource,
    ModelMetrics,
)
from sagemaker.processing import (
    ProcessingInput,
    ProcessingOutput,
    ScriptProcessor,
)
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.workflow.conditions import ConditionLessThanOrEqualTo
from sagemaker.workflow.condition_step import (
    ConditionStep,
)
from sagemaker.workflow.functions import (
    JsonGet,
)
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
)
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.steps import (
    ProcessingStep,
    TrainingStep,
)
from sagemaker.workflow.model_step import ModelStep
from sagemaker.model import Model
from sagemaker.workflow.pipeline_context import PipelineSession

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def define_pipeline(
    region,
    sagemaker_project_name=None,
    role=None,
    default_bucket=None,
    model_package_group_name="HousePricePackageGroup",
    pipeline_name="HousePricePipeline",
    base_job_prefix="HousePrice",
    processing_instance_type="ml.m5.xlarge",
    training_instance_type="ml.m5.xlarge",
    
):
    
    # initialise boto3 and sagemaker clients and sessions
    boto_session = boto3.Session(region_name=region)
    sagemaker_client = boto_session.client("sagemaker")
    runtime_client = boto_session.client("sagemaker-runtime")
    sagemaker_session = sagemaker.session.Session(
                            boto_session=boto_session,
                            sagemaker_client=sagemaker_client,
                            sagemaker_runtime_client=runtime_client,
                            default_bucket=default_bucket
                        )
    
    pipeline_session = PipelineSession(
        boto_session=boto_session,
        sagemaker_client=sagemaker_client,
        default_bucket=default_bucket
    )

    # get execution role for sagemaker
    if role is None:
        role = sagemaker.session.get_execution_role(sagemaker_session)
    
    ##############################################################################
    # define default parameters for pipeline execution
    processing_instance_count = ParameterInteger(
        name="ProcessingInstanceCount", 
        default_value=1
    )

    model_approval_status = ParameterString(
        name="ModelApprovalStatus", 
        default_value="PendingManualApproval"
    )
    
    input_data = ParameterString(
        name="InputDataUrl",
        default_value="s3://sagemaker-project-p-pvdjcw8fuq4v/dataset/Housing.csv",
    )
    ##############################################################################
    # preprocessing data (feature engineering)
    print("Preprocessing start")
    # initialise SKLearnProcessor
    sklearn_processor = SKLearnProcessor(
        framework_version="0.23-1",
        instance_type=processing_instance_type,
        instance_count=processing_instance_count,
        base_job_name=f"{base_job_prefix}/sklearn-house-preprocess",
        sagemaker_session=pipeline_session,
        role=role
    )

    step_args = sklearn_processor.run(
        outputs=[
            ProcessingOutput(
                output_name="train",
                source="/opt/ml/processing/train"
            ),
            ProcessingOutput(
                output_name="validation",
                source="/opt/ml/processing/validation"
            ),
            ProcessingOutput(
                output_name="test",
                source="/opt/ml/processing/test"
            )
        ],
        code=os.path.join(BASE_DIR, "preprocess.py"),
        arguments=["--input-data", input_data]
    )

    step_process = ProcessingStep(
        name="PreprocessingHousingPriceData",
        step_args=step_args
    )

    print("Preprocessing end")

    ##############################################################################
    # training step for training model
    print("Training start")
    model_path = f"s3://{sagemaker_session.default_bucket()}/{base_job_prefix}/HousePriceTrain"

    # initialise XGBoost training algorithm
    image_uri = sagemaker.image_uris.retrieve(
        framework="xgboost",
        region=region,
        version="1.0-1",
        py_version="py3",
        instance_type=training_instance_type,
    )
    
    xgb_train = Estimator(
        image_uri=image_uri,
        instance_type=training_instance_type,
        instance_count=1,
        output_path=model_path,
        base_job_name=f"{base_job_prefix}/house-price-train",
        sagemaker_session=pipeline_session,
        role=role
    )
    
    xgb_train.set_hyperparameters(
        objective="reg:linear",
        num_round=50,
        max_depth=5,
        eta=0.2,
        gamma=4,
        min_child_weight=6,
        subsample=0.7,
        silent=0
    )
    
    step_args = xgb_train.fit(
        inputs={
            "train": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                    "train"
                ].S3Output.S3Uri,
                content_type="text/csv"
            ),
            "validation": TrainingInput(
                s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                    "validation"
                ].S3Output.S3Uri,
                content_type="text/csv"
            )
        }
    )
    
    step_train = TrainingStep(
        name="TrainHousePriceModel",
        step_args=step_args
    )
    print("Training end")
    ###############################################################################
    # processing step for evaluating the model
    print("Evaluation start")
        
    script_eval = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        instance_type=processing_instance_type,
        instance_count=1,
        base_job_name=f"{base_job_prefix}/script-housing-price-eval",
        sagemaker_session=pipeline_session,
        role=role
    )
    
    step_args = script_eval.run(
        inputs=[
            ProcessingInput(
                source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
                destination="/opt/ml/processing/model",
            ),
            ProcessingInput(
                source=step_process.properties.ProcessingOutputConfig.Outputs[
                    "test"
                ].S3Output.S3Uri,
                destination="/opt/ml/processing/test"
            )
        ],
        outputs=[
            ProcessingOutput(
                output_name="evaluation",
                source="/opt/ml/processing/evaluation"
            )
        ],
        code=os.path.join(BASE_DIR, "evaluate.py")
    )
    
    evaluation_report = PropertyFile(
        name="HousePriceEvaluationReport",
        output_name="evaluation",
        path="evaluation.json"
    )
    
    step_eval = ProcessingStep(
        name="EvaluateHousePriceModel",
        step_args=step_args,
        property_files=[evaluation_report]
    )
    print("Evaluation end")
    ##################################################################################
    # register model to the model registry
    print("Model register start")
    
    model_metrics = ModelMetrics(
        model_statistics=MetricsSource(
            s3_uri="{}/evaluation.json".format(
                step_eval.arguments["ProcessingOutputConfig"]["Outputs"][0]["S3Output"]["S3Uri"]
            ),
            content_type="application/json"
        )
    )
    
    model = Model(
        image_uri=image_uri,
        model_data=step_train.properties.ModelArtifacts.S3ModelArtifacts,
        sagemaker_session=pipeline_session,
        role=role
    )
    
    step_args = model.register(
        content_types=["text/csv"],
        response_types=["text/csv"],
        inference_instances=["ml.t2.medium", "ml.m5.large"],
        transform_instances=["ml.m5.large"],
        model_package_group_name=model_package_group_name,
        approval_status=model_approval_status,
        model_metrics=model_metrics
    )
    
    step_register = ModelStep(
        name="RegisterHousePriceModel",
        step_args=step_args
    )
    
    print("Model register end")
    ################################################################################
    # condition step for evaluating whether the model should be registered
    cond_lte = ConditionLessThanOrEqualTo(
        left=JsonGet(
            step_name=step_eval.name,
            property_file=evaluation_report,
            json_path="regression_metrics.mse.value"
        ),
        right=6.0
    )
    step_cond = ConditionStep(
        name="CheckMSEHousePriceEvaluation",
        conditions=[cond_lte],
        if_steps=[step_register],
        else_steps=[]
    )

    ###############################################################################
    # initialise pipeline instance
    pipeline = Pipeline(
        name=pipeline_name,
        parameters=[
            processing_instance_type,
            processing_instance_count,
            training_instance_type,
            model_approval_status,
            input_data,
        ],
        steps=[step_process, step_train, step_eval, step_cond],
        sagemaker_session=pipeline_session,
    )
    return pipeline