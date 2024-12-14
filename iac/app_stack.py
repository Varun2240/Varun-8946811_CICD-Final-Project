from aws_cdk import (
    App, Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_apigateway as apigateway
)
from constructs import Construct

class AppStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 bucket for frontend
        frontend_bucket = s3.Bucket(self, "FrontendBucket",
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            )
        )

        # VPC and EC2 for backend
        vpc = ec2.Vpc(self, "AppVpc", max_azs=2)
        
        # Security group to allow HTTP traffic to the EC2 instance
        sg = ec2.SecurityGroup(self, "InstanceSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")
        
        instance = ec2.Instance(self, "BackendInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            security_group=sg
        )

        # Assign Elastic IP for the instance (public access)
        eip = ec2.CfnEIP(self, "ElasticIP", instance_id=instance.instance_id)

        # API Gateway with HTTP Integration pointing to the EC2 instance's public IP
        api = apigateway.RestApi(self, "AppApi")
        integration = apigateway.HttpIntegration(f"http://{eip.ref}")  # Use the EIP for public access
        api.root.add_method("GET", integration)
        
# Define the app
app = App()
AppStack(app, "MyAppStack")

app.synth()