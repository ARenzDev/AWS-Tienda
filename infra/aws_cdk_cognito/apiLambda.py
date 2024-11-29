import os

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_lambda,
  aws_events as events,
  aws_events_targets as targets
)
from constructs import Construct


class ApiLambdaProxy(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)
    event_bus = events.EventBus(
        self, "MyEventBus",
        event_bus_name="MyCustomEventBus"
    )
    lambda_proxy_fn = aws_lambda.Function(self, 'ApiLambdaProxyFn',
      runtime=aws_lambda.Runtime.PYTHON_3_9,
      function_name="ApiLambdaProxy",
      handler="proxy.lambda_handler",
      description='Funcion de proxy lambda"',
      code=aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), './src/main/lambdas')),
      environment={
                "EVENT_BUS_NAME": event_bus.event_bus_name
      },
      timeout=cdk.Duration.minutes(5)
    )
    
    regla_evento = events.Rule(self, 'ReglaEvento',  
            event_pattern={  
                "source": ["custom.api.proxy"],  
            }  
    ) 
    # regla_evento.add_target(targets.EventBus(event_bus.event_bus_name))
    # lambda_proxy_fn.grant_invoke(event_bus.event_bus_arn)
    
    regla_evento.add_target(targets.EventBus(event_bus))  

    # Permitir que la función Lambda envíe eventos al EventBus  
    event_bus.grant_all_put_events(lambda_proxy_fn)  
    self.lambda_fn = lambda_proxy_fn


    cdk.CfnOutput(self, 'LambdaFuncName',
      value=self.lambda_fn.function_name,
      export_name=f'{self.stack_name}-LambdaFuncName')