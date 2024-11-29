import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_apigateway
)
from constructs import Construct


class UserAuthorizerCognito(Stack):

  def __init__(self, scope: Construct, construct_id: str, user_pool, lambda_fn, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    auth = aws_apigateway.CognitoUserPoolsAuthorizer(self, 'AuthorizerForProxyLambda',
      cognito_user_pools=[user_pool]
    )

    lambda_rest_api = aws_apigateway.LambdaRestApi(self, 'LambdaProxy',
      rest_api_name="lambda-api",
      handler=lambda_fn,
      proxy=False,
      deploy=True,
      deploy_options=aws_apigateway.StageOptions(stage_name="v1"),
      endpoint_export_name='ApiGatewayRestApiEndpoint'
    )

    hello = lambda_rest_api.root.add_resource("proxy")
    hello.add_method('POST',
      aws_apigateway.LambdaIntegration(
        handler=lambda_fn
      ),
      authorization_type=aws_apigateway.AuthorizationType.COGNITO,
      authorizer=auth
    )


    cdk.CfnOutput(self, 'RestApiEndpointUrl',
      value=lambda_rest_api.url,
      export_name=f'{self.stack_name}-RestApiEndpointUrl')
