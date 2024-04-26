from aws_cdk import (
    Duration,
    Stack,
    aws_apigatewayv2 as apigw2,
    aws_apigatewayv2_integrations as apigw2_int,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_dynamodb as ddb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class BedrockWebsocketApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Setup WebSocket API
        table = ddb.Table(
            self, "Connections",
            partition_key=ddb.Attribute(
                name="pk",
                type=ddb.AttributeType.STRING
            ),
            sort_key=ddb.Attribute(
                name="sk",
                type=ddb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        connect_function = _lambda.Function(
            self, "ConnectFunction",
            handler="on_connect.handler",
            code=_lambda.Code.from_asset("functions"),
            runtime=_lambda.Runtime.PYTHON_3_12,
            environment={
                "TABLE_NAME": table.table_name
            },
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.THREE_DAYS,
        )
        table.grant_write_data(connect_function)

        disconnect_function = _lambda.Function(
            self, "DisconnectFunction",
            handler="on_disconnect.handler",
            code=_lambda.Code.from_asset("functions"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "TABLE_NAME": table.table_name
            },
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.THREE_DAYS,
        )
        table.grant_write_data(disconnect_function)

        default_function = _lambda.Function(
            self, "DefaultFunction",
            handler="on_default.handler",
            code=_lambda.Code.from_asset("functions"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.THREE_DAYS,
        )

        ws_api = apigw2.WebSocketApi(
            self, "WebSocketApi",
            connect_route_options=apigw2.WebSocketRouteOptions(
                integration=apigw2_int.WebSocketLambdaIntegration('ConnectIntegration', connect_function)
            ),
            disconnect_route_options=apigw2.WebSocketRouteOptions(
                integration=apigw2_int.WebSocketLambdaIntegration('DisconnectIntegration', disconnect_function)
            ),
            default_route_options=apigw2.WebSocketRouteOptions(
                integration=apigw2_int.WebSocketLambdaIntegration('DefaultIntegration', default_function)
            ),
        )

        ws_stage = apigw2.WebSocketStage(
            self, "WebSocketApiStage",
            stage_name='default',
            web_socket_api=ws_api,
            auto_deploy=True
        )
        ws_stage.grant_management_api_access(default_function)

        prompt_function = _lambda.Function(
            self, "PromptFunction",
            handler="on_sendmessage.handler",
            code=_lambda.Code.from_asset("functions"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.THREE_DAYS,
            initial_policy=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["bedrock:InvokeModelWithResponseStream"],
                    resources=["*"]
                )
            ]
        )
        ws_stage.grant_management_api_access(prompt_function)

        ws_api.add_route(
            integration=apigw2_int.WebSocketLambdaIntegration('PromptIntegration', prompt_function),
            route_key="sendmessage",
            return_response=True
        )

        CfnOutput(
            self, "WebSocketApiEndpoint",
            description="WebSocket API Endpoint",
            value=ws_stage.url
        )