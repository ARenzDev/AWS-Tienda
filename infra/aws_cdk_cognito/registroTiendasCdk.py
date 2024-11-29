import os
import aws_cdk as cdk
from aws_cdk import (
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    Stack,
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
        tienda1_event_rule = events.Rule(
            self, "TiendaEventRule",
            event_bus=event_bus,
            event_pattern={
                "source": ["tienda.registration"],
                "detail-type": ["Productos1 registrado"]
            }
        )
        tienda1_event_rule.add_target(targets.LambdaFunction(process_tienda1_lambda))

        # Regla para eventos de frutas
        tienda2_event_rule = events.Rule(
            self, "Tienda2EventRule",
            event_bus=event_bus,
            event_pattern={
                "source": ["tienda2.registration"],
                "detail-type": ["Productos2 registrado"]
            }
        )
        tienda2_event_rule.add_target(targets.LambdaFunction(process_tienda2_lambda))

        # Salidas
        cdk.CfnOutput(self, "EventBusName", value=event_bus.event_bus_name)