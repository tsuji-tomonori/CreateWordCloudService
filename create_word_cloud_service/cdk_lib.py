from collections.abc import Callable
from inspect import signature
from typing import NamedTuple

import aws_cdk as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from constructs import Construct


def set_tags(func: Callable):
    def wrapper(self, *args, **kwargs) -> None:
        # もととなるメソッド呼び出しリソースを作成
        result = func(self, *args, **kwargs)
        # メソッド呼び出しの引数から「resource_name」を取得
        sig = signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        resource_name = bound_args.arguments.get("resource_name")
        if resource_name is None:
            raise TypeError("デコレーターの対象となるメソッドの引数に「resource_name」がありません")
        # 作成したリソースにタグを付与
        cdk.Tags.of(result).add("project", self._param.project_name)
        cdk.Tags.of(result).add("resource", resource_name)
        cdk.Tags.of(result).add("creator", "cdk")
        cdk.Tags.of(result).add("usetype", self._param.usetype)
        return result
    return wrapper


class AwsStackParam(NamedTuple):
    core_service_name: str
    description: str
    project_name: str
    usetype: str


class LayerParam(NamedTuple):
    core_layer_name: str
    description: str


class InitializeException(AttributeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AwsCdkBase:
    def __init__(self, scope: Construct, param: AwsStackParam) -> None:
        self._scope = scope
        self._param = param

    def _build_resource_name(self, resource_name: str, service_name: str) -> str:
        return f"{resource_name}_{service_name}_cdk"


class LambdaBuilder(AwsCdkBase):
    def __init__(self, scope: Construct, param: AwsStackParam) -> None:
        super().__init__(scope, param)
        self.role = None
        self.fn = None
        self.log = None
        self.layer = []

    def build(self) -> None:
        self.role = self._create_role_base()
        self.fn = self._create_lambda_base()
        self.log = self._create_logs_base()

    def _create_role_base(self) -> iam.Role:
        service_name = f"{self._param.core_service_name}_role"
        resource_name = self._build_resource_name("rol", service_name)
        result = self._create_role(resource_name)
        return result

    @ set_tags
    def _create_role(self, resource_name: str):
        return iam.Role(
            self._scope, resource_name,
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole")
            ],
            role_name=resource_name,
            description=self._param.description
        )

    def _create_lambda_base(self) -> _lambda.Function:
        if self.role is None:
            raise InitializeException("Lambda roleが作成されていません")
        resource_name = self._build_lambda_name()
        result = self._create_lambda(resource_name)
        cdk.Tags.of(result).add("resource_name", resource_name)
        return result

    @ set_tags
    def _create_lambda(self, resource_name: str):
        return _lambda.DockerImageFunction(
            self._scope, resource_name,
            code=_lambda.DockerImageCode.from_image_asset(
                directory="lambda",
            ),
            function_name=resource_name,
            environment={
                "LOG_LEVEL": "INFO",
            },
            description=self._param.description,
            timeout=cdk.Duration.seconds(300),
            memory_size=256,
            role=self.role,
        )

    def _build_lambda_name(self):
        service_name = f"{self._param.core_service_name}_service"
        resource_name = self._build_resource_name("lmd", service_name)
        return resource_name

    def _create_logs_base(self) -> logs.LogGroup:
        if self.fn is None:
            raise InitializeException("Lambda 関数が作成されていません")
        loggroup_name = f"/aws/lambda/{self._build_lambda_name()}"
        result = self._create_logs(loggroup_name)
        return result

    @set_tags
    def _create_logs(self, resource_name: str):
        return logs.LogGroup(
            self._scope, resource_name,
            log_group_name=resource_name,
            retention=logs.RetentionDays.THREE_MONTHS,
        )

    def add_layer(self, param: LayerParam) -> None:
        self.layer.append(self._create_layer(param))

    def _create_layer(self, param: LayerParam) -> _lambda.LayerVersion:
        if self.fn is None:
            raise InitializeException("Lambda 関数が作成されていません")
        service_name = f"{self._param.core_service_name}_{param.core_layer_name}_layer"
        resource_name = self._build_resource_name("lyr", service_name)
        layer = _lambda.LayerVersion(
            self._scope, resource_name,
            code=_lambda.Code.from_asset(
                f"layer/{param.core_layer_name}"),
            layer_version_name=resource_name,
            description=param.description
        )
        self.fn.add_layers(layer)
        return layer


class S3Builder(AwsCdkBase):
    def __init__(self, scope: Construct, param: AwsStackParam) -> None:
        super().__init__(scope, param)

    def build(self) -> None:
        self.bucket = self._create_s3_base()

    def _create_s3_base(self) -> s3.Bucket:
        service_name = f"{self._param.core_service_name}_bucket"
        resource_name = self._build_resource_name(
            "s3s", service_name).replace("_", "-")
        print(resource_name)
        return self._create_s3(resource_name)

    @set_tags
    def _create_s3(self, resource_name: str) -> s3.Bucket:
        return s3.Bucket(
            self._scope, resource_name,
            bucket_name=resource_name,
        )
