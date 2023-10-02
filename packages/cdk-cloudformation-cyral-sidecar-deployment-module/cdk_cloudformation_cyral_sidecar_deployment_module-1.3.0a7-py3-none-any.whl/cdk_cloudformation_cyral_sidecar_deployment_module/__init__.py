'''
# cyral-sidecar-deployment-module

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Cyral::Sidecar::Deployment::MODULE` v1.3.0.

## Description

Schema for Module Fragment of type Cyral::Sidecar::Deployment::MODULE

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Cyral::Sidecar::Deployment::MODULE \
  --publisher-id fd1cb0d8eea619492a38da653b2e535d5b5f6410 \
  --type MODULE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/module/fd1cb0d8eea619492a38da653b2e535d5b5f6410/Cyral-Sidecar-Deployment-MODULE \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Cyral::Sidecar::Deployment::MODULE`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fcyral-sidecar-deployment-module+v1.3.0).
* Issues related to `Cyral::Sidecar::Deployment::MODULE` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnDeploymentModule(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModule",
):
    '''A CloudFormation ``Cyral::Sidecar::Deployment::MODULE``.

    :cloudformationResource: Cyral::Sidecar::Deployment::MODULE
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        parameters: typing.Optional[typing.Union["CfnDeploymentModulePropsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["CfnDeploymentModulePropsResources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Cyral::Sidecar::Deployment::MODULE``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param parameters: 
        :param resources: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0053a2f65c81e4364909e7bd4348b77a17a175ac0d1bfb8327e9d4bb7c0e43b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentModuleProps(parameters=parameters, resources=resources)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDeploymentModuleProps":
        '''Resource props.'''
        return typing.cast("CfnDeploymentModuleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModuleProps",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters", "resources": "resources"},
)
class CfnDeploymentModuleProps:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Union["CfnDeploymentModulePropsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["CfnDeploymentModulePropsResources", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Schema for Module Fragment of type Cyral::Sidecar::Deployment::MODULE.

        :param parameters: 
        :param resources: 

        :schema: CfnDeploymentModuleProps
        '''
        if isinstance(parameters, dict):
            parameters = CfnDeploymentModulePropsParameters(**parameters)
        if isinstance(resources, dict):
            resources = CfnDeploymentModulePropsResources(**resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0080438551c5e8ce1bbe0f93a800f1521def970b93c5af8a78f23023d6053a3c)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def parameters(self) -> typing.Optional["CfnDeploymentModulePropsParameters"]:
        '''
        :schema: CfnDeploymentModuleProps#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParameters"], result)

    @builtins.property
    def resources(self) -> typing.Optional["CfnDeploymentModulePropsResources"]:
        '''
        :schema: CfnDeploymentModuleProps#Resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResources"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParameters",
    jsii_struct_bases=[],
    name_mapping={
        "ami_id": "amiId",
        "asg_desired": "asgDesired",
        "asg_max": "asgMax",
        "asg_min": "asgMin",
        "associate_public_ip_address": "associatePublicIpAddress",
        "cloudwatch_log_group_name": "cloudwatchLogGroupName",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "container_registry": "containerRegistry",
        "container_registry_key": "containerRegistryKey",
        "container_registry_username": "containerRegistryUsername",
        "control_plane": "controlPlane",
        "custom_tag": "customTag",
        "custom_user_data_post": "customUserDataPost",
        "custom_user_data_pre": "customUserDataPre",
        "custom_user_data_pre_sidecar_start": "customUserDataPreSidecarStart",
        "db_inbound_cidr": "dbInboundCidr",
        "db_inbound_from_port": "dbInboundFromPort",
        "db_inbound_to_port": "dbInboundToPort",
        "ddapi_key": "ddapiKey",
        "deploy_secrets": "deploySecrets",
        "ec2_ebskms_arn": "ec2EbskmsArn",
        "ecsnlbdns_name": "ecsnlbdnsName",
        "hc_vault_integration_id": "hcVaultIntegrationId",
        "health_check_grace_period": "healthCheckGracePeriod",
        "id_p_certificate": "idPCertificate",
        "id_psso_login_url": "idPssoLoginUrl",
        "load_balancer_tls_ports": "loadBalancerTlsPorts",
        "log_integration": "logIntegration",
        "metadata_http_tokens_option": "metadataHttpTokensOption",
        "metrics_integration": "metricsIntegration",
        "monitoring_inbound_cidr": "monitoringInboundCidr",
        "name_prefix": "namePrefix",
        "num_sidecar_hosts": "numSidecarHosts",
        "permissions_boundary": "permissionsBoundary",
        "recycle_health_check_interval_sec": "recycleHealthCheckIntervalSec",
        "repositories_supported": "repositoriesSupported",
        "secrets_kms_arn": "secretsKmsArn",
        "secrets_location": "secretsLocation",
        "sidecar_ca_certificate_role_arn": "sidecarCaCertificateRoleArn",
        "sidecar_ca_certificate_secret_arn": "sidecarCaCertificateSecretArn",
        "sidecar_client_id": "sidecarClientId",
        "sidecar_client_secret": "sidecarClientSecret",
        "sidecar_custom_host_role": "sidecarCustomHostRole",
        "sidecar_dns_hosted_zone_id": "sidecarDnsHostedZoneId",
        "sidecar_dns_name": "sidecarDnsName",
        "sidecar_id": "sidecarId",
        "sidecar_instance_type": "sidecarInstanceType",
        "sidecar_private_id_p_key": "sidecarPrivateIdPKey",
        "sidecar_public_id_p_certificate": "sidecarPublicIdPCertificate",
        "sidecar_tls_certificate_role_arn": "sidecarTlsCertificateRoleArn",
        "sidecar_tls_certificate_secret_arn": "sidecarTlsCertificateSecretArn",
        "sidecar_version": "sidecarVersion",
        "sidecar_volume_size": "sidecarVolumeSize",
        "ssh_inbound_cidr": "sshInboundCidr",
        "ssh_key_name": "sshKeyName",
        "stack_target_group_ar_ns": "stackTargetGroupArNs",
        "subnets": "subnets",
        "tls_skip_verify": "tlsSkipVerify",
        "user_policies": "userPolicies",
        "use_single_container": "useSingleContainer",
        "vpc": "vpc",
    },
)
class CfnDeploymentModulePropsParameters:
    def __init__(
        self,
        *,
        ami_id: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersAmiId", typing.Dict[builtins.str, typing.Any]]] = None,
        asg_desired: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersAsgDesired", typing.Dict[builtins.str, typing.Any]]] = None,
        asg_max: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersAsgMax", typing.Dict[builtins.str, typing.Any]]] = None,
        asg_min: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersAsgMin", typing.Dict[builtins.str, typing.Any]]] = None,
        associate_public_ip_address: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersAssociatePublicIpAddress", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_log_group_name: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCloudwatchLogGroupName", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_logs_retention: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCloudwatchLogsRetention", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersContainerRegistry", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_key: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersContainerRegistryKey", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_username: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersContainerRegistryUsername", typing.Dict[builtins.str, typing.Any]]] = None,
        control_plane: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersControlPlane", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_tag: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCustomTag", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_user_data_post: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCustomUserDataPost", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_user_data_pre: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCustomUserDataPre", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_user_data_pre_sidecar_start: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart", typing.Dict[builtins.str, typing.Any]]] = None,
        db_inbound_cidr: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersDbInboundCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        db_inbound_from_port: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersDbInboundFromPort", typing.Dict[builtins.str, typing.Any]]] = None,
        db_inbound_to_port: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersDbInboundToPort", typing.Dict[builtins.str, typing.Any]]] = None,
        ddapi_key: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersDdapiKey", typing.Dict[builtins.str, typing.Any]]] = None,
        deploy_secrets: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersDeploySecrets", typing.Dict[builtins.str, typing.Any]]] = None,
        ec2_ebskms_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersEc2EbskmsArn", typing.Dict[builtins.str, typing.Any]]] = None,
        ecsnlbdns_name: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersEcsnlbdnsName", typing.Dict[builtins.str, typing.Any]]] = None,
        hc_vault_integration_id: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersHcVaultIntegrationId", typing.Dict[builtins.str, typing.Any]]] = None,
        health_check_grace_period: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersHealthCheckGracePeriod", typing.Dict[builtins.str, typing.Any]]] = None,
        id_p_certificate: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersIdPCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        id_psso_login_url: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersIdPssoLoginUrl", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer_tls_ports: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersLoadBalancerTlsPorts", typing.Dict[builtins.str, typing.Any]]] = None,
        log_integration: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersLogIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata_http_tokens_option: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersMetadataHttpTokensOption", typing.Dict[builtins.str, typing.Any]]] = None,
        metrics_integration: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersMetricsIntegration", typing.Dict[builtins.str, typing.Any]]] = None,
        monitoring_inbound_cidr: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersMonitoringInboundCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        name_prefix: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersNamePrefix", typing.Dict[builtins.str, typing.Any]]] = None,
        num_sidecar_hosts: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersNumSidecarHosts", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions_boundary: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersPermissionsBoundary", typing.Dict[builtins.str, typing.Any]]] = None,
        recycle_health_check_interval_sec: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec", typing.Dict[builtins.str, typing.Any]]] = None,
        repositories_supported: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersRepositoriesSupported", typing.Dict[builtins.str, typing.Any]]] = None,
        secrets_kms_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSecretsKmsArn", typing.Dict[builtins.str, typing.Any]]] = None,
        secrets_location: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSecretsLocation", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_ca_certificate_role_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_ca_certificate_secret_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_client_id: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarClientId", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_client_secret: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarClientSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_custom_host_role: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarCustomHostRole", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_dns_hosted_zone_id: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_dns_name: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarDnsName", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_id: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarId", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_instance_type: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarInstanceType", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_private_id_p_key: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarPrivateIdPKey", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_public_id_p_certificate: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_tls_certificate_role_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_tls_certificate_secret_arn: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_version: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarVersion", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_volume_size: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSidecarVolumeSize", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_inbound_cidr: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSshInboundCidr", typing.Dict[builtins.str, typing.Any]]] = None,
        ssh_key_name: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSshKeyName", typing.Dict[builtins.str, typing.Any]]] = None,
        stack_target_group_ar_ns: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersStackTargetGroupArNs", typing.Dict[builtins.str, typing.Any]]] = None,
        subnets: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersSubnets", typing.Dict[builtins.str, typing.Any]]] = None,
        tls_skip_verify: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersTlsSkipVerify", typing.Dict[builtins.str, typing.Any]]] = None,
        user_policies: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersUserPolicies", typing.Dict[builtins.str, typing.Any]]] = None,
        use_single_container: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersUseSingleContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[typing.Union["CfnDeploymentModulePropsParametersVpc", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ami_id: Amazon Linux 2 AMI ID for sidecar EC2 instances. The default behavior is to use the latest version. In order to define a new image, replace 'recommended' by the desired image name (eg 'amzn2-ami-ecs-hvm-2.0.20181112-x86_64-ebs').
        :param asg_desired: The desired number of hosts to create in the auto scaling group.
        :param asg_max: The maximum number of hosts to create in the auto scaling group.
        :param asg_min: The minimum number of hosts to create in the auto autoscaling group.
        :param associate_public_ip_address: Associates a public IP to sidecar EC2 instances.
        :param cloudwatch_log_group_name: Cloudwatch log group name.
        :param cloudwatch_logs_retention: Cloudwatch logs retention in days.
        :param container_registry: Address of the container registry where Cyral images are stored.
        :param container_registry_key: Key provided by Cyral for authenticating on Cyral's container registry.
        :param container_registry_username: Username provided by Cyral for authenticating on Cyral's container registry.
        :param control_plane: Address of the control plane - .cyral.com.
        :param custom_tag: (Optional) Custom tag to be added in the sidecar resources. Ex:"key=value".
        :param custom_user_data_post: (Optional) Ancillary consumer supplied user-data script. Provide Bash script commands to be executed after the sidecar starts. Ex:"echo 'TEST'"
        :param custom_user_data_pre: (Optional) Ancillary consumer supplied user-data script. Provide Bash script commands to be executed before the sidecar installation. Ex:"echo 'TEST'".
        :param custom_user_data_pre_sidecar_start: (Optional) Ancillary consumer supplied user-data script. Provide Bash script commands to be executed before the sidecar starts. Ex:"echo 'TEST'"
        :param db_inbound_cidr: Allowed CIDR block for database access to the sidecar.
        :param db_inbound_from_port: Allowed Starting Port for database access to the sidecar.
        :param db_inbound_to_port: Allowed Ending Port for database access to the sidecar.
        :param ddapi_key: (Deprecated - unused in sidecars v4.10+) API key to connect to DataDog.
        :param deploy_secrets: Create the AWS Secrets Manager resource at SecretsLocation containing client id, client secret and container registry key.
        :param ec2_ebskms_arn: (Optional) ARN of the KMS key used to encrypt/decrypt EBS volumes. If not set, EBS will use the default KMS key.
        :param ecsnlbdns_name: Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.
        :param hc_vault_integration_id: Hashicorp Vault Integration Id.
        :param health_check_grace_period: Determines how long (in seconds) the ASG will wait before checking the health status of the EC2 instance.
        :param id_p_certificate: (Optional) The certificate used to verify SAML assertions from the IdP being used with Snowflake. Enter this value as a one-line string with literal characters specifying the line breaks. Required if using SSO with Snowflake.
        :param id_psso_login_url: (Optional) The IdP SSO URL for the IdP being used with Snowflake. Required if using SSO with Snowflake.
        :param load_balancer_tls_ports: List of ports that will have TLS terminated at load balancer level (snowflake or S3 browser support, for example). If assigned, 'LoadBalancerCertificateArn' must also be provided. This parameter must be a subset of 'SidecarPorts'.
        :param log_integration: Log Integration Name.
        :param metadata_http_tokens_option: Instance Metadata Service token requirement.
        :param metrics_integration: Metrics Integration Name.
        :param monitoring_inbound_cidr: Allowed CIDR block for health check and metrics requests to the sidecar.
        :param name_prefix: Prefix for names of created resources in AWS.
        :param num_sidecar_hosts: (DEPRECATED - use Asg* parameters instead) Enter the number of sidecar hosts to create.
        :param permissions_boundary: ARN of the permissions boundary to apply to all the IAM roles. Set to an empty string if no permission boundaries should be used.
        :param recycle_health_check_interval_sec: (Optional) The interval (in seconds) in which the sidecar instance checks whether it has been marked or recycling.
        :param repositories_supported: List of wires that are enabled for the sidecar.
        :param secrets_kms_arn: (Optional) ARN of the KMS key used to encrypt/decrypt secrets. If not set, secrets will use the default KMS key.
        :param secrets_location: Location in AWS Secrets Manager to store client id, secret and container registry key.
        :param sidecar_ca_certificate_role_arn: (Optional) ARN of an AWS IAM Role to assume when reading the CA certificate.
        :param sidecar_ca_certificate_secret_arn: (Optional) ARN of secret in AWS Secrets Manager that contains a CA certificate to sign sidecar-generated certs.
        :param sidecar_client_id: Sidecar client ID.
        :param sidecar_client_secret: Sidecar client secret.
        :param sidecar_custom_host_role: (Optional) Name of an AWS IAM Role to attach to the EC2 instance profile.
        :param sidecar_dns_hosted_zone_id: (Optional) Route53 hosted zone ID for the corresponding SidecarDNSName provided.
        :param sidecar_dns_name: (Optional) Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.
        :param sidecar_id: Sidecar identifier.
        :param sidecar_instance_type: Amazon EC2 instance type for the sidecar instances.
        :param sidecar_private_id_p_key: (Optional) The private key used to sign SAML Assertions generated by the sidecar. Required if using SSO with Snowflake.
        :param sidecar_public_id_p_certificate: (Optional) The public certificate used to verify signatures for SAML Assertions generated by the sidecar. Required if using SSO with Snowflake.
        :param sidecar_tls_certificate_role_arn: (Optional) ARN of an AWS IAM Role to assume when reading the TLS certificate.
        :param sidecar_tls_certificate_secret_arn: (Optional) ARN of secret in AWS Secrets Manager that contains a certificate to terminate TLS connections.
        :param sidecar_version: (Optional, but required for Control Planes < v4.10) The version of the sidecar. If unset and the Control Plane version is >= v4.10, the sidecar version will be dynamically retrieved from the Control Plane, otherwise an error will occur and this value must be provided.
        :param sidecar_volume_size: Sidecar EC2 volume size (min 15GB).
        :param ssh_inbound_cidr: Allowed CIDR block for SSH access to the sidecar.
        :param ssh_key_name: Name of an existing EC2 KeyPair to enable SSH access to the EC2 instances.
        :param stack_target_group_ar_ns: 
        :param subnets: Subnets to add sidecar to.
        :param tls_skip_verify: Skip TLS verification for HTTPS communication with the control plane and during sidecar initialization.
        :param user_policies: (Optional) List of IAM policies ARNs that will be attached to the sidecar IAM role (Comma Delimited List).
        :param use_single_container: Determine whether to deploy as a single container or multiple containers.
        :param vpc: VPC.

        :schema: CfnDeploymentModulePropsParameters
        '''
        if isinstance(ami_id, dict):
            ami_id = CfnDeploymentModulePropsParametersAmiId(**ami_id)
        if isinstance(asg_desired, dict):
            asg_desired = CfnDeploymentModulePropsParametersAsgDesired(**asg_desired)
        if isinstance(asg_max, dict):
            asg_max = CfnDeploymentModulePropsParametersAsgMax(**asg_max)
        if isinstance(asg_min, dict):
            asg_min = CfnDeploymentModulePropsParametersAsgMin(**asg_min)
        if isinstance(associate_public_ip_address, dict):
            associate_public_ip_address = CfnDeploymentModulePropsParametersAssociatePublicIpAddress(**associate_public_ip_address)
        if isinstance(cloudwatch_log_group_name, dict):
            cloudwatch_log_group_name = CfnDeploymentModulePropsParametersCloudwatchLogGroupName(**cloudwatch_log_group_name)
        if isinstance(cloudwatch_logs_retention, dict):
            cloudwatch_logs_retention = CfnDeploymentModulePropsParametersCloudwatchLogsRetention(**cloudwatch_logs_retention)
        if isinstance(container_registry, dict):
            container_registry = CfnDeploymentModulePropsParametersContainerRegistry(**container_registry)
        if isinstance(container_registry_key, dict):
            container_registry_key = CfnDeploymentModulePropsParametersContainerRegistryKey(**container_registry_key)
        if isinstance(container_registry_username, dict):
            container_registry_username = CfnDeploymentModulePropsParametersContainerRegistryUsername(**container_registry_username)
        if isinstance(control_plane, dict):
            control_plane = CfnDeploymentModulePropsParametersControlPlane(**control_plane)
        if isinstance(custom_tag, dict):
            custom_tag = CfnDeploymentModulePropsParametersCustomTag(**custom_tag)
        if isinstance(custom_user_data_post, dict):
            custom_user_data_post = CfnDeploymentModulePropsParametersCustomUserDataPost(**custom_user_data_post)
        if isinstance(custom_user_data_pre, dict):
            custom_user_data_pre = CfnDeploymentModulePropsParametersCustomUserDataPre(**custom_user_data_pre)
        if isinstance(custom_user_data_pre_sidecar_start, dict):
            custom_user_data_pre_sidecar_start = CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart(**custom_user_data_pre_sidecar_start)
        if isinstance(db_inbound_cidr, dict):
            db_inbound_cidr = CfnDeploymentModulePropsParametersDbInboundCidr(**db_inbound_cidr)
        if isinstance(db_inbound_from_port, dict):
            db_inbound_from_port = CfnDeploymentModulePropsParametersDbInboundFromPort(**db_inbound_from_port)
        if isinstance(db_inbound_to_port, dict):
            db_inbound_to_port = CfnDeploymentModulePropsParametersDbInboundToPort(**db_inbound_to_port)
        if isinstance(ddapi_key, dict):
            ddapi_key = CfnDeploymentModulePropsParametersDdapiKey(**ddapi_key)
        if isinstance(deploy_secrets, dict):
            deploy_secrets = CfnDeploymentModulePropsParametersDeploySecrets(**deploy_secrets)
        if isinstance(ec2_ebskms_arn, dict):
            ec2_ebskms_arn = CfnDeploymentModulePropsParametersEc2EbskmsArn(**ec2_ebskms_arn)
        if isinstance(ecsnlbdns_name, dict):
            ecsnlbdns_name = CfnDeploymentModulePropsParametersEcsnlbdnsName(**ecsnlbdns_name)
        if isinstance(hc_vault_integration_id, dict):
            hc_vault_integration_id = CfnDeploymentModulePropsParametersHcVaultIntegrationId(**hc_vault_integration_id)
        if isinstance(health_check_grace_period, dict):
            health_check_grace_period = CfnDeploymentModulePropsParametersHealthCheckGracePeriod(**health_check_grace_period)
        if isinstance(id_p_certificate, dict):
            id_p_certificate = CfnDeploymentModulePropsParametersIdPCertificate(**id_p_certificate)
        if isinstance(id_psso_login_url, dict):
            id_psso_login_url = CfnDeploymentModulePropsParametersIdPssoLoginUrl(**id_psso_login_url)
        if isinstance(load_balancer_tls_ports, dict):
            load_balancer_tls_ports = CfnDeploymentModulePropsParametersLoadBalancerTlsPorts(**load_balancer_tls_ports)
        if isinstance(log_integration, dict):
            log_integration = CfnDeploymentModulePropsParametersLogIntegration(**log_integration)
        if isinstance(metadata_http_tokens_option, dict):
            metadata_http_tokens_option = CfnDeploymentModulePropsParametersMetadataHttpTokensOption(**metadata_http_tokens_option)
        if isinstance(metrics_integration, dict):
            metrics_integration = CfnDeploymentModulePropsParametersMetricsIntegration(**metrics_integration)
        if isinstance(monitoring_inbound_cidr, dict):
            monitoring_inbound_cidr = CfnDeploymentModulePropsParametersMonitoringInboundCidr(**monitoring_inbound_cidr)
        if isinstance(name_prefix, dict):
            name_prefix = CfnDeploymentModulePropsParametersNamePrefix(**name_prefix)
        if isinstance(num_sidecar_hosts, dict):
            num_sidecar_hosts = CfnDeploymentModulePropsParametersNumSidecarHosts(**num_sidecar_hosts)
        if isinstance(permissions_boundary, dict):
            permissions_boundary = CfnDeploymentModulePropsParametersPermissionsBoundary(**permissions_boundary)
        if isinstance(recycle_health_check_interval_sec, dict):
            recycle_health_check_interval_sec = CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec(**recycle_health_check_interval_sec)
        if isinstance(repositories_supported, dict):
            repositories_supported = CfnDeploymentModulePropsParametersRepositoriesSupported(**repositories_supported)
        if isinstance(secrets_kms_arn, dict):
            secrets_kms_arn = CfnDeploymentModulePropsParametersSecretsKmsArn(**secrets_kms_arn)
        if isinstance(secrets_location, dict):
            secrets_location = CfnDeploymentModulePropsParametersSecretsLocation(**secrets_location)
        if isinstance(sidecar_ca_certificate_role_arn, dict):
            sidecar_ca_certificate_role_arn = CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn(**sidecar_ca_certificate_role_arn)
        if isinstance(sidecar_ca_certificate_secret_arn, dict):
            sidecar_ca_certificate_secret_arn = CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn(**sidecar_ca_certificate_secret_arn)
        if isinstance(sidecar_client_id, dict):
            sidecar_client_id = CfnDeploymentModulePropsParametersSidecarClientId(**sidecar_client_id)
        if isinstance(sidecar_client_secret, dict):
            sidecar_client_secret = CfnDeploymentModulePropsParametersSidecarClientSecret(**sidecar_client_secret)
        if isinstance(sidecar_custom_host_role, dict):
            sidecar_custom_host_role = CfnDeploymentModulePropsParametersSidecarCustomHostRole(**sidecar_custom_host_role)
        if isinstance(sidecar_dns_hosted_zone_id, dict):
            sidecar_dns_hosted_zone_id = CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId(**sidecar_dns_hosted_zone_id)
        if isinstance(sidecar_dns_name, dict):
            sidecar_dns_name = CfnDeploymentModulePropsParametersSidecarDnsName(**sidecar_dns_name)
        if isinstance(sidecar_id, dict):
            sidecar_id = CfnDeploymentModulePropsParametersSidecarId(**sidecar_id)
        if isinstance(sidecar_instance_type, dict):
            sidecar_instance_type = CfnDeploymentModulePropsParametersSidecarInstanceType(**sidecar_instance_type)
        if isinstance(sidecar_private_id_p_key, dict):
            sidecar_private_id_p_key = CfnDeploymentModulePropsParametersSidecarPrivateIdPKey(**sidecar_private_id_p_key)
        if isinstance(sidecar_public_id_p_certificate, dict):
            sidecar_public_id_p_certificate = CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate(**sidecar_public_id_p_certificate)
        if isinstance(sidecar_tls_certificate_role_arn, dict):
            sidecar_tls_certificate_role_arn = CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn(**sidecar_tls_certificate_role_arn)
        if isinstance(sidecar_tls_certificate_secret_arn, dict):
            sidecar_tls_certificate_secret_arn = CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn(**sidecar_tls_certificate_secret_arn)
        if isinstance(sidecar_version, dict):
            sidecar_version = CfnDeploymentModulePropsParametersSidecarVersion(**sidecar_version)
        if isinstance(sidecar_volume_size, dict):
            sidecar_volume_size = CfnDeploymentModulePropsParametersSidecarVolumeSize(**sidecar_volume_size)
        if isinstance(ssh_inbound_cidr, dict):
            ssh_inbound_cidr = CfnDeploymentModulePropsParametersSshInboundCidr(**ssh_inbound_cidr)
        if isinstance(ssh_key_name, dict):
            ssh_key_name = CfnDeploymentModulePropsParametersSshKeyName(**ssh_key_name)
        if isinstance(stack_target_group_ar_ns, dict):
            stack_target_group_ar_ns = CfnDeploymentModulePropsParametersStackTargetGroupArNs(**stack_target_group_ar_ns)
        if isinstance(subnets, dict):
            subnets = CfnDeploymentModulePropsParametersSubnets(**subnets)
        if isinstance(tls_skip_verify, dict):
            tls_skip_verify = CfnDeploymentModulePropsParametersTlsSkipVerify(**tls_skip_verify)
        if isinstance(user_policies, dict):
            user_policies = CfnDeploymentModulePropsParametersUserPolicies(**user_policies)
        if isinstance(use_single_container, dict):
            use_single_container = CfnDeploymentModulePropsParametersUseSingleContainer(**use_single_container)
        if isinstance(vpc, dict):
            vpc = CfnDeploymentModulePropsParametersVpc(**vpc)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab7dc5f41dd448190ae88fabe417d3c9c075adf03ca5cb096d904212c328f1a)
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
            check_type(argname="argument asg_desired", value=asg_desired, expected_type=type_hints["asg_desired"])
            check_type(argname="argument asg_max", value=asg_max, expected_type=type_hints["asg_max"])
            check_type(argname="argument asg_min", value=asg_min, expected_type=type_hints["asg_min"])
            check_type(argname="argument associate_public_ip_address", value=associate_public_ip_address, expected_type=type_hints["associate_public_ip_address"])
            check_type(argname="argument cloudwatch_log_group_name", value=cloudwatch_log_group_name, expected_type=type_hints["cloudwatch_log_group_name"])
            check_type(argname="argument cloudwatch_logs_retention", value=cloudwatch_logs_retention, expected_type=type_hints["cloudwatch_logs_retention"])
            check_type(argname="argument container_registry", value=container_registry, expected_type=type_hints["container_registry"])
            check_type(argname="argument container_registry_key", value=container_registry_key, expected_type=type_hints["container_registry_key"])
            check_type(argname="argument container_registry_username", value=container_registry_username, expected_type=type_hints["container_registry_username"])
            check_type(argname="argument control_plane", value=control_plane, expected_type=type_hints["control_plane"])
            check_type(argname="argument custom_tag", value=custom_tag, expected_type=type_hints["custom_tag"])
            check_type(argname="argument custom_user_data_post", value=custom_user_data_post, expected_type=type_hints["custom_user_data_post"])
            check_type(argname="argument custom_user_data_pre", value=custom_user_data_pre, expected_type=type_hints["custom_user_data_pre"])
            check_type(argname="argument custom_user_data_pre_sidecar_start", value=custom_user_data_pre_sidecar_start, expected_type=type_hints["custom_user_data_pre_sidecar_start"])
            check_type(argname="argument db_inbound_cidr", value=db_inbound_cidr, expected_type=type_hints["db_inbound_cidr"])
            check_type(argname="argument db_inbound_from_port", value=db_inbound_from_port, expected_type=type_hints["db_inbound_from_port"])
            check_type(argname="argument db_inbound_to_port", value=db_inbound_to_port, expected_type=type_hints["db_inbound_to_port"])
            check_type(argname="argument ddapi_key", value=ddapi_key, expected_type=type_hints["ddapi_key"])
            check_type(argname="argument deploy_secrets", value=deploy_secrets, expected_type=type_hints["deploy_secrets"])
            check_type(argname="argument ec2_ebskms_arn", value=ec2_ebskms_arn, expected_type=type_hints["ec2_ebskms_arn"])
            check_type(argname="argument ecsnlbdns_name", value=ecsnlbdns_name, expected_type=type_hints["ecsnlbdns_name"])
            check_type(argname="argument hc_vault_integration_id", value=hc_vault_integration_id, expected_type=type_hints["hc_vault_integration_id"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
            check_type(argname="argument id_p_certificate", value=id_p_certificate, expected_type=type_hints["id_p_certificate"])
            check_type(argname="argument id_psso_login_url", value=id_psso_login_url, expected_type=type_hints["id_psso_login_url"])
            check_type(argname="argument load_balancer_tls_ports", value=load_balancer_tls_ports, expected_type=type_hints["load_balancer_tls_ports"])
            check_type(argname="argument log_integration", value=log_integration, expected_type=type_hints["log_integration"])
            check_type(argname="argument metadata_http_tokens_option", value=metadata_http_tokens_option, expected_type=type_hints["metadata_http_tokens_option"])
            check_type(argname="argument metrics_integration", value=metrics_integration, expected_type=type_hints["metrics_integration"])
            check_type(argname="argument monitoring_inbound_cidr", value=monitoring_inbound_cidr, expected_type=type_hints["monitoring_inbound_cidr"])
            check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            check_type(argname="argument num_sidecar_hosts", value=num_sidecar_hosts, expected_type=type_hints["num_sidecar_hosts"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument recycle_health_check_interval_sec", value=recycle_health_check_interval_sec, expected_type=type_hints["recycle_health_check_interval_sec"])
            check_type(argname="argument repositories_supported", value=repositories_supported, expected_type=type_hints["repositories_supported"])
            check_type(argname="argument secrets_kms_arn", value=secrets_kms_arn, expected_type=type_hints["secrets_kms_arn"])
            check_type(argname="argument secrets_location", value=secrets_location, expected_type=type_hints["secrets_location"])
            check_type(argname="argument sidecar_ca_certificate_role_arn", value=sidecar_ca_certificate_role_arn, expected_type=type_hints["sidecar_ca_certificate_role_arn"])
            check_type(argname="argument sidecar_ca_certificate_secret_arn", value=sidecar_ca_certificate_secret_arn, expected_type=type_hints["sidecar_ca_certificate_secret_arn"])
            check_type(argname="argument sidecar_client_id", value=sidecar_client_id, expected_type=type_hints["sidecar_client_id"])
            check_type(argname="argument sidecar_client_secret", value=sidecar_client_secret, expected_type=type_hints["sidecar_client_secret"])
            check_type(argname="argument sidecar_custom_host_role", value=sidecar_custom_host_role, expected_type=type_hints["sidecar_custom_host_role"])
            check_type(argname="argument sidecar_dns_hosted_zone_id", value=sidecar_dns_hosted_zone_id, expected_type=type_hints["sidecar_dns_hosted_zone_id"])
            check_type(argname="argument sidecar_dns_name", value=sidecar_dns_name, expected_type=type_hints["sidecar_dns_name"])
            check_type(argname="argument sidecar_id", value=sidecar_id, expected_type=type_hints["sidecar_id"])
            check_type(argname="argument sidecar_instance_type", value=sidecar_instance_type, expected_type=type_hints["sidecar_instance_type"])
            check_type(argname="argument sidecar_private_id_p_key", value=sidecar_private_id_p_key, expected_type=type_hints["sidecar_private_id_p_key"])
            check_type(argname="argument sidecar_public_id_p_certificate", value=sidecar_public_id_p_certificate, expected_type=type_hints["sidecar_public_id_p_certificate"])
            check_type(argname="argument sidecar_tls_certificate_role_arn", value=sidecar_tls_certificate_role_arn, expected_type=type_hints["sidecar_tls_certificate_role_arn"])
            check_type(argname="argument sidecar_tls_certificate_secret_arn", value=sidecar_tls_certificate_secret_arn, expected_type=type_hints["sidecar_tls_certificate_secret_arn"])
            check_type(argname="argument sidecar_version", value=sidecar_version, expected_type=type_hints["sidecar_version"])
            check_type(argname="argument sidecar_volume_size", value=sidecar_volume_size, expected_type=type_hints["sidecar_volume_size"])
            check_type(argname="argument ssh_inbound_cidr", value=ssh_inbound_cidr, expected_type=type_hints["ssh_inbound_cidr"])
            check_type(argname="argument ssh_key_name", value=ssh_key_name, expected_type=type_hints["ssh_key_name"])
            check_type(argname="argument stack_target_group_ar_ns", value=stack_target_group_ar_ns, expected_type=type_hints["stack_target_group_ar_ns"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tls_skip_verify", value=tls_skip_verify, expected_type=type_hints["tls_skip_verify"])
            check_type(argname="argument user_policies", value=user_policies, expected_type=type_hints["user_policies"])
            check_type(argname="argument use_single_container", value=use_single_container, expected_type=type_hints["use_single_container"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_id is not None:
            self._values["ami_id"] = ami_id
        if asg_desired is not None:
            self._values["asg_desired"] = asg_desired
        if asg_max is not None:
            self._values["asg_max"] = asg_max
        if asg_min is not None:
            self._values["asg_min"] = asg_min
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if cloudwatch_log_group_name is not None:
            self._values["cloudwatch_log_group_name"] = cloudwatch_log_group_name
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if container_registry is not None:
            self._values["container_registry"] = container_registry
        if container_registry_key is not None:
            self._values["container_registry_key"] = container_registry_key
        if container_registry_username is not None:
            self._values["container_registry_username"] = container_registry_username
        if control_plane is not None:
            self._values["control_plane"] = control_plane
        if custom_tag is not None:
            self._values["custom_tag"] = custom_tag
        if custom_user_data_post is not None:
            self._values["custom_user_data_post"] = custom_user_data_post
        if custom_user_data_pre is not None:
            self._values["custom_user_data_pre"] = custom_user_data_pre
        if custom_user_data_pre_sidecar_start is not None:
            self._values["custom_user_data_pre_sidecar_start"] = custom_user_data_pre_sidecar_start
        if db_inbound_cidr is not None:
            self._values["db_inbound_cidr"] = db_inbound_cidr
        if db_inbound_from_port is not None:
            self._values["db_inbound_from_port"] = db_inbound_from_port
        if db_inbound_to_port is not None:
            self._values["db_inbound_to_port"] = db_inbound_to_port
        if ddapi_key is not None:
            self._values["ddapi_key"] = ddapi_key
        if deploy_secrets is not None:
            self._values["deploy_secrets"] = deploy_secrets
        if ec2_ebskms_arn is not None:
            self._values["ec2_ebskms_arn"] = ec2_ebskms_arn
        if ecsnlbdns_name is not None:
            self._values["ecsnlbdns_name"] = ecsnlbdns_name
        if hc_vault_integration_id is not None:
            self._values["hc_vault_integration_id"] = hc_vault_integration_id
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period
        if id_p_certificate is not None:
            self._values["id_p_certificate"] = id_p_certificate
        if id_psso_login_url is not None:
            self._values["id_psso_login_url"] = id_psso_login_url
        if load_balancer_tls_ports is not None:
            self._values["load_balancer_tls_ports"] = load_balancer_tls_ports
        if log_integration is not None:
            self._values["log_integration"] = log_integration
        if metadata_http_tokens_option is not None:
            self._values["metadata_http_tokens_option"] = metadata_http_tokens_option
        if metrics_integration is not None:
            self._values["metrics_integration"] = metrics_integration
        if monitoring_inbound_cidr is not None:
            self._values["monitoring_inbound_cidr"] = monitoring_inbound_cidr
        if name_prefix is not None:
            self._values["name_prefix"] = name_prefix
        if num_sidecar_hosts is not None:
            self._values["num_sidecar_hosts"] = num_sidecar_hosts
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if recycle_health_check_interval_sec is not None:
            self._values["recycle_health_check_interval_sec"] = recycle_health_check_interval_sec
        if repositories_supported is not None:
            self._values["repositories_supported"] = repositories_supported
        if secrets_kms_arn is not None:
            self._values["secrets_kms_arn"] = secrets_kms_arn
        if secrets_location is not None:
            self._values["secrets_location"] = secrets_location
        if sidecar_ca_certificate_role_arn is not None:
            self._values["sidecar_ca_certificate_role_arn"] = sidecar_ca_certificate_role_arn
        if sidecar_ca_certificate_secret_arn is not None:
            self._values["sidecar_ca_certificate_secret_arn"] = sidecar_ca_certificate_secret_arn
        if sidecar_client_id is not None:
            self._values["sidecar_client_id"] = sidecar_client_id
        if sidecar_client_secret is not None:
            self._values["sidecar_client_secret"] = sidecar_client_secret
        if sidecar_custom_host_role is not None:
            self._values["sidecar_custom_host_role"] = sidecar_custom_host_role
        if sidecar_dns_hosted_zone_id is not None:
            self._values["sidecar_dns_hosted_zone_id"] = sidecar_dns_hosted_zone_id
        if sidecar_dns_name is not None:
            self._values["sidecar_dns_name"] = sidecar_dns_name
        if sidecar_id is not None:
            self._values["sidecar_id"] = sidecar_id
        if sidecar_instance_type is not None:
            self._values["sidecar_instance_type"] = sidecar_instance_type
        if sidecar_private_id_p_key is not None:
            self._values["sidecar_private_id_p_key"] = sidecar_private_id_p_key
        if sidecar_public_id_p_certificate is not None:
            self._values["sidecar_public_id_p_certificate"] = sidecar_public_id_p_certificate
        if sidecar_tls_certificate_role_arn is not None:
            self._values["sidecar_tls_certificate_role_arn"] = sidecar_tls_certificate_role_arn
        if sidecar_tls_certificate_secret_arn is not None:
            self._values["sidecar_tls_certificate_secret_arn"] = sidecar_tls_certificate_secret_arn
        if sidecar_version is not None:
            self._values["sidecar_version"] = sidecar_version
        if sidecar_volume_size is not None:
            self._values["sidecar_volume_size"] = sidecar_volume_size
        if ssh_inbound_cidr is not None:
            self._values["ssh_inbound_cidr"] = ssh_inbound_cidr
        if ssh_key_name is not None:
            self._values["ssh_key_name"] = ssh_key_name
        if stack_target_group_ar_ns is not None:
            self._values["stack_target_group_ar_ns"] = stack_target_group_ar_ns
        if subnets is not None:
            self._values["subnets"] = subnets
        if tls_skip_verify is not None:
            self._values["tls_skip_verify"] = tls_skip_verify
        if user_policies is not None:
            self._values["user_policies"] = user_policies
        if use_single_container is not None:
            self._values["use_single_container"] = use_single_container
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def ami_id(self) -> typing.Optional["CfnDeploymentModulePropsParametersAmiId"]:
        '''Amazon Linux 2 AMI ID for sidecar EC2 instances.

        The default behavior is to use the latest version. In order to define a new image, replace 'recommended' by the desired image name (eg 'amzn2-ami-ecs-hvm-2.0.20181112-x86_64-ebs').

        :schema: CfnDeploymentModulePropsParameters#AmiId
        '''
        result = self._values.get("ami_id")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersAmiId"], result)

    @builtins.property
    def asg_desired(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersAsgDesired"]:
        '''The desired number of hosts to create in the auto scaling group.

        :schema: CfnDeploymentModulePropsParameters#AsgDesired
        '''
        result = self._values.get("asg_desired")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersAsgDesired"], result)

    @builtins.property
    def asg_max(self) -> typing.Optional["CfnDeploymentModulePropsParametersAsgMax"]:
        '''The maximum number of hosts to create in the auto scaling group.

        :schema: CfnDeploymentModulePropsParameters#AsgMax
        '''
        result = self._values.get("asg_max")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersAsgMax"], result)

    @builtins.property
    def asg_min(self) -> typing.Optional["CfnDeploymentModulePropsParametersAsgMin"]:
        '''The minimum number of hosts to create in the auto autoscaling group.

        :schema: CfnDeploymentModulePropsParameters#AsgMin
        '''
        result = self._values.get("asg_min")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersAsgMin"], result)

    @builtins.property
    def associate_public_ip_address(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersAssociatePublicIpAddress"]:
        '''Associates a public IP to sidecar EC2 instances.

        :schema: CfnDeploymentModulePropsParameters#AssociatePublicIpAddress
        '''
        result = self._values.get("associate_public_ip_address")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersAssociatePublicIpAddress"], result)

    @builtins.property
    def cloudwatch_log_group_name(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCloudwatchLogGroupName"]:
        '''Cloudwatch log group name.

        :schema: CfnDeploymentModulePropsParameters#CloudwatchLogGroupName
        '''
        result = self._values.get("cloudwatch_log_group_name")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCloudwatchLogGroupName"], result)

    @builtins.property
    def cloudwatch_logs_retention(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCloudwatchLogsRetention"]:
        '''Cloudwatch logs retention in days.

        :schema: CfnDeploymentModulePropsParameters#CloudwatchLogsRetention
        '''
        result = self._values.get("cloudwatch_logs_retention")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCloudwatchLogsRetention"], result)

    @builtins.property
    def container_registry(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersContainerRegistry"]:
        '''Address of the container registry where Cyral images are stored.

        :schema: CfnDeploymentModulePropsParameters#ContainerRegistry
        '''
        result = self._values.get("container_registry")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersContainerRegistry"], result)

    @builtins.property
    def container_registry_key(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersContainerRegistryKey"]:
        '''Key provided by Cyral for authenticating on Cyral's container registry.

        :schema: CfnDeploymentModulePropsParameters#ContainerRegistryKey
        '''
        result = self._values.get("container_registry_key")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersContainerRegistryKey"], result)

    @builtins.property
    def container_registry_username(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersContainerRegistryUsername"]:
        '''Username provided by Cyral for authenticating on Cyral's container registry.

        :schema: CfnDeploymentModulePropsParameters#ContainerRegistryUsername
        '''
        result = self._values.get("container_registry_username")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersContainerRegistryUsername"], result)

    @builtins.property
    def control_plane(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersControlPlane"]:
        '''Address of the control plane - .cyral.com.

        :schema: CfnDeploymentModulePropsParameters#ControlPlane
        '''
        result = self._values.get("control_plane")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersControlPlane"], result)

    @builtins.property
    def custom_tag(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCustomTag"]:
        '''(Optional) Custom tag to be added in the sidecar resources.

        Ex:"key=value".

        :schema: CfnDeploymentModulePropsParameters#CustomTag
        '''
        result = self._values.get("custom_tag")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCustomTag"], result)

    @builtins.property
    def custom_user_data_post(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPost"]:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed after the sidecar starts. Ex:"echo 'TEST'"

        :schema: CfnDeploymentModulePropsParameters#CustomUserDataPost
        '''
        result = self._values.get("custom_user_data_post")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPost"], result)

    @builtins.property
    def custom_user_data_pre(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPre"]:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed before the sidecar installation. Ex:"echo 'TEST'".

        :schema: CfnDeploymentModulePropsParameters#CustomUserDataPre
        '''
        result = self._values.get("custom_user_data_pre")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPre"], result)

    @builtins.property
    def custom_user_data_pre_sidecar_start(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart"]:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed before the sidecar starts. Ex:"echo 'TEST'"

        :schema: CfnDeploymentModulePropsParameters#CustomUserDataPreSidecarStart
        '''
        result = self._values.get("custom_user_data_pre_sidecar_start")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart"], result)

    @builtins.property
    def db_inbound_cidr(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersDbInboundCidr"]:
        '''Allowed CIDR block for database access to the sidecar.

        :schema: CfnDeploymentModulePropsParameters#DBInboundCIDR
        '''
        result = self._values.get("db_inbound_cidr")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersDbInboundCidr"], result)

    @builtins.property
    def db_inbound_from_port(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersDbInboundFromPort"]:
        '''Allowed Starting Port for database access to the sidecar.

        :schema: CfnDeploymentModulePropsParameters#DBInboundFromPort
        '''
        result = self._values.get("db_inbound_from_port")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersDbInboundFromPort"], result)

    @builtins.property
    def db_inbound_to_port(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersDbInboundToPort"]:
        '''Allowed Ending Port for database access to the sidecar.

        :schema: CfnDeploymentModulePropsParameters#DBInboundToPort
        '''
        result = self._values.get("db_inbound_to_port")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersDbInboundToPort"], result)

    @builtins.property
    def ddapi_key(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersDdapiKey"]:
        '''(Deprecated - unused in sidecars v4.10+) API key to connect to DataDog.

        :schema: CfnDeploymentModulePropsParameters#DDAPIKey
        '''
        result = self._values.get("ddapi_key")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersDdapiKey"], result)

    @builtins.property
    def deploy_secrets(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersDeploySecrets"]:
        '''Create the AWS Secrets Manager resource at SecretsLocation containing client id, client secret and container registry key.

        :schema: CfnDeploymentModulePropsParameters#DeploySecrets
        '''
        result = self._values.get("deploy_secrets")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersDeploySecrets"], result)

    @builtins.property
    def ec2_ebskms_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersEc2EbskmsArn"]:
        '''(Optional) ARN of the KMS key used to encrypt/decrypt EBS volumes.

        If not set, EBS will use the default KMS key.

        :schema: CfnDeploymentModulePropsParameters#EC2EBSKMSArn
        '''
        result = self._values.get("ec2_ebskms_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersEc2EbskmsArn"], result)

    @builtins.property
    def ecsnlbdns_name(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersEcsnlbdnsName"]:
        '''Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.

        :schema: CfnDeploymentModulePropsParameters#ECSNLBDNSName
        '''
        result = self._values.get("ecsnlbdns_name")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersEcsnlbdnsName"], result)

    @builtins.property
    def hc_vault_integration_id(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersHcVaultIntegrationId"]:
        '''Hashicorp Vault Integration Id.

        :schema: CfnDeploymentModulePropsParameters#HCVaultIntegrationId
        '''
        result = self._values.get("hc_vault_integration_id")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersHcVaultIntegrationId"], result)

    @builtins.property
    def health_check_grace_period(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersHealthCheckGracePeriod"]:
        '''Determines how long (in seconds) the ASG will wait before checking the health status of the EC2 instance.

        :schema: CfnDeploymentModulePropsParameters#HealthCheckGracePeriod
        '''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersHealthCheckGracePeriod"], result)

    @builtins.property
    def id_p_certificate(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersIdPCertificate"]:
        '''(Optional) The certificate used to verify SAML assertions from the IdP being used with Snowflake.

        Enter this value as a one-line string with literal
        characters specifying the line breaks. Required if using SSO with Snowflake.

        :schema: CfnDeploymentModulePropsParameters#IdPCertificate
        '''
        result = self._values.get("id_p_certificate")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersIdPCertificate"], result)

    @builtins.property
    def id_psso_login_url(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersIdPssoLoginUrl"]:
        '''(Optional) The IdP SSO URL for the IdP being used with Snowflake.

        Required if using SSO with Snowflake.

        :schema: CfnDeploymentModulePropsParameters#IdPSSOLoginURL
        '''
        result = self._values.get("id_psso_login_url")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersIdPssoLoginUrl"], result)

    @builtins.property
    def load_balancer_tls_ports(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersLoadBalancerTlsPorts"]:
        '''List of ports that will have TLS terminated at load balancer level (snowflake or S3 browser support, for example).

        If assigned, 'LoadBalancerCertificateArn' must also be provided. This parameter must be a subset of 'SidecarPorts'.

        :schema: CfnDeploymentModulePropsParameters#LoadBalancerTLSPorts
        '''
        result = self._values.get("load_balancer_tls_ports")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersLoadBalancerTlsPorts"], result)

    @builtins.property
    def log_integration(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersLogIntegration"]:
        '''Log Integration Name.

        :schema: CfnDeploymentModulePropsParameters#LogIntegration
        '''
        result = self._values.get("log_integration")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersLogIntegration"], result)

    @builtins.property
    def metadata_http_tokens_option(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersMetadataHttpTokensOption"]:
        '''Instance Metadata Service token requirement.

        :schema: CfnDeploymentModulePropsParameters#MetadataHttpTokensOption
        '''
        result = self._values.get("metadata_http_tokens_option")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersMetadataHttpTokensOption"], result)

    @builtins.property
    def metrics_integration(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersMetricsIntegration"]:
        '''Metrics Integration Name.

        :schema: CfnDeploymentModulePropsParameters#MetricsIntegration
        '''
        result = self._values.get("metrics_integration")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersMetricsIntegration"], result)

    @builtins.property
    def monitoring_inbound_cidr(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersMonitoringInboundCidr"]:
        '''Allowed CIDR block for health check and metrics requests to the sidecar.

        :schema: CfnDeploymentModulePropsParameters#MonitoringInboundCIDR
        '''
        result = self._values.get("monitoring_inbound_cidr")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersMonitoringInboundCidr"], result)

    @builtins.property
    def name_prefix(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersNamePrefix"]:
        '''Prefix for names of created resources in AWS.

        :schema: CfnDeploymentModulePropsParameters#NamePrefix
        '''
        result = self._values.get("name_prefix")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersNamePrefix"], result)

    @builtins.property
    def num_sidecar_hosts(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersNumSidecarHosts"]:
        '''(DEPRECATED - use Asg* parameters instead) Enter the number of sidecar hosts to create.

        :schema: CfnDeploymentModulePropsParameters#NumSidecarHosts
        '''
        result = self._values.get("num_sidecar_hosts")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersNumSidecarHosts"], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersPermissionsBoundary"]:
        '''ARN of the permissions boundary to apply to all the IAM roles.

        Set to an empty string if no permission boundaries should be used.

        :schema: CfnDeploymentModulePropsParameters#PermissionsBoundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersPermissionsBoundary"], result)

    @builtins.property
    def recycle_health_check_interval_sec(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec"]:
        '''(Optional) The interval (in seconds) in which the sidecar instance checks whether it has been marked or recycling.

        :schema: CfnDeploymentModulePropsParameters#RecycleHealthCheckIntervalSec
        '''
        result = self._values.get("recycle_health_check_interval_sec")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec"], result)

    @builtins.property
    def repositories_supported(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersRepositoriesSupported"]:
        '''List of wires that are enabled for the sidecar.

        :schema: CfnDeploymentModulePropsParameters#RepositoriesSupported
        '''
        result = self._values.get("repositories_supported")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersRepositoriesSupported"], result)

    @builtins.property
    def secrets_kms_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSecretsKmsArn"]:
        '''(Optional) ARN of the KMS key used to encrypt/decrypt secrets.

        If not set, secrets will use the default KMS key.

        :schema: CfnDeploymentModulePropsParameters#SecretsKMSArn
        '''
        result = self._values.get("secrets_kms_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSecretsKmsArn"], result)

    @builtins.property
    def secrets_location(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSecretsLocation"]:
        '''Location in AWS Secrets Manager to store client id, secret and container registry key.

        :schema: CfnDeploymentModulePropsParameters#SecretsLocation
        '''
        result = self._values.get("secrets_location")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSecretsLocation"], result)

    @builtins.property
    def sidecar_ca_certificate_role_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn"]:
        '''(Optional) ARN of an AWS IAM Role to assume when reading the CA certificate.

        :schema: CfnDeploymentModulePropsParameters#SidecarCACertificateRoleArn
        '''
        result = self._values.get("sidecar_ca_certificate_role_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn"], result)

    @builtins.property
    def sidecar_ca_certificate_secret_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn"]:
        '''(Optional) ARN of secret in AWS Secrets Manager that contains a CA certificate to sign sidecar-generated certs.

        :schema: CfnDeploymentModulePropsParameters#SidecarCACertificateSecretArn
        '''
        result = self._values.get("sidecar_ca_certificate_secret_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn"], result)

    @builtins.property
    def sidecar_client_id(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarClientId"]:
        '''Sidecar client ID.

        :schema: CfnDeploymentModulePropsParameters#SidecarClientID
        '''
        result = self._values.get("sidecar_client_id")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarClientId"], result)

    @builtins.property
    def sidecar_client_secret(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarClientSecret"]:
        '''Sidecar client secret.

        :schema: CfnDeploymentModulePropsParameters#SidecarClientSecret
        '''
        result = self._values.get("sidecar_client_secret")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarClientSecret"], result)

    @builtins.property
    def sidecar_custom_host_role(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarCustomHostRole"]:
        '''(Optional) Name of an AWS IAM Role to attach to the EC2 instance profile.

        :schema: CfnDeploymentModulePropsParameters#SidecarCustomHostRole
        '''
        result = self._values.get("sidecar_custom_host_role")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarCustomHostRole"], result)

    @builtins.property
    def sidecar_dns_hosted_zone_id(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId"]:
        '''(Optional) Route53 hosted zone ID for the corresponding SidecarDNSName provided.

        :schema: CfnDeploymentModulePropsParameters#SidecarDNSHostedZoneId
        '''
        result = self._values.get("sidecar_dns_hosted_zone_id")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId"], result)

    @builtins.property
    def sidecar_dns_name(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarDnsName"]:
        '''(Optional) Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.

        :schema: CfnDeploymentModulePropsParameters#SidecarDNSName
        '''
        result = self._values.get("sidecar_dns_name")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarDnsName"], result)

    @builtins.property
    def sidecar_id(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarId"]:
        '''Sidecar identifier.

        :schema: CfnDeploymentModulePropsParameters#SidecarId
        '''
        result = self._values.get("sidecar_id")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarId"], result)

    @builtins.property
    def sidecar_instance_type(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarInstanceType"]:
        '''Amazon EC2 instance type for the sidecar instances.

        :schema: CfnDeploymentModulePropsParameters#SidecarInstanceType
        '''
        result = self._values.get("sidecar_instance_type")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarInstanceType"], result)

    @builtins.property
    def sidecar_private_id_p_key(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarPrivateIdPKey"]:
        '''(Optional) The private key used to sign SAML Assertions generated by the sidecar.

        Required if using SSO with Snowflake.

        :schema: CfnDeploymentModulePropsParameters#SidecarPrivateIdPKey
        '''
        result = self._values.get("sidecar_private_id_p_key")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarPrivateIdPKey"], result)

    @builtins.property
    def sidecar_public_id_p_certificate(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate"]:
        '''(Optional) The public certificate used to verify signatures for SAML Assertions generated by the sidecar.

        Required if using SSO with Snowflake.

        :schema: CfnDeploymentModulePropsParameters#SidecarPublicIdPCertificate
        '''
        result = self._values.get("sidecar_public_id_p_certificate")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate"], result)

    @builtins.property
    def sidecar_tls_certificate_role_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn"]:
        '''(Optional) ARN of an AWS IAM Role to assume when reading the TLS certificate.

        :schema: CfnDeploymentModulePropsParameters#SidecarTLSCertificateRoleArn
        '''
        result = self._values.get("sidecar_tls_certificate_role_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn"], result)

    @builtins.property
    def sidecar_tls_certificate_secret_arn(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn"]:
        '''(Optional) ARN of secret in AWS Secrets Manager that contains a certificate to terminate TLS connections.

        :schema: CfnDeploymentModulePropsParameters#SidecarTLSCertificateSecretArn
        '''
        result = self._values.get("sidecar_tls_certificate_secret_arn")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn"], result)

    @builtins.property
    def sidecar_version(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarVersion"]:
        '''(Optional, but required for Control Planes < v4.10) The version of the sidecar. If unset and the Control Plane version is >= v4.10, the sidecar version will be dynamically retrieved from the Control Plane, otherwise an error will occur and this value must be provided.

        :schema: CfnDeploymentModulePropsParameters#SidecarVersion
        '''
        result = self._values.get("sidecar_version")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarVersion"], result)

    @builtins.property
    def sidecar_volume_size(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSidecarVolumeSize"]:
        '''Sidecar EC2 volume size (min 15GB).

        :schema: CfnDeploymentModulePropsParameters#SidecarVolumeSize
        '''
        result = self._values.get("sidecar_volume_size")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSidecarVolumeSize"], result)

    @builtins.property
    def ssh_inbound_cidr(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSshInboundCidr"]:
        '''Allowed CIDR block for SSH access to the sidecar.

        :schema: CfnDeploymentModulePropsParameters#SSHInboundCIDR
        '''
        result = self._values.get("ssh_inbound_cidr")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSshInboundCidr"], result)

    @builtins.property
    def ssh_key_name(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersSshKeyName"]:
        '''Name of an existing EC2 KeyPair to enable SSH access to the EC2 instances.

        :schema: CfnDeploymentModulePropsParameters#SSHKeyName
        '''
        result = self._values.get("ssh_key_name")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSshKeyName"], result)

    @builtins.property
    def stack_target_group_ar_ns(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersStackTargetGroupArNs"]:
        '''
        :schema: CfnDeploymentModulePropsParameters#StackTargetGroupARNs
        '''
        result = self._values.get("stack_target_group_ar_ns")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersStackTargetGroupArNs"], result)

    @builtins.property
    def subnets(self) -> typing.Optional["CfnDeploymentModulePropsParametersSubnets"]:
        '''Subnets to add sidecar to.

        :schema: CfnDeploymentModulePropsParameters#Subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersSubnets"], result)

    @builtins.property
    def tls_skip_verify(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersTlsSkipVerify"]:
        '''Skip TLS verification for HTTPS communication with the control plane and during sidecar initialization.

        :schema: CfnDeploymentModulePropsParameters#TLSSkipVerify
        '''
        result = self._values.get("tls_skip_verify")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersTlsSkipVerify"], result)

    @builtins.property
    def user_policies(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersUserPolicies"]:
        '''(Optional) List of IAM policies ARNs that will be attached to the sidecar IAM role (Comma Delimited List).

        :schema: CfnDeploymentModulePropsParameters#UserPolicies
        '''
        result = self._values.get("user_policies")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersUserPolicies"], result)

    @builtins.property
    def use_single_container(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsParametersUseSingleContainer"]:
        '''Determine whether to deploy as a single container or multiple containers.

        :schema: CfnDeploymentModulePropsParameters#UseSingleContainer
        '''
        result = self._values.get("use_single_container")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersUseSingleContainer"], result)

    @builtins.property
    def vpc(self) -> typing.Optional["CfnDeploymentModulePropsParametersVpc"]:
        '''VPC.

        :schema: CfnDeploymentModulePropsParameters#VPC
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsParametersVpc"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersAmiId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersAmiId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Amazon Linux 2 AMI ID for sidecar EC2 instances.

        The default behavior is to use the latest version. In order to define a new image, replace 'recommended' by the desired image name (eg 'amzn2-ami-ecs-hvm-2.0.20181112-x86_64-ebs').

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersAmiId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ded6977b8576a28dbfdd97d1f56399a23147b9208c191d0b92a3882107ac35d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAmiId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAmiId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersAmiId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersAsgDesired",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersAsgDesired:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''The desired number of hosts to create in the auto scaling group.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersAsgDesired
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9de064ca1495f905e1e07c370f42c99b62a422c9090b35ae3ffde0386cd007a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgDesired#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgDesired#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersAsgDesired(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersAsgMax",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersAsgMax:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''The maximum number of hosts to create in the auto scaling group.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersAsgMax
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce23b3ce59b572330ff6f68faf8a8d40be7b66d12a9979e8d00999f08562593)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgMax#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgMax#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersAsgMax(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersAsgMin",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersAsgMin:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''The minimum number of hosts to create in the auto autoscaling group.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersAsgMin
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f379b92452ff018326338108e34d54d167a5694ab7e2405c53ab7d67f6c6185)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgMin#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAsgMin#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersAsgMin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersAssociatePublicIpAddress",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersAssociatePublicIpAddress:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Associates a public IP to sidecar EC2 instances.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersAssociatePublicIpAddress
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bee4ff2e6b5dd2bdb633781d56598a94e6fe45491ab04c0a3c0ca85daff297)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAssociatePublicIpAddress#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersAssociatePublicIpAddress#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersAssociatePublicIpAddress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCloudwatchLogGroupName",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCloudwatchLogGroupName:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Cloudwatch log group name.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCloudwatchLogGroupName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f60bca5df3c8eaa60ca1dfa85a88fd6f3e53602f216e6a825e57b7d687dcffc)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCloudwatchLogGroupName#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCloudwatchLogGroupName#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCloudwatchLogGroupName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCloudwatchLogsRetention",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCloudwatchLogsRetention:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Cloudwatch logs retention in days.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCloudwatchLogsRetention
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ade07e89099401d6fb56ac8818e27401f3af18938946a6da9b9bbece9013fb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCloudwatchLogsRetention#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCloudwatchLogsRetention#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCloudwatchLogsRetention(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersContainerRegistry",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersContainerRegistry:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Address of the container registry where Cyral images are stored.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersContainerRegistry
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273cb3675632aff458979b58fded156a1dc4716f31d127f75cefe60724781c80)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistry#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistry#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersContainerRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersContainerRegistryKey",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersContainerRegistryKey:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Key provided by Cyral for authenticating on Cyral's container registry.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersContainerRegistryKey
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d3c53bf1efabbd02d5a05f3c633d38c6bdaaf784cec6f73339b17f04379e9c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistryKey#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistryKey#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersContainerRegistryKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersContainerRegistryUsername",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersContainerRegistryUsername:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Username provided by Cyral for authenticating on Cyral's container registry.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersContainerRegistryUsername
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1e351476d09c9f6d8f75461a483efec64f60bbeeb9408dac71b875c9ab75a0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistryUsername#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersContainerRegistryUsername#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersContainerRegistryUsername(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersControlPlane",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersControlPlane:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Address of the control plane - .cyral.com.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersControlPlane
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ec02bb6b9ee8c57d8b21b528becd3aa6c6b1ad476f89604b9f72bf283d76c1)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersControlPlane#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersControlPlane#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersControlPlane(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCustomTag",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCustomTag:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Custom tag to be added in the sidecar resources.

        Ex:"key=value".

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCustomTag
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4946b49a51670eb0ee5b2ad82fff1cd587c457979dad49a6b688e192a4a2eed5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomTag#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomTag#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCustomTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCustomUserDataPost",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCustomUserDataPost:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed after the sidecar starts. Ex:"echo 'TEST'"

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCustomUserDataPost
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce512aaa46489cef250c3f52c1e573a1c7be7724634908feb7e912c64806ca08)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPost#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPost#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCustomUserDataPost(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCustomUserDataPre",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCustomUserDataPre:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed before the sidecar installation. Ex:"echo 'TEST'".

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCustomUserDataPre
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d919d6818eaa75740d7fb5218beafdf21d89e5b28db44e30b2268457496abfd)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPre#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPre#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCustomUserDataPre(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Ancillary consumer supplied user-data script.

        Provide Bash script commands to be executed before the sidecar starts. Ex:"echo 'TEST'"

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c9a0c390d66dec484d5eaf0dfab766c05cd606d5a70e26ade16d56201980e2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersDbInboundCidr",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersDbInboundCidr:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Allowed CIDR block for database access to the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersDbInboundCidr
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f498a3130298a141efeaf3d4d15845b16bf663e8ad0258710a233902fab102eb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundCidr#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundCidr#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersDbInboundCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersDbInboundFromPort",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersDbInboundFromPort:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Allowed Starting Port for database access to the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersDbInboundFromPort
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4829745b5e87ad5dbcf8840eb1b41991d07955da4dd72860fb4030a3897d3bb6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundFromPort#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundFromPort#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersDbInboundFromPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersDbInboundToPort",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersDbInboundToPort:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Allowed Ending Port for database access to the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersDbInboundToPort
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f22d2bd7cdaf7c88d733a0c12cd9665cfee6ac6eb51df1745181a1936c85d8b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundToPort#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDbInboundToPort#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersDbInboundToPort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersDdapiKey",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersDdapiKey:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Deprecated - unused in sidecars v4.10+) API key to connect to DataDog.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersDdapiKey
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dcb0e4457aa1f3f712b7c092e2d20e3cc325b39d876c1303473f7b2b84d1ce)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDdapiKey#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDdapiKey#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersDdapiKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersDeploySecrets",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersDeploySecrets:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Create the AWS Secrets Manager resource at SecretsLocation containing client id, client secret and container registry key.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersDeploySecrets
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde3eb4392459503eae4f2b129ba46f590199fb92a88db2b3c676eeb2d43bd53)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDeploySecrets#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersDeploySecrets#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersDeploySecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersEc2EbskmsArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersEc2EbskmsArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of the KMS key used to encrypt/decrypt EBS volumes.

        If not set, EBS will use the default KMS key.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersEc2EbskmsArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39586ff3d199d412620ad17d867095765dac16082069cf44ac0527d155df0d80)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersEc2EbskmsArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersEc2EbskmsArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersEc2EbskmsArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersEcsnlbdnsName",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersEcsnlbdnsName:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersEcsnlbdnsName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39f1cada033256d0a545608e5c203cf5b074bb005d801f1fa4541984c42c974)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersEcsnlbdnsName#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersEcsnlbdnsName#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersEcsnlbdnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersHcVaultIntegrationId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersHcVaultIntegrationId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Hashicorp Vault Integration Id.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersHcVaultIntegrationId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adcea4669cf1b98389762780963bf6e30a1f16d27b8e1ff969b88741fe41517)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersHcVaultIntegrationId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersHcVaultIntegrationId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersHcVaultIntegrationId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersHealthCheckGracePeriod",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersHealthCheckGracePeriod:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Determines how long (in seconds) the ASG will wait before checking the health status of the EC2 instance.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersHealthCheckGracePeriod
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538bec2898af3369e8b5b94d8ae4f98827064612e5bf8845da55c75934a4824e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersHealthCheckGracePeriod#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersHealthCheckGracePeriod#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersHealthCheckGracePeriod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersIdPCertificate",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersIdPCertificate:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) The certificate used to verify SAML assertions from the IdP being used with Snowflake.

        Enter this value as a one-line string with literal
        characters specifying the line breaks. Required if using SSO with Snowflake.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersIdPCertificate
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daceb1a9684fe73909c3b1849e5870596ac2f534ce8a40688be62b7aec2d83e2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersIdPCertificate#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersIdPCertificate#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersIdPCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersIdPssoLoginUrl",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersIdPssoLoginUrl:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) The IdP SSO URL for the IdP being used with Snowflake.

        Required if using SSO with Snowflake.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersIdPssoLoginUrl
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85ce7da64d175e1263f8db1c28f4abc98aa34a885dc7166ecccadee34c45916)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersIdPssoLoginUrl#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersIdPssoLoginUrl#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersIdPssoLoginUrl(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersLoadBalancerTlsPorts",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersLoadBalancerTlsPorts:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''List of ports that will have TLS terminated at load balancer level (snowflake or S3 browser support, for example).

        If assigned, 'LoadBalancerCertificateArn' must also be provided. This parameter must be a subset of 'SidecarPorts'.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersLoadBalancerTlsPorts
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__175b067cd0dd459fe27ec20ef27b297694b3da0150aa083c237259d79e702987)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersLoadBalancerTlsPorts#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersLoadBalancerTlsPorts#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersLoadBalancerTlsPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersLogIntegration",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersLogIntegration:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Log Integration Name.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersLogIntegration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5219d9c527cfc8980f04454e9f7ccdf76a7cd29d5fc21bbfb2e5089d5f207812)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersLogIntegration#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersLogIntegration#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersLogIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersMetadataHttpTokensOption",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersMetadataHttpTokensOption:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Instance Metadata Service token requirement.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersMetadataHttpTokensOption
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4954310de8972fba835b9f4838da3045e141df41779719323fdf7916399c15eb)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMetadataHttpTokensOption#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMetadataHttpTokensOption#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersMetadataHttpTokensOption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersMetricsIntegration",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersMetricsIntegration:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Metrics Integration Name.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersMetricsIntegration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1461a56cd6a90f7189aa9c3c8c4734411249182f7980ed69866652858a575c96)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMetricsIntegration#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMetricsIntegration#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersMetricsIntegration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersMonitoringInboundCidr",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersMonitoringInboundCidr:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Allowed CIDR block for health check and metrics requests to the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersMonitoringInboundCidr
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bd348ab36f65bb4087faaedd511e18389d0a7d21e8668bd07174489bdbb696)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMonitoringInboundCidr#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersMonitoringInboundCidr#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersMonitoringInboundCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersNamePrefix",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersNamePrefix:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Prefix for names of created resources in AWS.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersNamePrefix
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a388da12c2630a891a1a3b730149be41867cff7f8ab2326d87c340790d5d8564)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersNamePrefix#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersNamePrefix#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersNamePrefix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersNumSidecarHosts",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersNumSidecarHosts:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(DEPRECATED - use Asg* parameters instead) Enter the number of sidecar hosts to create.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersNumSidecarHosts
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59c27b606d3f6c33758f92b8c69a0ccebb6c75e32ff215411d5efdcb9ec6c8d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersNumSidecarHosts#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersNumSidecarHosts#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersNumSidecarHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersPermissionsBoundary",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersPermissionsBoundary:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''ARN of the permissions boundary to apply to all the IAM roles.

        Set to an empty string if no permission boundaries should be used.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersPermissionsBoundary
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e8eae52007ad722262cb6a77018d6332264ff32ff403cb181838554e08772b0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersPermissionsBoundary#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersPermissionsBoundary#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersPermissionsBoundary(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) The interval (in seconds) in which the sidecar instance checks whether it has been marked or recycling.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b3bdfd8efc26ab60803038067ab74c79f42a66f52a4740a1a2d46c33dc5a25)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersRepositoriesSupported",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersRepositoriesSupported:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''List of wires that are enabled for the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersRepositoriesSupported
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357e63a8b963a96360450ea4282e00e600d3b5cddb83ad2bf29f8a488c1dfee3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersRepositoriesSupported#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersRepositoriesSupported#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersRepositoriesSupported(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSecretsKmsArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSecretsKmsArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of the KMS key used to encrypt/decrypt secrets.

        If not set, secrets will use the default KMS key.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSecretsKmsArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22a786c7645e4b186562d72ab39aa8b4b6acef46edd6d8a027e4434473b33e66)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSecretsKmsArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSecretsKmsArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSecretsKmsArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSecretsLocation",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSecretsLocation:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Location in AWS Secrets Manager to store client id, secret and container registry key.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSecretsLocation
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a5066cd6c14fa3dd5ebdeca74dd0dd4c1825347286842ae8db06ee8b6f77d0)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSecretsLocation#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSecretsLocation#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSecretsLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of an AWS IAM Role to assume when reading the CA certificate.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee07c446f6960f98272efc98fdd6afee00017f91e714b8d35ef1f2889bf1272c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of secret in AWS Secrets Manager that contains a CA certificate to sign sidecar-generated certs.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea7c3b2f29269b03e26d2ced905f55e0023507fb2899eb20831426afabdd96c)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarClientId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarClientId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Sidecar client ID.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarClientId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07dbbc1926213130afba7a3f9a13196893fae9972c6e25fac95098121f26baa)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarClientId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarClientId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarClientId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarClientSecret",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarClientSecret:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Sidecar client secret.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarClientSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cef8c430edacab401916537a3be5e1d7e506f6d54d586fb1da1be42bde4dd9)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarClientSecret#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarClientSecret#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarClientSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarCustomHostRole",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarCustomHostRole:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Name of an AWS IAM Role to attach to the EC2 instance profile.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarCustomHostRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373f4994dc4ef0ce3aa5df105883b122e200ec1e16ce57438b539fc6d05237f7)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCustomHostRole#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarCustomHostRole#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarCustomHostRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Route53 hosted zone ID for the corresponding SidecarDNSName provided.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15789ce48e932912091661cd5b95ea6bc270a42d9a9a48a04e8cc8cc4c74557)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarDnsName",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarDnsName:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) Fully qualified domain name that will be automatically created/updated to reference the sidecar LB.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarDnsName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d2fe600b9e2f058242fdbd4016979ba500086f7517eb0c66bf5a03c9c31b79)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarDnsName#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarDnsName#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarDnsName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarId",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarId:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Sidecar identifier.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarId
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be488e9e3fcc3cc8889a9986840dc8ad82566f9baea7e46b10c9c54eddb8453)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarId#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarId#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarInstanceType",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarInstanceType:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Amazon EC2 instance type for the sidecar instances.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarInstanceType
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cde5f308fedbaf2a7fc957f54bef82fdb943a2bc1d9fb8708d2bc753280af6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarInstanceType#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarInstanceType#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarInstanceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarPrivateIdPKey",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarPrivateIdPKey:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) The private key used to sign SAML Assertions generated by the sidecar.

        Required if using SSO with Snowflake.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarPrivateIdPKey
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5416a6fa3d64935b1901ab1bc5bdfe8166f9d51fc325e649a801e0bcd0011b6d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarPrivateIdPKey#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarPrivateIdPKey#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarPrivateIdPKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) The public certificate used to verify signatures for SAML Assertions generated by the sidecar.

        Required if using SSO with Snowflake.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6852176b84378b48d87e2b967dac51667e4206b25a3558a909243e57bd336b7e)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of an AWS IAM Role to assume when reading the TLS certificate.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c224ee880e65162eafad585540fb217f4767de16b677f390c38fe27590339b03)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) ARN of secret in AWS Secrets Manager that contains a certificate to terminate TLS connections.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__615a7324ee1759590c18876abd3335a1f17c1f56c5ea7a0a6418c822d1035f7f)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarVersion",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarVersion:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional, but required for Control Planes < v4.10) The version of the sidecar. If unset and the Control Plane version is >= v4.10, the sidecar version will be dynamically retrieved from the Control Plane, otherwise an error will occur and this value must be provided.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarVersion
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21315ae2a7d97662b3b4a83ccc88ab8f42c4315d192245ae6a5b1969e00bbc4)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarVersion#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarVersion#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSidecarVolumeSize",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSidecarVolumeSize:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Sidecar EC2 volume size (min 15GB).

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSidecarVolumeSize
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6c5ee257e95c1120bda1368812d3b1b20f29cd4ff31b549e13293c758a1b6b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarVolumeSize#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSidecarVolumeSize#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSidecarVolumeSize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSshInboundCidr",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSshInboundCidr:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Allowed CIDR block for SSH access to the sidecar.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSshInboundCidr
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d53bf79257a9a50c98b861d8515f58f879ab4eee311d6df90bb2c167843647)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSshInboundCidr#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSshInboundCidr#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSshInboundCidr(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSshKeyName",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSshKeyName:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Name of an existing EC2 KeyPair to enable SSH access to the EC2 instances.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSshKeyName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ad3c943afda1d7f33ba9f2b9d042c1c1d02b3633bc5ce99c6f31a20809caa6)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSshKeyName#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSshKeyName#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSshKeyName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersStackTargetGroupArNs",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class CfnDeploymentModulePropsParametersStackTargetGroupArNs:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: 

        :schema: CfnDeploymentModulePropsParametersStackTargetGroupArNs
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__206edd13994c6137ae465b406b7a9fec6c9232110d318db4f98ae21c9981994c)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersStackTargetGroupArNs#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersStackTargetGroupArNs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersSubnets",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersSubnets:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Subnets to add sidecar to.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersSubnets
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13914f88b33a5a945fd2672b07caee97af7c10b11506d2ca981b0630b06d000)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSubnets#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersSubnets#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersSubnets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersTlsSkipVerify",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersTlsSkipVerify:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Skip TLS verification for HTTPS communication with the control plane and during sidecar initialization.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersTlsSkipVerify
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcf531a98db2386be1626a288afc497daa94d42a30d23fbff383afedc8bc802)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersTlsSkipVerify#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersTlsSkipVerify#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersTlsSkipVerify(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersUseSingleContainer",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersUseSingleContainer:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''Determine whether to deploy as a single container or multiple containers.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersUseSingleContainer
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b26f1feae62a4714ee6ef3b569bc8f043f501a6615811e905921741faa3eedd)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersUseSingleContainer#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersUseSingleContainer#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersUseSingleContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersUserPolicies",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersUserPolicies:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''(Optional) List of IAM policies ARNs that will be attached to the sidecar IAM role (Comma Delimited List).

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersUserPolicies
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a756e7152b4c6ee1388f498a929129d23440e55e2874e992b007fdc143d5b3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersUserPolicies#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersUserPolicies#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersUserPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsParametersVpc",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "type": "type"},
)
class CfnDeploymentModulePropsParametersVpc:
    def __init__(self, *, description: builtins.str, type: builtins.str) -> None:
        '''VPC.

        :param description: 
        :param type: 

        :schema: CfnDeploymentModulePropsParametersVpc
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4e763e6ef40f0f8f278e8424025965494af333d04ad7bed5564cc61fa2d564)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "type": type,
        }

    @builtins.property
    def description(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersVpc#Description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''
        :schema: CfnDeploymentModulePropsParametersVpc#Type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsParametersVpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResources",
    jsii_struct_bases=[],
    name_mapping={
        "auto_scaling_group_sidecar": "autoScalingGroupSidecar",
        "cloudwatch_log_group": "cloudwatchLogGroup",
        "lambda_ingress_list_role": "lambdaIngressListRole",
        "self_signed_certificate_lambda": "selfSignedCertificateLambda",
        "self_signed_certificate_role": "selfSignedCertificateRole",
        "sidecar_ca_certificate_secret": "sidecarCaCertificateSecret",
        "sidecar_c_name": "sidecarCName",
        "sidecar_created_certificate_secret": "sidecarCreatedCertificateSecret",
        "sidecar_host_policy": "sidecarHostPolicy",
        "sidecar_host_profile": "sidecarHostProfile",
        "sidecar_host_role": "sidecarHostRole",
        "sidecar_kms_policy": "sidecarKmsPolicy",
        "sidecar_launch_template": "sidecarLaunchTemplate",
        "sidecar_security_group": "sidecarSecurityGroup",
        "sm_sidecar_secret": "smSidecarSecret",
    },
)
class CfnDeploymentModulePropsResources:
    def __init__(
        self,
        *,
        auto_scaling_group_sidecar: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar", typing.Dict[builtins.str, typing.Any]]] = None,
        cloudwatch_log_group: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesCloudwatchLogGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_ingress_list_role: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesLambdaIngressListRole", typing.Dict[builtins.str, typing.Any]]] = None,
        self_signed_certificate_lambda: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda", typing.Dict[builtins.str, typing.Any]]] = None,
        self_signed_certificate_role: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSelfSignedCertificateRole", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_ca_certificate_secret: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_c_name: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarCName", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_created_certificate_secret: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_host_policy: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarHostPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_host_profile: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarHostProfile", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_host_role: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarHostRole", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_kms_policy: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarKmsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_launch_template: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarLaunchTemplate", typing.Dict[builtins.str, typing.Any]]] = None,
        sidecar_security_group: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSidecarSecurityGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        sm_sidecar_secret: typing.Optional[typing.Union["CfnDeploymentModulePropsResourcesSmSidecarSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auto_scaling_group_sidecar: 
        :param cloudwatch_log_group: 
        :param lambda_ingress_list_role: 
        :param self_signed_certificate_lambda: 
        :param self_signed_certificate_role: 
        :param sidecar_ca_certificate_secret: 
        :param sidecar_c_name: 
        :param sidecar_created_certificate_secret: 
        :param sidecar_host_policy: 
        :param sidecar_host_profile: 
        :param sidecar_host_role: 
        :param sidecar_kms_policy: 
        :param sidecar_launch_template: 
        :param sidecar_security_group: 
        :param sm_sidecar_secret: 

        :schema: CfnDeploymentModulePropsResources
        '''
        if isinstance(auto_scaling_group_sidecar, dict):
            auto_scaling_group_sidecar = CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar(**auto_scaling_group_sidecar)
        if isinstance(cloudwatch_log_group, dict):
            cloudwatch_log_group = CfnDeploymentModulePropsResourcesCloudwatchLogGroup(**cloudwatch_log_group)
        if isinstance(lambda_ingress_list_role, dict):
            lambda_ingress_list_role = CfnDeploymentModulePropsResourcesLambdaIngressListRole(**lambda_ingress_list_role)
        if isinstance(self_signed_certificate_lambda, dict):
            self_signed_certificate_lambda = CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda(**self_signed_certificate_lambda)
        if isinstance(self_signed_certificate_role, dict):
            self_signed_certificate_role = CfnDeploymentModulePropsResourcesSelfSignedCertificateRole(**self_signed_certificate_role)
        if isinstance(sidecar_ca_certificate_secret, dict):
            sidecar_ca_certificate_secret = CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret(**sidecar_ca_certificate_secret)
        if isinstance(sidecar_c_name, dict):
            sidecar_c_name = CfnDeploymentModulePropsResourcesSidecarCName(**sidecar_c_name)
        if isinstance(sidecar_created_certificate_secret, dict):
            sidecar_created_certificate_secret = CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret(**sidecar_created_certificate_secret)
        if isinstance(sidecar_host_policy, dict):
            sidecar_host_policy = CfnDeploymentModulePropsResourcesSidecarHostPolicy(**sidecar_host_policy)
        if isinstance(sidecar_host_profile, dict):
            sidecar_host_profile = CfnDeploymentModulePropsResourcesSidecarHostProfile(**sidecar_host_profile)
        if isinstance(sidecar_host_role, dict):
            sidecar_host_role = CfnDeploymentModulePropsResourcesSidecarHostRole(**sidecar_host_role)
        if isinstance(sidecar_kms_policy, dict):
            sidecar_kms_policy = CfnDeploymentModulePropsResourcesSidecarKmsPolicy(**sidecar_kms_policy)
        if isinstance(sidecar_launch_template, dict):
            sidecar_launch_template = CfnDeploymentModulePropsResourcesSidecarLaunchTemplate(**sidecar_launch_template)
        if isinstance(sidecar_security_group, dict):
            sidecar_security_group = CfnDeploymentModulePropsResourcesSidecarSecurityGroup(**sidecar_security_group)
        if isinstance(sm_sidecar_secret, dict):
            sm_sidecar_secret = CfnDeploymentModulePropsResourcesSmSidecarSecret(**sm_sidecar_secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a678543c1a9de9f331bff6b919be99f11613d27768bf066ceccfa76d05f64586)
            check_type(argname="argument auto_scaling_group_sidecar", value=auto_scaling_group_sidecar, expected_type=type_hints["auto_scaling_group_sidecar"])
            check_type(argname="argument cloudwatch_log_group", value=cloudwatch_log_group, expected_type=type_hints["cloudwatch_log_group"])
            check_type(argname="argument lambda_ingress_list_role", value=lambda_ingress_list_role, expected_type=type_hints["lambda_ingress_list_role"])
            check_type(argname="argument self_signed_certificate_lambda", value=self_signed_certificate_lambda, expected_type=type_hints["self_signed_certificate_lambda"])
            check_type(argname="argument self_signed_certificate_role", value=self_signed_certificate_role, expected_type=type_hints["self_signed_certificate_role"])
            check_type(argname="argument sidecar_ca_certificate_secret", value=sidecar_ca_certificate_secret, expected_type=type_hints["sidecar_ca_certificate_secret"])
            check_type(argname="argument sidecar_c_name", value=sidecar_c_name, expected_type=type_hints["sidecar_c_name"])
            check_type(argname="argument sidecar_created_certificate_secret", value=sidecar_created_certificate_secret, expected_type=type_hints["sidecar_created_certificate_secret"])
            check_type(argname="argument sidecar_host_policy", value=sidecar_host_policy, expected_type=type_hints["sidecar_host_policy"])
            check_type(argname="argument sidecar_host_profile", value=sidecar_host_profile, expected_type=type_hints["sidecar_host_profile"])
            check_type(argname="argument sidecar_host_role", value=sidecar_host_role, expected_type=type_hints["sidecar_host_role"])
            check_type(argname="argument sidecar_kms_policy", value=sidecar_kms_policy, expected_type=type_hints["sidecar_kms_policy"])
            check_type(argname="argument sidecar_launch_template", value=sidecar_launch_template, expected_type=type_hints["sidecar_launch_template"])
            check_type(argname="argument sidecar_security_group", value=sidecar_security_group, expected_type=type_hints["sidecar_security_group"])
            check_type(argname="argument sm_sidecar_secret", value=sm_sidecar_secret, expected_type=type_hints["sm_sidecar_secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_scaling_group_sidecar is not None:
            self._values["auto_scaling_group_sidecar"] = auto_scaling_group_sidecar
        if cloudwatch_log_group is not None:
            self._values["cloudwatch_log_group"] = cloudwatch_log_group
        if lambda_ingress_list_role is not None:
            self._values["lambda_ingress_list_role"] = lambda_ingress_list_role
        if self_signed_certificate_lambda is not None:
            self._values["self_signed_certificate_lambda"] = self_signed_certificate_lambda
        if self_signed_certificate_role is not None:
            self._values["self_signed_certificate_role"] = self_signed_certificate_role
        if sidecar_ca_certificate_secret is not None:
            self._values["sidecar_ca_certificate_secret"] = sidecar_ca_certificate_secret
        if sidecar_c_name is not None:
            self._values["sidecar_c_name"] = sidecar_c_name
        if sidecar_created_certificate_secret is not None:
            self._values["sidecar_created_certificate_secret"] = sidecar_created_certificate_secret
        if sidecar_host_policy is not None:
            self._values["sidecar_host_policy"] = sidecar_host_policy
        if sidecar_host_profile is not None:
            self._values["sidecar_host_profile"] = sidecar_host_profile
        if sidecar_host_role is not None:
            self._values["sidecar_host_role"] = sidecar_host_role
        if sidecar_kms_policy is not None:
            self._values["sidecar_kms_policy"] = sidecar_kms_policy
        if sidecar_launch_template is not None:
            self._values["sidecar_launch_template"] = sidecar_launch_template
        if sidecar_security_group is not None:
            self._values["sidecar_security_group"] = sidecar_security_group
        if sm_sidecar_secret is not None:
            self._values["sm_sidecar_secret"] = sm_sidecar_secret

    @builtins.property
    def auto_scaling_group_sidecar(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar"]:
        '''
        :schema: CfnDeploymentModulePropsResources#AutoScalingGroupSidecar
        '''
        result = self._values.get("auto_scaling_group_sidecar")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar"], result)

    @builtins.property
    def cloudwatch_log_group(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesCloudwatchLogGroup"]:
        '''
        :schema: CfnDeploymentModulePropsResources#CloudwatchLogGroup
        '''
        result = self._values.get("cloudwatch_log_group")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesCloudwatchLogGroup"], result)

    @builtins.property
    def lambda_ingress_list_role(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesLambdaIngressListRole"]:
        '''
        :schema: CfnDeploymentModulePropsResources#LambdaIngressListRole
        '''
        result = self._values.get("lambda_ingress_list_role")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesLambdaIngressListRole"], result)

    @builtins.property
    def self_signed_certificate_lambda(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SelfSignedCertificateLambda
        '''
        result = self._values.get("self_signed_certificate_lambda")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda"], result)

    @builtins.property
    def self_signed_certificate_role(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSelfSignedCertificateRole"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SelfSignedCertificateRole
        '''
        result = self._values.get("self_signed_certificate_role")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSelfSignedCertificateRole"], result)

    @builtins.property
    def sidecar_ca_certificate_secret(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarCACertificateSecret
        '''
        result = self._values.get("sidecar_ca_certificate_secret")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret"], result)

    @builtins.property
    def sidecar_c_name(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarCName"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarCName
        '''
        result = self._values.get("sidecar_c_name")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarCName"], result)

    @builtins.property
    def sidecar_created_certificate_secret(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarCreatedCertificateSecret
        '''
        result = self._values.get("sidecar_created_certificate_secret")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret"], result)

    @builtins.property
    def sidecar_host_policy(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostPolicy"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarHostPolicy
        '''
        result = self._values.get("sidecar_host_policy")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostPolicy"], result)

    @builtins.property
    def sidecar_host_profile(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostProfile"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarHostProfile
        '''
        result = self._values.get("sidecar_host_profile")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostProfile"], result)

    @builtins.property
    def sidecar_host_role(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostRole"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarHostRole
        '''
        result = self._values.get("sidecar_host_role")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarHostRole"], result)

    @builtins.property
    def sidecar_kms_policy(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarKmsPolicy"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarKMSPolicy
        '''
        result = self._values.get("sidecar_kms_policy")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarKmsPolicy"], result)

    @builtins.property
    def sidecar_launch_template(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarLaunchTemplate"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarLaunchTemplate
        '''
        result = self._values.get("sidecar_launch_template")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarLaunchTemplate"], result)

    @builtins.property
    def sidecar_security_group(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSidecarSecurityGroup"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SidecarSecurityGroup
        '''
        result = self._values.get("sidecar_security_group")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSidecarSecurityGroup"], result)

    @builtins.property
    def sm_sidecar_secret(
        self,
    ) -> typing.Optional["CfnDeploymentModulePropsResourcesSmSidecarSecret"]:
        '''
        :schema: CfnDeploymentModulePropsResources#SMSidecarSecret
        '''
        result = self._values.get("sm_sidecar_secret")
        return typing.cast(typing.Optional["CfnDeploymentModulePropsResourcesSmSidecarSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3b008ad7aa72bcb178aa190d20e0df7bf4c9d4ef53e2f45d3ad73411d05480)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesCloudwatchLogGroup",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesCloudwatchLogGroup:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesCloudwatchLogGroup
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df18f3c963a89713c4faa775cf2ed4d311669e93cb7837653f8f8694a168267)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesCloudwatchLogGroup#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesCloudwatchLogGroup#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesCloudwatchLogGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesLambdaIngressListRole",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesLambdaIngressListRole:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesLambdaIngressListRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4f58a480c4c5611359237dce9d301f32d4a1bd7abc6cb13f341edf265cc426)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesLambdaIngressListRole#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesLambdaIngressListRole#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesLambdaIngressListRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891145f586a807dc752d85deeca436be3b14350c302cd59f1791612a54648665)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSelfSignedCertificateRole",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSelfSignedCertificateRole:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db6fb63b64133acbe657b74521b06415bff99964a8d3b7912b9fcdf69f8729ff)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateRole#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSelfSignedCertificateRole#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSelfSignedCertificateRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarCName",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarCName:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarCName
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46acaf0612f66d1e221ceae959a24e8b258d7cd72ebb2251d48f682f406bd3d5)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCName#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCName#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarCName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5073de179fc0397a609124687633639b092631c52e1a8e3b853108bcc433858f)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6935e7e4936d698b15047c8dccc601e9362aa120769099184174fdaf259ca3)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarHostPolicy",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarHostPolicy:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarHostPolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e65c0ab63d5f9a56f24cb1952c64cdcf80fccc79dca045bb27b0ace29d694f1)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostPolicy#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostPolicy#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarHostPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarHostProfile",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarHostProfile:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarHostProfile
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361a92e81c7d2d77620e6269dd84d7c927323b30fd5ba8c15e8274d716dd5e58)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostProfile#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostProfile#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarHostProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarHostRole",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarHostRole:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarHostRole
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d88a147886f2f35033647526f3756ac77784a0031b17b9313eb2e8f0e0e245)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostRole#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarHostRole#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarHostRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarKmsPolicy",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarKmsPolicy:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarKmsPolicy
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc196af15b4f1f3f86e55ca9f534a05a14f96886380b709d04d80d1b2c0a3d23)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarKmsPolicy#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarKmsPolicy#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarKmsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarLaunchTemplate",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarLaunchTemplate:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarLaunchTemplate
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4963c4eeaba20903ffdffdeb65cc9f65312b082b7fbd45f9cbb5b5643688c3bd)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarLaunchTemplate#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarLaunchTemplate#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarLaunchTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSidecarSecurityGroup",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSidecarSecurityGroup:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSidecarSecurityGroup
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7deaefb070f3ebba70575ffad3896002fef3f0c6923352d544db45afdf14148)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarSecurityGroup#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSidecarSecurityGroup#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSidecarSecurityGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/cyral-sidecar-deployment-module.CfnDeploymentModulePropsResourcesSmSidecarSecret",
    jsii_struct_bases=[],
    name_mapping={"properties": "properties", "type": "type"},
)
class CfnDeploymentModulePropsResourcesSmSidecarSecret:
    def __init__(
        self,
        *,
        properties: typing.Any = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param properties: 
        :param type: 

        :schema: CfnDeploymentModulePropsResourcesSmSidecarSecret
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c5b59408d72fd549bd25df8f55ab8890cf72c62e9e607e51b0d253fc5c6e97)
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if properties is not None:
            self._values["properties"] = properties
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def properties(self) -> typing.Any:
        '''
        :schema: CfnDeploymentModulePropsResourcesSmSidecarSecret#Properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnDeploymentModulePropsResourcesSmSidecarSecret#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentModulePropsResourcesSmSidecarSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDeploymentModule",
    "CfnDeploymentModuleProps",
    "CfnDeploymentModulePropsParameters",
    "CfnDeploymentModulePropsParametersAmiId",
    "CfnDeploymentModulePropsParametersAsgDesired",
    "CfnDeploymentModulePropsParametersAsgMax",
    "CfnDeploymentModulePropsParametersAsgMin",
    "CfnDeploymentModulePropsParametersAssociatePublicIpAddress",
    "CfnDeploymentModulePropsParametersCloudwatchLogGroupName",
    "CfnDeploymentModulePropsParametersCloudwatchLogsRetention",
    "CfnDeploymentModulePropsParametersContainerRegistry",
    "CfnDeploymentModulePropsParametersContainerRegistryKey",
    "CfnDeploymentModulePropsParametersContainerRegistryUsername",
    "CfnDeploymentModulePropsParametersControlPlane",
    "CfnDeploymentModulePropsParametersCustomTag",
    "CfnDeploymentModulePropsParametersCustomUserDataPost",
    "CfnDeploymentModulePropsParametersCustomUserDataPre",
    "CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart",
    "CfnDeploymentModulePropsParametersDbInboundCidr",
    "CfnDeploymentModulePropsParametersDbInboundFromPort",
    "CfnDeploymentModulePropsParametersDbInboundToPort",
    "CfnDeploymentModulePropsParametersDdapiKey",
    "CfnDeploymentModulePropsParametersDeploySecrets",
    "CfnDeploymentModulePropsParametersEc2EbskmsArn",
    "CfnDeploymentModulePropsParametersEcsnlbdnsName",
    "CfnDeploymentModulePropsParametersHcVaultIntegrationId",
    "CfnDeploymentModulePropsParametersHealthCheckGracePeriod",
    "CfnDeploymentModulePropsParametersIdPCertificate",
    "CfnDeploymentModulePropsParametersIdPssoLoginUrl",
    "CfnDeploymentModulePropsParametersLoadBalancerTlsPorts",
    "CfnDeploymentModulePropsParametersLogIntegration",
    "CfnDeploymentModulePropsParametersMetadataHttpTokensOption",
    "CfnDeploymentModulePropsParametersMetricsIntegration",
    "CfnDeploymentModulePropsParametersMonitoringInboundCidr",
    "CfnDeploymentModulePropsParametersNamePrefix",
    "CfnDeploymentModulePropsParametersNumSidecarHosts",
    "CfnDeploymentModulePropsParametersPermissionsBoundary",
    "CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec",
    "CfnDeploymentModulePropsParametersRepositoriesSupported",
    "CfnDeploymentModulePropsParametersSecretsKmsArn",
    "CfnDeploymentModulePropsParametersSecretsLocation",
    "CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn",
    "CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn",
    "CfnDeploymentModulePropsParametersSidecarClientId",
    "CfnDeploymentModulePropsParametersSidecarClientSecret",
    "CfnDeploymentModulePropsParametersSidecarCustomHostRole",
    "CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId",
    "CfnDeploymentModulePropsParametersSidecarDnsName",
    "CfnDeploymentModulePropsParametersSidecarId",
    "CfnDeploymentModulePropsParametersSidecarInstanceType",
    "CfnDeploymentModulePropsParametersSidecarPrivateIdPKey",
    "CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate",
    "CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn",
    "CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn",
    "CfnDeploymentModulePropsParametersSidecarVersion",
    "CfnDeploymentModulePropsParametersSidecarVolumeSize",
    "CfnDeploymentModulePropsParametersSshInboundCidr",
    "CfnDeploymentModulePropsParametersSshKeyName",
    "CfnDeploymentModulePropsParametersStackTargetGroupArNs",
    "CfnDeploymentModulePropsParametersSubnets",
    "CfnDeploymentModulePropsParametersTlsSkipVerify",
    "CfnDeploymentModulePropsParametersUseSingleContainer",
    "CfnDeploymentModulePropsParametersUserPolicies",
    "CfnDeploymentModulePropsParametersVpc",
    "CfnDeploymentModulePropsResources",
    "CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar",
    "CfnDeploymentModulePropsResourcesCloudwatchLogGroup",
    "CfnDeploymentModulePropsResourcesLambdaIngressListRole",
    "CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda",
    "CfnDeploymentModulePropsResourcesSelfSignedCertificateRole",
    "CfnDeploymentModulePropsResourcesSidecarCName",
    "CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret",
    "CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret",
    "CfnDeploymentModulePropsResourcesSidecarHostPolicy",
    "CfnDeploymentModulePropsResourcesSidecarHostProfile",
    "CfnDeploymentModulePropsResourcesSidecarHostRole",
    "CfnDeploymentModulePropsResourcesSidecarKmsPolicy",
    "CfnDeploymentModulePropsResourcesSidecarLaunchTemplate",
    "CfnDeploymentModulePropsResourcesSidecarSecurityGroup",
    "CfnDeploymentModulePropsResourcesSmSidecarSecret",
]

publication.publish()

def _typecheckingstub__c0053a2f65c81e4364909e7bd4348b77a17a175ac0d1bfb8327e9d4bb7c0e43b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    parameters: typing.Optional[typing.Union[CfnDeploymentModulePropsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[CfnDeploymentModulePropsResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0080438551c5e8ce1bbe0f93a800f1521def970b93c5af8a78f23023d6053a3c(
    *,
    parameters: typing.Optional[typing.Union[CfnDeploymentModulePropsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[CfnDeploymentModulePropsResources, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab7dc5f41dd448190ae88fabe417d3c9c075adf03ca5cb096d904212c328f1a(
    *,
    ami_id: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersAmiId, typing.Dict[builtins.str, typing.Any]]] = None,
    asg_desired: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersAsgDesired, typing.Dict[builtins.str, typing.Any]]] = None,
    asg_max: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersAsgMax, typing.Dict[builtins.str, typing.Any]]] = None,
    asg_min: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersAsgMin, typing.Dict[builtins.str, typing.Any]]] = None,
    associate_public_ip_address: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersAssociatePublicIpAddress, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_log_group_name: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCloudwatchLogGroupName, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_logs_retention: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCloudwatchLogsRetention, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersContainerRegistry, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry_key: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersContainerRegistryKey, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry_username: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersContainerRegistryUsername, typing.Dict[builtins.str, typing.Any]]] = None,
    control_plane: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersControlPlane, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_tag: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCustomTag, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_user_data_post: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCustomUserDataPost, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_user_data_pre: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCustomUserDataPre, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_user_data_pre_sidecar_start: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersCustomUserDataPreSidecarStart, typing.Dict[builtins.str, typing.Any]]] = None,
    db_inbound_cidr: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersDbInboundCidr, typing.Dict[builtins.str, typing.Any]]] = None,
    db_inbound_from_port: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersDbInboundFromPort, typing.Dict[builtins.str, typing.Any]]] = None,
    db_inbound_to_port: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersDbInboundToPort, typing.Dict[builtins.str, typing.Any]]] = None,
    ddapi_key: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersDdapiKey, typing.Dict[builtins.str, typing.Any]]] = None,
    deploy_secrets: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersDeploySecrets, typing.Dict[builtins.str, typing.Any]]] = None,
    ec2_ebskms_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersEc2EbskmsArn, typing.Dict[builtins.str, typing.Any]]] = None,
    ecsnlbdns_name: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersEcsnlbdnsName, typing.Dict[builtins.str, typing.Any]]] = None,
    hc_vault_integration_id: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersHcVaultIntegrationId, typing.Dict[builtins.str, typing.Any]]] = None,
    health_check_grace_period: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersHealthCheckGracePeriod, typing.Dict[builtins.str, typing.Any]]] = None,
    id_p_certificate: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersIdPCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    id_psso_login_url: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersIdPssoLoginUrl, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer_tls_ports: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersLoadBalancerTlsPorts, typing.Dict[builtins.str, typing.Any]]] = None,
    log_integration: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersLogIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata_http_tokens_option: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersMetadataHttpTokensOption, typing.Dict[builtins.str, typing.Any]]] = None,
    metrics_integration: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersMetricsIntegration, typing.Dict[builtins.str, typing.Any]]] = None,
    monitoring_inbound_cidr: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersMonitoringInboundCidr, typing.Dict[builtins.str, typing.Any]]] = None,
    name_prefix: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersNamePrefix, typing.Dict[builtins.str, typing.Any]]] = None,
    num_sidecar_hosts: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersNumSidecarHosts, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions_boundary: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersPermissionsBoundary, typing.Dict[builtins.str, typing.Any]]] = None,
    recycle_health_check_interval_sec: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersRecycleHealthCheckIntervalSec, typing.Dict[builtins.str, typing.Any]]] = None,
    repositories_supported: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersRepositoriesSupported, typing.Dict[builtins.str, typing.Any]]] = None,
    secrets_kms_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSecretsKmsArn, typing.Dict[builtins.str, typing.Any]]] = None,
    secrets_location: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSecretsLocation, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_ca_certificate_role_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarCaCertificateRoleArn, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_ca_certificate_secret_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarCaCertificateSecretArn, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_client_id: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarClientId, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_client_secret: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarClientSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_custom_host_role: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarCustomHostRole, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_dns_hosted_zone_id: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarDnsHostedZoneId, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_dns_name: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarDnsName, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_id: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarId, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_instance_type: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarInstanceType, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_private_id_p_key: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarPrivateIdPKey, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_public_id_p_certificate: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarPublicIdPCertificate, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_tls_certificate_role_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarTlsCertificateRoleArn, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_tls_certificate_secret_arn: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarTlsCertificateSecretArn, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_version: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarVersion, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_volume_size: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSidecarVolumeSize, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_inbound_cidr: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSshInboundCidr, typing.Dict[builtins.str, typing.Any]]] = None,
    ssh_key_name: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSshKeyName, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_target_group_ar_ns: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersStackTargetGroupArNs, typing.Dict[builtins.str, typing.Any]]] = None,
    subnets: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersSubnets, typing.Dict[builtins.str, typing.Any]]] = None,
    tls_skip_verify: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersTlsSkipVerify, typing.Dict[builtins.str, typing.Any]]] = None,
    user_policies: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersUserPolicies, typing.Dict[builtins.str, typing.Any]]] = None,
    use_single_container: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersUseSingleContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[typing.Union[CfnDeploymentModulePropsParametersVpc, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ded6977b8576a28dbfdd97d1f56399a23147b9208c191d0b92a3882107ac35d(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9de064ca1495f905e1e07c370f42c99b62a422c9090b35ae3ffde0386cd007a(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce23b3ce59b572330ff6f68faf8a8d40be7b66d12a9979e8d00999f08562593(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f379b92452ff018326338108e34d54d167a5694ab7e2405c53ab7d67f6c6185(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bee4ff2e6b5dd2bdb633781d56598a94e6fe45491ab04c0a3c0ca85daff297(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f60bca5df3c8eaa60ca1dfa85a88fd6f3e53602f216e6a825e57b7d687dcffc(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ade07e89099401d6fb56ac8818e27401f3af18938946a6da9b9bbece9013fb(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273cb3675632aff458979b58fded156a1dc4716f31d127f75cefe60724781c80(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d3c53bf1efabbd02d5a05f3c633d38c6bdaaf784cec6f73339b17f04379e9c(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1e351476d09c9f6d8f75461a483efec64f60bbeeb9408dac71b875c9ab75a0(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ec02bb6b9ee8c57d8b21b528becd3aa6c6b1ad476f89604b9f72bf283d76c1(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4946b49a51670eb0ee5b2ad82fff1cd587c457979dad49a6b688e192a4a2eed5(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce512aaa46489cef250c3f52c1e573a1c7be7724634908feb7e912c64806ca08(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d919d6818eaa75740d7fb5218beafdf21d89e5b28db44e30b2268457496abfd(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c9a0c390d66dec484d5eaf0dfab766c05cd606d5a70e26ade16d56201980e2(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f498a3130298a141efeaf3d4d15845b16bf663e8ad0258710a233902fab102eb(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4829745b5e87ad5dbcf8840eb1b41991d07955da4dd72860fb4030a3897d3bb6(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f22d2bd7cdaf7c88d733a0c12cd9665cfee6ac6eb51df1745181a1936c85d8b(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dcb0e4457aa1f3f712b7c092e2d20e3cc325b39d876c1303473f7b2b84d1ce(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde3eb4392459503eae4f2b129ba46f590199fb92a88db2b3c676eeb2d43bd53(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39586ff3d199d412620ad17d867095765dac16082069cf44ac0527d155df0d80(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39f1cada033256d0a545608e5c203cf5b074bb005d801f1fa4541984c42c974(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adcea4669cf1b98389762780963bf6e30a1f16d27b8e1ff969b88741fe41517(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538bec2898af3369e8b5b94d8ae4f98827064612e5bf8845da55c75934a4824e(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daceb1a9684fe73909c3b1849e5870596ac2f534ce8a40688be62b7aec2d83e2(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b85ce7da64d175e1263f8db1c28f4abc98aa34a885dc7166ecccadee34c45916(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__175b067cd0dd459fe27ec20ef27b297694b3da0150aa083c237259d79e702987(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5219d9c527cfc8980f04454e9f7ccdf76a7cd29d5fc21bbfb2e5089d5f207812(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4954310de8972fba835b9f4838da3045e141df41779719323fdf7916399c15eb(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1461a56cd6a90f7189aa9c3c8c4734411249182f7980ed69866652858a575c96(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bd348ab36f65bb4087faaedd511e18389d0a7d21e8668bd07174489bdbb696(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a388da12c2630a891a1a3b730149be41867cff7f8ab2326d87c340790d5d8564(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59c27b606d3f6c33758f92b8c69a0ccebb6c75e32ff215411d5efdcb9ec6c8d(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8eae52007ad722262cb6a77018d6332264ff32ff403cb181838554e08772b0(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b3bdfd8efc26ab60803038067ab74c79f42a66f52a4740a1a2d46c33dc5a25(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357e63a8b963a96360450ea4282e00e600d3b5cddb83ad2bf29f8a488c1dfee3(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22a786c7645e4b186562d72ab39aa8b4b6acef46edd6d8a027e4434473b33e66(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a5066cd6c14fa3dd5ebdeca74dd0dd4c1825347286842ae8db06ee8b6f77d0(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee07c446f6960f98272efc98fdd6afee00017f91e714b8d35ef1f2889bf1272c(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea7c3b2f29269b03e26d2ced905f55e0023507fb2899eb20831426afabdd96c(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07dbbc1926213130afba7a3f9a13196893fae9972c6e25fac95098121f26baa(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cef8c430edacab401916537a3be5e1d7e506f6d54d586fb1da1be42bde4dd9(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373f4994dc4ef0ce3aa5df105883b122e200ec1e16ce57438b539fc6d05237f7(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15789ce48e932912091661cd5b95ea6bc270a42d9a9a48a04e8cc8cc4c74557(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d2fe600b9e2f058242fdbd4016979ba500086f7517eb0c66bf5a03c9c31b79(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be488e9e3fcc3cc8889a9986840dc8ad82566f9baea7e46b10c9c54eddb8453(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cde5f308fedbaf2a7fc957f54bef82fdb943a2bc1d9fb8708d2bc753280af6(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5416a6fa3d64935b1901ab1bc5bdfe8166f9d51fc325e649a801e0bcd0011b6d(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6852176b84378b48d87e2b967dac51667e4206b25a3558a909243e57bd336b7e(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c224ee880e65162eafad585540fb217f4767de16b677f390c38fe27590339b03(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615a7324ee1759590c18876abd3335a1f17c1f56c5ea7a0a6418c822d1035f7f(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21315ae2a7d97662b3b4a83ccc88ab8f42c4315d192245ae6a5b1969e00bbc4(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6c5ee257e95c1120bda1368812d3b1b20f29cd4ff31b549e13293c758a1b6b(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d53bf79257a9a50c98b861d8515f58f879ab4eee311d6df90bb2c167843647(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ad3c943afda1d7f33ba9f2b9d042c1c1d02b3633bc5ce99c6f31a20809caa6(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206edd13994c6137ae465b406b7a9fec6c9232110d318db4f98ae21c9981994c(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13914f88b33a5a945fd2672b07caee97af7c10b11506d2ca981b0630b06d000(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcf531a98db2386be1626a288afc497daa94d42a30d23fbff383afedc8bc802(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b26f1feae62a4714ee6ef3b569bc8f043f501a6615811e905921741faa3eedd(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a756e7152b4c6ee1388f498a929129d23440e55e2874e992b007fdc143d5b3(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4e763e6ef40f0f8f278e8424025965494af333d04ad7bed5564cc61fa2d564(
    *,
    description: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a678543c1a9de9f331bff6b919be99f11613d27768bf066ceccfa76d05f64586(
    *,
    auto_scaling_group_sidecar: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesAutoScalingGroupSidecar, typing.Dict[builtins.str, typing.Any]]] = None,
    cloudwatch_log_group: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesCloudwatchLogGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_ingress_list_role: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesLambdaIngressListRole, typing.Dict[builtins.str, typing.Any]]] = None,
    self_signed_certificate_lambda: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSelfSignedCertificateLambda, typing.Dict[builtins.str, typing.Any]]] = None,
    self_signed_certificate_role: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSelfSignedCertificateRole, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_ca_certificate_secret: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarCaCertificateSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_c_name: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarCName, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_created_certificate_secret: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarCreatedCertificateSecret, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_host_policy: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarHostPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_host_profile: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarHostProfile, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_host_role: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarHostRole, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_kms_policy: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarKmsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_launch_template: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarLaunchTemplate, typing.Dict[builtins.str, typing.Any]]] = None,
    sidecar_security_group: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSidecarSecurityGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    sm_sidecar_secret: typing.Optional[typing.Union[CfnDeploymentModulePropsResourcesSmSidecarSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3b008ad7aa72bcb178aa190d20e0df7bf4c9d4ef53e2f45d3ad73411d05480(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df18f3c963a89713c4faa775cf2ed4d311669e93cb7837653f8f8694a168267(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4f58a480c4c5611359237dce9d301f32d4a1bd7abc6cb13f341edf265cc426(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891145f586a807dc752d85deeca436be3b14350c302cd59f1791612a54648665(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6fb63b64133acbe657b74521b06415bff99964a8d3b7912b9fcdf69f8729ff(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46acaf0612f66d1e221ceae959a24e8b258d7cd72ebb2251d48f682f406bd3d5(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5073de179fc0397a609124687633639b092631c52e1a8e3b853108bcc433858f(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6935e7e4936d698b15047c8dccc601e9362aa120769099184174fdaf259ca3(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e65c0ab63d5f9a56f24cb1952c64cdcf80fccc79dca045bb27b0ace29d694f1(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361a92e81c7d2d77620e6269dd84d7c927323b30fd5ba8c15e8274d716dd5e58(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d88a147886f2f35033647526f3756ac77784a0031b17b9313eb2e8f0e0e245(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc196af15b4f1f3f86e55ca9f534a05a14f96886380b709d04d80d1b2c0a3d23(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4963c4eeaba20903ffdffdeb65cc9f65312b082b7fbd45f9cbb5b5643688c3bd(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7deaefb070f3ebba70575ffad3896002fef3f0c6923352d544db45afdf14148(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c5b59408d72fd549bd25df8f55ab8890cf72c62e9e607e51b0d253fc5c6e97(
    *,
    properties: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
