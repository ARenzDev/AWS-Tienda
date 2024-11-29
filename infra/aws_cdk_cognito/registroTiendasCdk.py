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

        # Crear un EventBridge Bus
        event_bus = events.EventBus.from_event_bus_name(
            self, "ExisteEventBus", "MyCustomEventBus"
        )
        # Lambda para crear registros de animales
        crear_tienda_lambda = _lambda.Function(
            self, "RegistrarTienda1Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="tienda.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name
            }
        )

        # Lambda para crear registros de frutas
        crear_tienda2_lambda = _lambda.Function(
            self, "RegistrarTienda2Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="tienda2.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
            environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name
            }
        )

        # Lambda para procesar registros de animales
        process_tienda1_lambda = _lambda.Function(
            self, "ProcessTienda1Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="process_tienda1.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
        )

        # Lambda para procesar registros de frutas
        process_tienda2_lambda = _lambda.Function(
            self, "ProcessTienda2Function",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="process_tienda2.handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
        )

        # Permitir a las Lambdas publicar eventos en el EventBus
        event_bus.grant_put_events_to(crear_tienda_lambda)
        event_bus.grant_put_events_to(crear_tienda2_lambda)

        # Regla para eventos de animales
        # Definimos el patrón de eventos correctamente
        event_pattern = events.EventPattern(
            source=["tienda.registration"],
            detail_type=["Productos1 registrado"]
        )

        # Creamos la regla de eventos con el patrón adecuado
        tienda1_event_rule = events.Rule(
            self, "TiendaEventRule",
            event_bus=event_bus,
            event_pattern=event_pattern
        )
        tienda1_event_rule.add_target(targets.LambdaFunction(process_tienda1_lambda))
        

        # Regla para eventos de frutas
        # Definimos el patrón de eventos correctamente
        event_pattern = events.EventPattern(
            source=["tienda2.registration"],
            detail_type=["Productos2 registrado"]
        )

        # Creamos la regla de eventos con el patrón adecuado
        tienda2_event_rule = events.Rule(
            self, "Tienda2EventRule",
            event_bus=event_bus,
            event_pattern=event_pattern
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
                name="id_pk2", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        global_table.grant_full_access(crear_tienda_lambda)
        global_table2.grant_full_access(crear_tienda2_lambda)

        # Salidas
        cdk.CfnOutput(self, "EventBusName", value=event_bus.event_bus_name)
