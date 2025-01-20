import sagemaker
import boto3
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.processing import ScriptProcessor
from sagemaker import get_execution_role, Session
from src.utils.helper import load_config


def create_sagemaker_pipeline(
    execution_role,
    sagemaker_session,
    input_data_uri,
    output_data_uri,
    model_output_uri,
    processing_instance_type='ml.t3.medium',
    training_instance_type='ml.t3.medium'
):
    """
    Create a SageMaker pipeline with preprocessing and training steps using ScriptProcessor.

    Args:
        execution_role (str): The execution role ARN for SageMaker.
        sagemaker_session (sagemaker.session.Session): The SageMaker session to use.
        input_data_uri (str): The S3 URI where the input data is stored.
        output_data_uri (str): The S3 URI where the processed data will be saved.
        model_output_uri (str): The S3 URI where the trained model artifacts will be stored.
        processing_instance_type (str, optional): The instance type for the preprocessing step. Defaults to 'ml.t3.medium'.
        training_instance_type (str, optional): The instance type for the training step. Defaults to 'ml.t3.medium'.

    Returns:
        Pipeline: A SageMaker pipeline object with preprocessing and training steps.

    Notes:
        - The pipeline consists of a preprocessing step that uses a custom Docker image with ScriptProcessor, followed by a training step.
        - The input data is processed in the preprocessing step and passed to the training step.
        - The pipeline is created with the provided execution role and session.
    """


    # Create a pipeline session
    pipeline_session = PipelineSession()

    # SageMaker coustom image URI
    image_uri = "750573229682.dkr.ecr.us-east-1.amazonaws.com/xgboost-sagemaker:latest"

    # ScriptProcessor for preprocessing 
    script_processor = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        role=execution_role,
        instance_type=processing_instance_type,
        instance_count=1,
        sagemaker_session=pipeline_session
    )

    # Preprocessing step
    processing_step = ProcessingStep(
        name='PreprocessIrisData',
        processor=script_processor,
        inputs=[
            ProcessingInput(
                source=input_data_uri,
                destination='/opt/ml/processing/input'
            )
        ],
        outputs=[
            ProcessingOutput(
                source='/opt/ml/processing/output',
                destination=output_data_uri,
                output_name='ProcessedData'
            )
        ],
        code='src/preprocessing.py'
    )

    # ScriptProcessor for training 
    training_processor = ScriptProcessor(
        image_uri=image_uri,
        command=["python3"],
        role=execution_role,
        instance_type=training_instance_type,
        instance_count=1,
        sagemaker_session=pipeline_session
    )

    # Training step
    training_step = ProcessingStep(
        name='TrainIrisModel',
        processor=training_processor,
        inputs=[
            ProcessingInput(
                source=processing_step.properties.ProcessingOutputConfig.Outputs['ProcessedData'].S3Output.S3Uri,
                destination='/opt/ml/processing/input/train'
            )
        ],
        outputs=[
            ProcessingOutput(
                source='/opt/ml/processing/output',
                destination=model_output_uri,
                output_name='ModelArtifacts'
            )
        ],
        code='src/train.py'
    )


    # Create pipeline
    pipeline = Pipeline(
        name='xgboost-mlflow-pipeline',
        steps=[processing_step],
        sagemaker_session=pipeline_session
    )

    return pipeline


def main():

    region_name = "us-east-1" 
    boto3.setup_default_session(region_name=region_name)
    sagemaker_session = Session()

    # execution_role = get_execution_role(sagemaker_session=sagemaker_session)
    execution_role = 'arn:aws:iam::750573229682:role/service-role/AmazonSageMaker-ExecutionRole-20241211T150457'
    
    config = load_config()
    s3 = config.get("s3", {}) 

    # S3 URIs for input and output data

    # input_data_uri = "s3://mlflow-sagemaker-us-east-1-750573229682/xgb_housing/inout_csv/"
    input_data_uri = s3.get("input_bucket_name") 
    # output_data_uri = "s3://mlflow-sagemaker-us-east-1-750573229682/xgb_housing/processed_csv/" 
    output_data_uri = s3.get("output_bucket_name")
    model_output_uri = "s3://mlflow-sagemaker-us-east-1-750573229682/xgb_housing/model/" 

 
    # Create pipeline
    pipeline = create_sagemaker_pipeline(
        execution_role,
        sagemaker_session,
        input_data_uri,
        output_data_uri,
        model_output_uri,
    )

    # Upsert pipeline
    pipeline.upsert(role_arn=execution_role)

    # Execute the pipeline
    execution = pipeline.start()

    # Wait for the pipeline to finish
    execution.wait()

    print("Pipeline execution completed.")
    print("Pipeline Execution Status:", execution.describe()['PipelineExecutionStatus'])


if __name__ == '__main__':
    main()

