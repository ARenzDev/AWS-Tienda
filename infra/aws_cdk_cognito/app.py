import os

from cognito import cognitoPoolUser
from apiLambda import ApiLambdaProxy
from UserAuthorizerCognito import UserAuthorizerCognito
from registroTiendasCdk import RegistroTiendasCdkStack
import aws_cdk as cdk


APP_ENV = cdk.Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')
)

app = cdk.App()

user_pool_stack = cognitoPoolUser(app, "cognitoPoolUser",
  env=APP_ENV
)

lambda_apigw_stack = ApiLambdaProxy(app, "ApiLambdaProxy",
  env=APP_ENV
)
lambda_apigw_stack.add_dependency(user_pool_stack)

apigw_stack = UserAuthorizerCognito(app, "UserAuthorizerCognito",
  user_pool_stack.user_pool,
  lambda_apigw_stack.lambda_fn,
  env=APP_ENV
)
apigw_stack.add_dependency(lambda_apigw_stack)

registroTienda_stack = RegistroTiendasCdkStack(app, "RegistroTiendasCdkStack",
  env=APP_ENV
)
registroTienda_stack.add_dependency(lambda_apigw_stack)

app.synth()