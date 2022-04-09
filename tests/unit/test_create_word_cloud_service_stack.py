import aws_cdk as core
import aws_cdk.assertions as assertions

from create_word_cloud_service.create_word_cloud_service_stack import CreateWordCloudServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in create_word_cloud_service/create_word_cloud_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CreateWordCloudServiceStack(app, "create-word-cloud-service")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
