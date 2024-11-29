import os
import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    Stack,
    aws_dynamodb as dynamodb
)
from constructs import Construct

class RegistroTiendasCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        event_bus = events.EventBus.from_event_bus_name(
            self, "ExisteEventBus", "MyCustomEventBus"
        )
        
        crear_tienda_lambda = _lambda.Function(
            self, "RegistrarTienda1Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="tienda.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name
            }
        )

        
        crear_tienda2_lambda = _lambda.Function(
            self, "RegistrarTienda2Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="tienda2.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name
            }
        )

        
        process_tienda1_lambda = _lambda.Function(
            self, "ProcessTienda1Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="process_tienda1.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
        )

        
        process_tienda2_lambda = _lambda.Function(
            self, "ProcessTienda2Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="process_tienda2.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
        )

        # Permitir a las Lambdas publicar eventos en el EventBus
        event_bus.grant_put_events_to(crear_tienda_lambda)
        event_bus.grant_put_events_to(crear_tienda2_lambda)

        # event_pattern1 = events.EventPattern(
        #     source=["tienda.registration"],
        #     detail_type=["Productos1 registrado"]
        # )
        
        # event_pattern2 = events.EventPattern(
        #     source=["tienda.registration"],
        #     detail_type=["Productos1 registrado"]
        # )
        
        tienda1_event_rule = events.Rule(
            self, "TiendaEvent",
            event_pattern={  
                "source": ["tienda.registration"],  
            }  
        )
        tienda1_event_rule.add_target(targets.LambdaFunction(process_tienda1_lambda))

        
        tienda2_event_rule = events.Rule(
            self, "Tienda2Event",
            event_pattern={  
                "source": ["tienda2.registration"],  
            }  
        )
        tienda2_event_rule.add_target(targets.LambdaFunction(process_tienda2_lambda))

        
        global_table = dynamodb.TableV2(
            self,
            id="GlobalTable",
            table_name="tienda1",
            billing=dynamodb.Billing.on_demand(),
            partition_key=dynamodb.Attribute(
                name="id_pk", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
        global_table2 = dynamodb.TableV2(
            self,
            id="GlobalTable2",
            table_name="tienda2",
            billing=dynamodb.Billing.on_demand(),
            partition_key=dynamodb.Attribute(
                name="id_pk", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        global_table.grant_full_access(crear_tienda_lambda)
        global_table2.grant_full_access(crear_tienda2_lambda)
        
        # Salidas
        cdk.CfnOutput(self, "tiendaLambdaARN", value=crear_tienda_lambda.function_arn)
        cdk.CfnOutput(self, "tienda2LambdaARN", value=crear_tienda2_lambda.function_arn)