import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8
from ..stack import (
    BaseStack as _BaseStack_8603347c, BaseStackProps as _BaseStackProps_bfec638c
)


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.newrelic.CfnMetricStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_filters": "excludeFilters",
        "include_filters": "includeFilters",
    },
)
class CfnMetricStreamProps:
    def __init__(
        self,
        *,
        exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param exclude_filters: 
        :param include_filters: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6d20bbd3f7853ec725446e0e0bdc01a91d551e3b6b6403d48344fb0cac184f)
            check_type(argname="argument exclude_filters", value=exclude_filters, expected_type=type_hints["exclude_filters"])
            check_type(argname="argument include_filters", value=include_filters, expected_type=type_hints["include_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_filters is not None:
            self._values["exclude_filters"] = exclude_filters
        if include_filters is not None:
            self._values["include_filters"] = include_filters

    @builtins.property
    def exclude_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty]]]]:
        result = self._values.get("exclude_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty]]]], result)

    @builtins.property
    def include_filters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty]]]]:
        result = self._values.get("include_filters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="neulabs-cdk-constructs.newrelic.EndpointType")
class EndpointType(enum.Enum):
    METRICS = "METRICS"
    LOGS = "LOGS"


@jsii.enum(jsii_type="neulabs-cdk-constructs.newrelic.EndpointUrlLogs")
class EndpointUrlLogs(enum.Enum):
    EU_LOGS = "EU_LOGS"
    US_LOGS = "US_LOGS"


@jsii.enum(jsii_type="neulabs-cdk-constructs.newrelic.EndpointUrlMetrics")
class EndpointUrlMetrics(enum.Enum):
    EU_METRICS = "EU_METRICS"
    US_METRICS = "US_METRICS"


class NewRelicStack(
    _BaseStack_8603347c,
    metaclass=jsii.JSIIMeta,
    jsii_type="neulabs-cdk-constructs.newrelic.NewRelicStack",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        new_relic_account_id: builtins.str,
        new_relic_bucket_name: builtins.str,
        new_relic_license_key: builtins.str,
        buffery_hints: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric_stream_props: typing.Optional[typing.Union[CfnMetricStreamProps, typing.Dict[builtins.str, typing.Any]]] = None,
        new_relic_api_url_logs: typing.Optional[EndpointUrlLogs] = None,
        new_relic_api_url_metrics: typing.Optional[EndpointUrlMetrics] = None,
        stage: builtins.str,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param new_relic_account_id: 
        :param new_relic_bucket_name: 
        :param new_relic_license_key: 
        :param buffery_hints: 
        :param cloudwatch_metric_stream_props: 
        :param new_relic_api_url_logs: 
        :param new_relic_api_url_metrics: 
        :param stage: 
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d16994fa6098e1a11bee3003bb87e23e040f04cdc0edc42f729eccb764b26ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NewRelicStackProps(
            new_relic_account_id=new_relic_account_id,
            new_relic_bucket_name=new_relic_bucket_name,
            new_relic_license_key=new_relic_license_key,
            buffery_hints=buffery_hints,
            cloudwatch_metric_stream_props=cloudwatch_metric_stream_props,
            new_relic_api_url_logs=new_relic_api_url_logs,
            new_relic_api_url_metrics=new_relic_api_url_metrics,
            stage=stage,
            analytics_reporting=analytics_reporting,
            cross_region_references=cross_region_references,
            description=description,
            env=env,
            permissions_boundary=permissions_boundary,
            stack_name=stack_name,
            suppress_template_indentation=suppress_template_indentation,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createCloudwatchLogsStreamRole")
    def create_cloudwatch_logs_stream_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createCloudwatchLogsStreamRole", []))

    @jsii.member(jsii_name="createCloudwatchMetricStream")
    def create_cloudwatch_metric_stream(
        self,
        firehose_arn: builtins.str,
        *,
        exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream:
        '''
        :param firehose_arn: -
        :param exclude_filters: 
        :param include_filters: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5773e82050fc71ec7adaea596012c6633e76c642a3debe22d934aa0706495f65)
            check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
        props = CfnMetricStreamProps(
            exclude_filters=exclude_filters, include_filters=include_filters
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream, jsii.invoke(self, "createCloudwatchMetricStream", [firehose_arn, props]))

    @jsii.member(jsii_name="createFirehoseBucket")
    def create_firehose_bucket(
        self,
        new_relic_bucket_name: builtins.str,
    ) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''
        :param new_relic_bucket_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__293b2457a5464a82a7b9803bc92a5b11e65e07b096a59d01d32e5d5aeb5758de)
            check_type(argname="argument new_relic_bucket_name", value=new_relic_bucket_name, expected_type=type_hints["new_relic_bucket_name"])
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.invoke(self, "createFirehoseBucket", [new_relic_bucket_name]))

    @jsii.member(jsii_name="createFirehoseRole")
    def create_firehose_role(
        self,
        new_relic_firehose_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param new_relic_firehose_bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfa6a835034d382ecc291b7960d75dc926758335729c5c5c87a3df26e9fbc42)
            check_type(argname="argument new_relic_firehose_bucket", value=new_relic_firehose_bucket, expected_type=type_hints["new_relic_firehose_bucket"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createFirehoseRole", [new_relic_firehose_bucket]))

    @jsii.member(jsii_name="createFirehoseStream")
    def create_firehose_stream(
        self,
        new_relic_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        endpoint_type: EndpointType,
        endpoint_url: builtins.str,
        new_relic_license_ley: builtins.str,
        *,
        interval_in_seconds: typing.Optional[jsii.Number] = None,
        size_in_m_bs: typing.Optional[jsii.Number] = None,
    ) -> _aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream:
        '''
        :param new_relic_bucket: -
        :param role: -
        :param endpoint_type: -
        :param endpoint_url: -
        :param new_relic_license_ley: -
        :param interval_in_seconds: The length of time, in seconds, that Kinesis Data Firehose buffers incoming data before delivering it to the destination. For valid values, see the ``IntervalInSeconds`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
        :param size_in_m_bs: The size of the buffer, in MBs, that Kinesis Data Firehose uses for incoming data before delivering it to the destination. For valid values, see the ``SizeInMBs`` content for the `BufferingHints <https://docs.aws.amazon.com/firehose/latest/APIReference/API_BufferingHints.html>`_ data type in the *Amazon Kinesis Data Firehose API Reference* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a8c6006513a8211068ba90e3161ed414e09ab40b8b39a6df5b69eda0c7580b)
            check_type(argname="argument new_relic_bucket", value=new_relic_bucket, expected_type=type_hints["new_relic_bucket"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument endpoint_url", value=endpoint_url, expected_type=type_hints["endpoint_url"])
            check_type(argname="argument new_relic_license_ley", value=new_relic_license_ley, expected_type=type_hints["new_relic_license_ley"])
        buffering_hints = _aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty(
            interval_in_seconds=interval_in_seconds, size_in_m_bs=size_in_m_bs
        )

        return typing.cast(_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream, jsii.invoke(self, "createFirehoseStream", [new_relic_bucket, role, endpoint_type, endpoint_url, new_relic_license_ley, buffering_hints]))

    @jsii.member(jsii_name="createNewRelicRole")
    def create_new_relic_role(
        self,
        new_relic_account_id: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''
        :param new_relic_account_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2ce9d7e6b30b79bf03d30143ef0ab44dace126e3cf4fe6416410a87bd7adb9)
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.invoke(self, "createNewRelicRole", [new_relic_account_id]))

    @jsii.member(jsii_name="createSecrets")
    def create_secrets(
        self,
        new_relic_account_id: builtins.str,
        new_relic_license_ley: builtins.str,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.Secret:
        '''
        :param new_relic_account_id: -
        :param new_relic_license_ley: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9207c4cf652dd32e1982552a337d2c6ee4feec21293e5d142637f19f7d15f3a8)
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
            check_type(argname="argument new_relic_license_ley", value=new_relic_license_ley, expected_type=type_hints["new_relic_license_ley"])
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.Secret, jsii.invoke(self, "createSecrets", [new_relic_account_id, new_relic_license_ley]))

    @builtins.property
    @jsii.member(jsii_name="newRelicBucket")
    def new_relic_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "newRelicBucket"))

    @new_relic_bucket.setter
    def new_relic_bucket(self, value: _aws_cdk_aws_s3_ceddda9d.IBucket) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a50c8dc84366507632494f10d58f67e1091f40c52854003fae935854f6531d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicBucket", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseRole")
    def new_relic_firehose_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "newRelicFirehoseRole"))

    @new_relic_firehose_role.setter
    def new_relic_firehose_role(self, value: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e8c6d495785af865a26845a47ed746ae3e1fee7de9da3764cf516e17c4e684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicIntegrationRole")
    def new_relic_integration_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "newRelicIntegrationRole"))

    @new_relic_integration_role.setter
    def new_relic_integration_role(
        self,
        value: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ca0ea0cd3f3616c2179a54cf735a2d37122b82c41398eec2891ef2fa698bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicIntegrationRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicSecret")
    def new_relic_secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "newRelicSecret"))

    @new_relic_secret.setter
    def new_relic_secret(
        self,
        value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c472c90902e049b6a42940d42ae6cef79723eda5f3ce524a30c9a15dd0adcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicSecret", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicCloudwatchLogsStreamRole")
    def new_relic_cloudwatch_logs_stream_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "newRelicCloudwatchLogsStreamRole"))

    @new_relic_cloudwatch_logs_stream_role.setter
    def new_relic_cloudwatch_logs_stream_role(
        self,
        value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d7723a7d99349ba3576fa9bf229bf874cc36485f27a88ad69aefda9bbc2282)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicCloudwatchLogsStreamRole", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseLogs")
    def new_relic_firehose_logs(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream], jsii.get(self, "newRelicFirehoseLogs"))

    @new_relic_firehose_logs.setter
    def new_relic_firehose_logs(
        self,
        value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6418b5fbf4f90a7918374905169359a2830a7d6a1d2255582d84e39ce47a1a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseLogs", value)

    @builtins.property
    @jsii.member(jsii_name="newRelicFirehoseMetrics")
    def new_relic_firehose_metrics(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream], jsii.get(self, "newRelicFirehoseMetrics"))

    @new_relic_firehose_metrics.setter
    def new_relic_firehose_metrics(
        self,
        value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931c517602897fd81019537fc68431f31f8a2fa16ffd611b69094e837d87ef05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newRelicFirehoseMetrics", value)


@jsii.data_type(
    jsii_type="neulabs-cdk-constructs.newrelic.NewRelicStackProps",
    jsii_struct_bases=[_BaseStackProps_bfec638c],
    name_mapping={
        "analytics_reporting": "analyticsReporting",
        "cross_region_references": "crossRegionReferences",
        "description": "description",
        "env": "env",
        "permissions_boundary": "permissionsBoundary",
        "stack_name": "stackName",
        "suppress_template_indentation": "suppressTemplateIndentation",
        "synthesizer": "synthesizer",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "stage": "stage",
        "new_relic_account_id": "newRelicAccountId",
        "new_relic_bucket_name": "newRelicBucketName",
        "new_relic_license_key": "newRelicLicenseKey",
        "buffery_hints": "bufferyHints",
        "cloudwatch_metric_stream_props": "cloudwatchMetricStreamProps",
        "new_relic_api_url_logs": "newRelicApiUrlLogs",
        "new_relic_api_url_metrics": "newRelicApiUrlMetrics",
    },
)
class NewRelicStackProps(_BaseStackProps_bfec638c):
    def __init__(
        self,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        cross_region_references: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        stack_name: typing.Optional[builtins.str] = None,
        suppress_template_indentation: typing.Optional[builtins.bool] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        stage: builtins.str,
        new_relic_account_id: builtins.str,
        new_relic_bucket_name: builtins.str,
        new_relic_license_key: builtins.str,
        buffery_hints: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_metric_stream_props: typing.Optional[typing.Union[CfnMetricStreamProps, typing.Dict[builtins.str, typing.Any]]] = None,
        new_relic_api_url_logs: typing.Optional[EndpointUrlLogs] = None,
        new_relic_api_url_metrics: typing.Optional[EndpointUrlMetrics] = None,
    ) -> None:
        '''
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param cross_region_references: Enable this flag to allow native cross region stack references. Enabling this will create a CloudFormation custom resource in both the producing stack and consuming stack in order to perform the export/import This feature is currently experimental Default: false
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param suppress_template_indentation: Enable this flag to suppress indentation in generated CloudFormation templates. If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation`` context key will be used. If that is not specified, then the default value ``false`` will be used. Default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        :param synthesizer: Synthesis method to use while deploying this stack. The Stack Synthesizer controls aspects of synthesis and deployment, like how assets are referenced and what IAM roles to use. For more information, see the README of the main CDK package. If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used. If that is not specified, ``DefaultStackSynthesizer`` is used if ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no other synthesizer is specified. Default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param stage: 
        :param new_relic_account_id: 
        :param new_relic_bucket_name: 
        :param new_relic_license_key: 
        :param buffery_hints: 
        :param cloudwatch_metric_stream_props: 
        :param new_relic_api_url_logs: 
        :param new_relic_api_url_metrics: 
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if isinstance(buffery_hints, dict):
            buffery_hints = _aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty(**buffery_hints)
        if isinstance(cloudwatch_metric_stream_props, dict):
            cloudwatch_metric_stream_props = CfnMetricStreamProps(**cloudwatch_metric_stream_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b73444472d0b16a38d845ab8c4feabeadd9937eadb9c68ca1f7a002e868c7df)
            check_type(argname="argument analytics_reporting", value=analytics_reporting, expected_type=type_hints["analytics_reporting"])
            check_type(argname="argument cross_region_references", value=cross_region_references, expected_type=type_hints["cross_region_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument suppress_template_indentation", value=suppress_template_indentation, expected_type=type_hints["suppress_template_indentation"])
            check_type(argname="argument synthesizer", value=synthesizer, expected_type=type_hints["synthesizer"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument new_relic_account_id", value=new_relic_account_id, expected_type=type_hints["new_relic_account_id"])
            check_type(argname="argument new_relic_bucket_name", value=new_relic_bucket_name, expected_type=type_hints["new_relic_bucket_name"])
            check_type(argname="argument new_relic_license_key", value=new_relic_license_key, expected_type=type_hints["new_relic_license_key"])
            check_type(argname="argument buffery_hints", value=buffery_hints, expected_type=type_hints["buffery_hints"])
            check_type(argname="argument cloudwatch_metric_stream_props", value=cloudwatch_metric_stream_props, expected_type=type_hints["cloudwatch_metric_stream_props"])
            check_type(argname="argument new_relic_api_url_logs", value=new_relic_api_url_logs, expected_type=type_hints["new_relic_api_url_logs"])
            check_type(argname="argument new_relic_api_url_metrics", value=new_relic_api_url_metrics, expected_type=type_hints["new_relic_api_url_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
            "new_relic_account_id": new_relic_account_id,
            "new_relic_bucket_name": new_relic_bucket_name,
            "new_relic_license_key": new_relic_license_key,
        }
        if analytics_reporting is not None:
            self._values["analytics_reporting"] = analytics_reporting
        if cross_region_references is not None:
            self._values["cross_region_references"] = cross_region_references
        if description is not None:
            self._values["description"] = description
        if env is not None:
            self._values["env"] = env
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if suppress_template_indentation is not None:
            self._values["suppress_template_indentation"] = suppress_template_indentation
        if synthesizer is not None:
            self._values["synthesizer"] = synthesizer
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if buffery_hints is not None:
            self._values["buffery_hints"] = buffery_hints
        if cloudwatch_metric_stream_props is not None:
            self._values["cloudwatch_metric_stream_props"] = cloudwatch_metric_stream_props
        if new_relic_api_url_logs is not None:
            self._values["new_relic_api_url_logs"] = new_relic_api_url_logs
        if new_relic_api_url_metrics is not None:
            self._values["new_relic_api_url_metrics"] = new_relic_api_url_metrics

    @builtins.property
    def analytics_reporting(self) -> typing.Optional[builtins.bool]:
        '''Include runtime versioning information in this Stack.

        :default:

        ``analyticsReporting`` setting of containing ``App``, or value of
        'aws:cdk:version-reporting' context key
        '''
        result = self._values.get("analytics_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cross_region_references(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to allow native cross region stack references.

        Enabling this will create a CloudFormation custom resource
        in both the producing stack and consuming stack in order to perform the export/import

        This feature is currently experimental

        :default: false
        '''
        result = self._values.get("cross_region_references")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the stack.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.

        Set the ``region``/``account`` fields of ``env`` to either a concrete value to
        select the indicated environment (recommended for production stacks), or to
        the values of environment variables
        ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment
        depend on the AWS credentials/configuration that the CDK CLI is executed
        under (recommended for development stacks).

        If the ``Stack`` is instantiated inside a ``Stage``, any undefined
        ``region``/``account`` fields from ``env`` will default to the same field on the
        encompassing ``Stage``, if configured there.

        If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the
        Stack will be considered "*environment-agnostic*"". Environment-agnostic
        stacks can be deployed to any environment but may not be able to take
        advantage of all features of the CDK. For example, they will not be able to
        use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not
        automatically translate Service Principals to the right format based on the
        environment's AWS partition, and other such enhancements.

        :default:

        - The environment of the containing ``Stage`` if available,
        otherwise create the stack will be environment-agnostic.

        Example::

            // Use a concrete account and region to deploy this stack to:
            // `.account` and `.region` will simply return these values.
            new Stack(app, 'Stack1', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              },
            });
            
            // Use the CLI's current credentials to determine the target environment:
            // `.account` and `.region` will reflect the account+region the CLI
            // is configured to use (based on the user CLI credentials)
            new Stack(app, 'Stack2', {
              env: {
                account: process.env.CDK_DEFAULT_ACCOUNT,
                region: process.env.CDK_DEFAULT_REGION
              },
            });
            
            // Define multiple stacks stage associated with an environment
            const myStage = new Stage(app, 'MyStage', {
              env: {
                account: '123456789012',
                region: 'us-east-1'
              }
            });
            
            // both of these stacks will use the stage's account/region:
            // `.account` and `.region` will resolve to the concrete values as above
            new MyStack(myStage, 'Stack1');
            new YourStack(myStage, 'Stack2');
            
            // Define an environment-agnostic stack:
            // `.account` and `.region` will resolve to `{ "Ref": "AWS::AccountId" }` and `{ "Ref": "AWS::Region" }` respectively.
            // which will only resolve to actual values by CloudFormation during deployment.
            new MyStack(app, 'Stack1');
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''Name to deploy the stack with.

        :default: - Derived from construct path.
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress_template_indentation(self) -> typing.Optional[builtins.bool]:
        '''Enable this flag to suppress indentation in generated CloudFormation templates.

        If not specified, the value of the ``@aws-cdk/core:suppressTemplateIndentation``
        context key will be used. If that is not specified, then the
        default value ``false`` will be used.

        :default: - the value of ``@aws-cdk/core:suppressTemplateIndentation``, or ``false`` if that is not set.
        '''
        result = self._values.get("suppress_template_indentation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synthesizer(self) -> typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer]:
        '''Synthesis method to use while deploying this stack.

        The Stack Synthesizer controls aspects of synthesis and deployment,
        like how assets are referenced and what IAM roles to use. For more
        information, see the README of the main CDK package.

        If not specified, the ``defaultStackSynthesizer`` from ``App`` will be used.
        If that is not specified, ``DefaultStackSynthesizer`` is used if
        ``@aws-cdk/core:newStyleStackSynthesis`` is set to ``true`` or the CDK major
        version is v2. In CDK v1 ``LegacyStackSynthesizer`` is the default if no
        other synthesizer is specified.

        :default: - The synthesizer specified on ``App``, or ``DefaultStackSynthesizer`` otherwise.
        '''
        result = self._values.get("synthesizer")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Stack tags that will be applied to all the taggable resources and the stack itself.

        :default: {}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable termination protection for this stack.

        :default: false
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> builtins.str:
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_account_id(self) -> builtins.str:
        result = self._values.get("new_relic_account_id")
        assert result is not None, "Required property 'new_relic_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_bucket_name(self) -> builtins.str:
        result = self._values.get("new_relic_bucket_name")
        assert result is not None, "Required property 'new_relic_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_relic_license_key(self) -> builtins.str:
        result = self._values.get("new_relic_license_key")
        assert result is not None, "Required property 'new_relic_license_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def buffery_hints(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty]:
        result = self._values.get("buffery_hints")
        return typing.cast(typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty], result)

    @builtins.property
    def cloudwatch_metric_stream_props(self) -> typing.Optional[CfnMetricStreamProps]:
        result = self._values.get("cloudwatch_metric_stream_props")
        return typing.cast(typing.Optional[CfnMetricStreamProps], result)

    @builtins.property
    def new_relic_api_url_logs(self) -> typing.Optional[EndpointUrlLogs]:
        result = self._values.get("new_relic_api_url_logs")
        return typing.cast(typing.Optional[EndpointUrlLogs], result)

    @builtins.property
    def new_relic_api_url_metrics(self) -> typing.Optional[EndpointUrlMetrics]:
        result = self._values.get("new_relic_api_url_metrics")
        return typing.cast(typing.Optional[EndpointUrlMetrics], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NewRelicStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMetricStreamProps",
    "EndpointType",
    "EndpointUrlLogs",
    "EndpointUrlMetrics",
    "NewRelicStack",
    "NewRelicStackProps",
]

publication.publish()

def _typecheckingstub__ac6d20bbd3f7853ec725446e0e0bdc01a91d551e3b6b6403d48344fb0cac184f(
    *,
    exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d16994fa6098e1a11bee3003bb87e23e040f04cdc0edc42f729eccb764b26ca(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    new_relic_account_id: builtins.str,
    new_relic_bucket_name: builtins.str,
    new_relic_license_key: builtins.str,
    buffery_hints: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_metric_stream_props: typing.Optional[typing.Union[CfnMetricStreamProps, typing.Dict[builtins.str, typing.Any]]] = None,
    new_relic_api_url_logs: typing.Optional[EndpointUrlLogs] = None,
    new_relic_api_url_metrics: typing.Optional[EndpointUrlMetrics] = None,
    stage: builtins.str,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5773e82050fc71ec7adaea596012c6633e76c642a3debe22d934aa0706495f65(
    firehose_arn: builtins.str,
    *,
    exclude_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_filters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_cloudwatch_ceddda9d.CfnMetricStream.MetricStreamFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293b2457a5464a82a7b9803bc92a5b11e65e07b096a59d01d32e5d5aeb5758de(
    new_relic_bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfa6a835034d382ecc291b7960d75dc926758335729c5c5c87a3df26e9fbc42(
    new_relic_firehose_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a8c6006513a8211068ba90e3161ed414e09ab40b8b39a6df5b69eda0c7580b(
    new_relic_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    endpoint_type: EndpointType,
    endpoint_url: builtins.str,
    new_relic_license_ley: builtins.str,
    *,
    interval_in_seconds: typing.Optional[jsii.Number] = None,
    size_in_m_bs: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2ce9d7e6b30b79bf03d30143ef0ab44dace126e3cf4fe6416410a87bd7adb9(
    new_relic_account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9207c4cf652dd32e1982552a337d2c6ee4feec21293e5d142637f19f7d15f3a8(
    new_relic_account_id: builtins.str,
    new_relic_license_ley: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a50c8dc84366507632494f10d58f67e1091f40c52854003fae935854f6531d(
    value: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e8c6d495785af865a26845a47ed746ae3e1fee7de9da3764cf516e17c4e684(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ca0ea0cd3f3616c2179a54cf735a2d37122b82c41398eec2891ef2fa698bf9(
    value: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c472c90902e049b6a42940d42ae6cef79723eda5f3ce524a30c9a15dd0adcf(
    value: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d7723a7d99349ba3576fa9bf229bf874cc36485f27a88ad69aefda9bbc2282(
    value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6418b5fbf4f90a7918374905169359a2830a7d6a1d2255582d84e39ce47a1a1e(
    value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931c517602897fd81019537fc68431f31f8a2fa16ffd611b69094e837d87ef05(
    value: typing.Optional[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b73444472d0b16a38d845ab8c4feabeadd9937eadb9c68ca1f7a002e868c7df(
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    cross_region_references: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    stack_name: typing.Optional[builtins.str] = None,
    suppress_template_indentation: typing.Optional[builtins.bool] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    stage: builtins.str,
    new_relic_account_id: builtins.str,
    new_relic_bucket_name: builtins.str,
    new_relic_license_key: builtins.str,
    buffery_hints: typing.Optional[typing.Union[_aws_cdk_aws_kinesisfirehose_ceddda9d.CfnDeliveryStream.BufferingHintsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_metric_stream_props: typing.Optional[typing.Union[CfnMetricStreamProps, typing.Dict[builtins.str, typing.Any]]] = None,
    new_relic_api_url_logs: typing.Optional[EndpointUrlLogs] = None,
    new_relic_api_url_metrics: typing.Optional[EndpointUrlMetrics] = None,
) -> None:
    """Type checking stubs"""
    pass
