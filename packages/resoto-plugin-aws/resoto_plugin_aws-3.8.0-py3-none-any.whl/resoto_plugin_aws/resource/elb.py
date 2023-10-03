from typing import ClassVar, Dict, Optional, Type, List

from attrs import define, field

from resoto_plugin_aws.resource.base import AwsResource, GraphBuilder, AwsApiSpec
from resoto_plugin_aws.resource.ec2 import AwsEc2Subnet, AwsEc2SecurityGroup, AwsEc2Vpc, AwsEc2Instance
from resoto_plugin_aws.resource.cloudwatch import AwsCloudwatchQuery, AwsCloudwatchMetricData, update_resource_metrics
from resoto_plugin_aws.utils import ToDict, MetricNormalization
from resotolib.baseresources import BaseLoadBalancer, ModelReference
from resotolib.graph import Graph
from resotolib.json_bender import Bender, S, Bend, bend, ForallBend, K
from resotolib.types import Json
from resoto_plugin_aws.aws_client import AwsClient

service_name = "elb"


# noinspection PyUnresolvedReferences
class ElbTaggable:
    def update_resource_tag(self, client: AwsClient, key: str, value: str) -> bool:
        if isinstance(self, AwsResource):
            if spec := self.api_spec:
                client.call(
                    aws_service=spec.service,
                    action="add-tags",
                    result_name=None,
                    LoadBalancerNames=[self.name],
                    Tags=[{"Key": key, "Value": value}],
                )
                return True
            return False
        return False

    def delete_resource_tag(self, client: AwsClient, key: str) -> bool:
        if isinstance(self, AwsResource):
            if spec := self.api_spec:
                client.call(
                    aws_service=spec.service,
                    action="remove-tags",
                    result_name=None,
                    LoadBalancerNames=[self.name],
                    Tags=[{"Key": key}],
                )
                return True
            return False
        return False

    @classmethod
    def called_mutator_apis(cls) -> List[AwsApiSpec]:
        return [
            AwsApiSpec(service_name, "add-tags", override_iam_permission="elasticloadbalancing:AddTags"),
            AwsApiSpec(service_name, "remove-tags", override_iam_permission="elasticloadbalancing:RemoveTags"),
        ]


@define(eq=False, slots=False)
class AwsElbListener:
    kind: ClassVar[str] = "aws_elb_listener"
    mapping: ClassVar[Dict[str, Bender]] = {
        "protocol": S("Protocol"),
        "load_balancer_port": S("LoadBalancerPort"),
        "instance_protocol": S("InstanceProtocol"),
        "instance_port": S("InstancePort"),
        "ssl_certificate_id": S("SSLCertificateId"),
    }
    protocol: Optional[str] = field(default=None)
    load_balancer_port: Optional[int] = field(default=None)
    instance_protocol: Optional[str] = field(default=None)
    instance_port: Optional[int] = field(default=None)
    ssl_certificate_id: Optional[str] = field(default=None)


@define(eq=False, slots=False)
class AwsElbListenerDescription:
    kind: ClassVar[str] = "aws_elb_listener_description"
    mapping: ClassVar[Dict[str, Bender]] = {
        "listener": S("Listener") >> Bend(AwsElbListener.mapping),
        "policy_names": S("PolicyNames", default=[]),
    }
    listener: Optional[AwsElbListener] = field(default=None)
    policy_names: List[str] = field(factory=list)


@define(eq=False, slots=False)
class AwsElbAppCookieStickinessPolicy:
    kind: ClassVar[str] = "aws_elb_app_cookie_stickiness_policy"
    mapping: ClassVar[Dict[str, Bender]] = {"policy_name": S("PolicyName"), "cookie_name": S("CookieName")}
    policy_name: Optional[str] = field(default=None)
    cookie_name: Optional[str] = field(default=None)


@define(eq=False, slots=False)
class AwsElbLBCookieStickinessPolicy:
    kind: ClassVar[str] = "aws_elb_lb_cookie_stickiness_policy"
    mapping: ClassVar[Dict[str, Bender]] = {
        "policy_name": S("PolicyName"),
        "cookie_expiration_period": S("CookieExpirationPeriod"),
    }
    policy_name: Optional[str] = field(default=None)
    cookie_expiration_period: Optional[int] = field(default=None)


@define(eq=False, slots=False)
class AwsElbPolicies:
    kind: ClassVar[str] = "aws_elb_policies"
    mapping: ClassVar[Dict[str, Bender]] = {
        "app_cookie_stickiness_policies": S("AppCookieStickinessPolicies", default=[])
        >> ForallBend(AwsElbAppCookieStickinessPolicy.mapping),
        "lb_cookie_stickiness_policies": S("LBCookieStickinessPolicies", default=[])
        >> ForallBend(AwsElbLBCookieStickinessPolicy.mapping),
        "other_policies": S("OtherPolicies", default=[]),
    }
    app_cookie_stickiness_policies: List[AwsElbAppCookieStickinessPolicy] = field(factory=list)
    lb_cookie_stickiness_policies: List[AwsElbLBCookieStickinessPolicy] = field(factory=list)
    other_policies: List[str] = field(factory=list)


@define(eq=False, slots=False)
class AwsElbBackendServerDescription:
    kind: ClassVar[str] = "aws_elb_backend_server_description"
    mapping: ClassVar[Dict[str, Bender]] = {
        "instance_port": S("InstancePort"),
        "policy_names": S("PolicyNames", default=[]),
    }
    instance_port: Optional[int] = field(default=None)
    policy_names: List[str] = field(factory=list)


@define(eq=False, slots=False)
class AwsElbHealthCheck:
    kind: ClassVar[str] = "aws_elb_health_check"
    mapping: ClassVar[Dict[str, Bender]] = {
        "target": S("Target"),
        "interval": S("Interval"),
        "timeout": S("Timeout"),
        "unhealthy_threshold": S("UnhealthyThreshold"),
        "healthy_threshold": S("HealthyThreshold"),
    }
    target: Optional[str] = field(default=None)
    interval: Optional[int] = field(default=None)
    timeout: Optional[int] = field(default=None)
    unhealthy_threshold: Optional[int] = field(default=None)
    healthy_threshold: Optional[int] = field(default=None)


@define(eq=False, slots=False)
class AwsElbSourceSecurityGroup:
    kind: ClassVar[str] = "aws_elb_source_security_group"
    mapping: ClassVar[Dict[str, Bender]] = {"owner_alias": S("OwnerAlias"), "group_name": S("GroupName")}
    owner_alias: Optional[str] = field(default=None)
    group_name: Optional[str] = field(default=None)


@define(eq=False, slots=False)
class AwsElb(ElbTaggable, AwsResource, BaseLoadBalancer):
    kind: ClassVar[str] = "aws_elb"
    api_spec: ClassVar[AwsApiSpec] = AwsApiSpec(
        service_name,
        "describe-load-balancers",
        "LoadBalancerDescriptions",
        override_iam_permission="elasticloadbalancing:DescribeLoadBalancers",
    )
    reference_kinds: ClassVar[ModelReference] = {
        "predecessors": {
            "default": ["aws_vpc", "aws_ec2_subnet", "aws_ec2_security_group"],
            "delete": ["aws_vpc", "aws_ec2_subnet", "aws_ec2_security_group", "aws_ec2_instance"],
        },
        "successors": {
            "default": ["aws_ec2_instance"],
        },
    }
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("DNSName"),
        "name": S("LoadBalancerName"),
        "lb_type": K("elb"),
        "ctime": S("CreatedTime"),
        "backends": S("Instances", default=[]) >> ForallBend(S("InstanceId")),
        "elb_canonical_hosted_zone_name": S("CanonicalHostedZoneName"),
        "elb_canonical_hosted_zone_name_id": S("CanonicalHostedZoneNameID"),
        "elb_listener_descriptions": S("ListenerDescriptions", default=[])
        >> ForallBend(AwsElbListenerDescription.mapping),
        "elb_policies": S("Policies") >> Bend(AwsElbPolicies.mapping),
        "elb_backend_server_descriptions": S("BackendServerDescriptions", default=[])
        >> ForallBend(AwsElbBackendServerDescription.mapping),
        "elb_availability_zones": S("AvailabilityZones", default=[]),
        "elb_health_check": S("HealthCheck") >> Bend(AwsElbHealthCheck.mapping),
        "elb_source_security_group": S("SourceSecurityGroup") >> Bend(AwsElbSourceSecurityGroup.mapping),
        "scheme": S("Scheme"),
    }
    scheme: Optional[str] = field(default=None)
    elb_canonical_hosted_zone_name: Optional[str] = field(default=None)
    elb_canonical_hosted_zone_name_id: Optional[str] = field(default=None)
    elb_listener_descriptions: List[AwsElbListenerDescription] = field(factory=list)
    elb_policies: Optional[AwsElbPolicies] = field(default=None)
    elb_backend_server_descriptions: List[AwsElbBackendServerDescription] = field(factory=list)
    elb_availability_zones: List[str] = field(factory=list)
    elb_health_check: Optional[AwsElbHealthCheck] = field(default=None)
    elb_source_security_group: Optional[AwsElbSourceSecurityGroup] = field(default=None)

    @classmethod
    def called_collect_apis(cls) -> List[AwsApiSpec]:
        return [
            cls.api_spec,
            AwsApiSpec(
                cls.api_spec.service,
                "describe-tags",
                override_iam_permission="elasticloadbalancing:DescribeTags",
            ),
        ]

    @classmethod
    def collect(cls: Type[AwsResource], json: List[Json], builder: GraphBuilder) -> None:
        def add_tags(elb: AwsElb) -> None:
            tags = builder.client.list(
                service_name,
                "describe-tags",
                "TagDescriptions",
                LoadBalancerNames=[elb.name],
                expected_errors=["LoadBalancerNotFound"],
            )
            if tags:
                elb.tags = bend(S("Tags", default=[]) >> ToDict(), tags[0])

        for js in json:
            if instance := cls.from_api(js, builder):
                builder.add_node(instance, js)
                builder.submit_work(service_name, add_tags, instance)

    @classmethod
    def collect_usage_metrics(cls: Type[AwsResource], builder: GraphBuilder) -> None:
        elbs = {elb.id: elb for elb in builder.nodes(clazz=AwsElb) if elb.region().id == builder.region.id}
        queries = []
        delta = builder.metrics_delta
        start = builder.metrics_start
        now = builder.created_at
        for elb_id, elb in elbs.items():
            queries.extend(
                [
                    AwsCloudwatchQuery.create(
                        metric_name=metric,
                        namespace="AWS/ELB",
                        period=delta,
                        ref_id=elb_id,
                        stat="Sum",
                        unit="Count",
                        LoadBalancerName=elb.name or "",
                    )
                    for metric in [
                        "RequestCount",
                        "HealthyHostCount",
                        "UnHealthyHostCount",
                        "EstimatedALBActiveConnectionCount",
                        "HTTPCode_Backend_2XX_Count",
                        "HTTPCode_Backend_4XX_Count",
                        "HTTPCode_Backend_5XX_Count",
                    ]
                ]
            )
            queries.extend(
                [
                    AwsCloudwatchQuery.create(
                        metric_name="Latency",
                        namespace="AWS/ELB",
                        period=delta,
                        ref_id=elb_id,
                        stat=stat,
                        unit="Seconds",
                        LoadBalancerName=elb.name or "",
                    )
                    for stat in ["Minimum", "Average", "Maximum"]
                ]
            )
            queries.extend(
                [
                    AwsCloudwatchQuery.create(
                        metric_name="EstimatedProcessedBytes",
                        namespace="AWS/ELB",
                        period=delta,
                        ref_id=elb_id,
                        stat="Sum",
                        unit="Bytes",
                        LoadBalancerName=elb.name or "",
                    )
                ]
            )

        metric_normalizers = {
            "RequestCount": MetricNormalization(name="request_count"),
            "EstimatedALBActiveConnectionCount": MetricNormalization(name="active_connection_count"),
            "HTTPCode_Backend_2XX_Count": MetricNormalization(name="status_code_2xx_count"),
            "HTTPCode_Backend_4XX_Count": MetricNormalization(name="status_code_4xx_count"),
            "HTTPCode_Backend_5XX_Count": MetricNormalization(name="status_code_5xx_count"),
            "HealthyHostCount": MetricNormalization(name="healthy_host_count"),
            "UnHealthyHostCount": MetricNormalization(name="unhealthy_host_count"),
            "Latency": MetricNormalization(name="latency_seconds", normalize_value=lambda x: round(x, ndigits=3)),
            "EstimatedProcessedBytes": MetricNormalization(name="processed_bytes"),
        }

        cloudwatch_result = AwsCloudwatchMetricData.query_for(builder.client, queries, start, now)

        update_resource_metrics(elbs, cloudwatch_result, metric_normalizers)

    def connect_in_graph(self, builder: GraphBuilder, source: Json) -> None:
        super().connect_in_graph(builder, source)
        if vpc_id := source.get("VPCId"):
            builder.dependant_node(self, reverse=True, delete_same_as_default=True, clazz=AwsEc2Vpc, id=vpc_id)
        for subnet_id in source.get("Subnets", []):
            builder.dependant_node(self, reverse=True, delete_same_as_default=True, clazz=AwsEc2Subnet, id=subnet_id)
        for sg_id in source.get("SecurityGroups", []):
            builder.dependant_node(self, reverse=True, delete_same_as_default=True, clazz=AwsEc2SecurityGroup, id=sg_id)
        for instance in self.backends:
            builder.dependant_node(self, clazz=AwsEc2Instance, id=instance)

    def delete_resource(self, client: AwsClient, graph: Graph) -> bool:
        client.call(
            aws_service=self.api_spec.service,
            action="delete-load-balancer",
            result_name=None,
            LoadBalancerName=self.name,
        )
        return True

    @classmethod
    def called_mutator_apis(cls) -> List[AwsApiSpec]:
        return super().called_mutator_apis() + [
            AwsApiSpec(
                service_name, "delete-load-balancer", override_iam_permission="elasticloadbalancing:DeleteLoadBalancer"
            ),
        ]


resources: List[Type[AwsResource]] = [AwsElb]
