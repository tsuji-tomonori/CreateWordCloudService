from pathlib import Path
from aws_cdk import Stack
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_notifications as s3n
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct

from create_word_cloud_service.cdk_lib import (AwsStackParam, LambdaBuilder,
                                               LayerParam, S3Builder)


class CreateWordCloudServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        param = AwsStackParam(
            core_service_name="create_word_cloud",
            description="Create Word Cloud img.",
            project_name="CreateWordClooudService",
            usetype="service"
        )

        create_word_cloud_service = LambdaBuilder(
            self,
            param
        )
        create_word_cloud_service.build()

        layer_names = [x.name for x in (
            Path.cwd() / "layer").iterdir() if x.is_dir()]

        for layer_name in layer_names:
            create_word_cloud_service.add_layer(
                LayerParam(
                    layer_name,
                    f"create cdk {layer_name}"
                )
            )

        input_bucket = s3.Bucket.from_bucket_name(
            self, "s3s-file-output-bucket-cdk",
            "s3s-file-output-bucket-cdk"
        )
        input_bucket.grant_read(create_word_cloud_service.role)
        input_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(create_word_cloud_service.fn),
        )

        output_bucket = S3Builder(
            self,
            param,
        )
        output_bucket.build()
        output_bucket.bucket.grant_put(create_word_cloud_service.role)
        create_word_cloud_service.fn.add_environment(
            key="OUTPUT_BUCKET_NAME",
            value=output_bucket.bucket.bucket_name
        )

        create_word_cloud_service.fn.add_environment(
            key="FONT_PATH",
            value="fonts/ttf/ShipporiAntique-Regular.ttf"
        )
