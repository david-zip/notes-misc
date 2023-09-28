# AWS Lambda

## Environment Variables

Environment variables can be used to adjust Lambda function behaviour without needing to make adjustments on the code. It is a pair of strings that is stored externally from the code (in a function version-specific configuration). When a version is published, the environment variables are locked for that version.

Any value defined as an environment variable will be considered a literal string.

The key of environment variables can be retrive using the following code (using Python):

``` python
import os

environment_variable_value = os.environ["environment variable key"]
```

Lambda stores environment variables securely by encrypting them at rest.

## How to Trigger Lambda Functions using other Lambda Functions

One way to trigger other Lambda functions within a Lambda function is by using the `invoke` method from the **AWS SDK library**. This allows for chains of Lambda functions to be trigger based certain conditions and events.

The general guideline of triggering other Lambda function goes as follows:

1. Import **AWS SDK** libraries into the Lambda function
    * For Python, import `boto3`
2. Call `invoke` method to trigger desired Lambda function
    * Specify target function ARN

``` python
import boto3

def lambda_handler(event, context):
    # configure AWS SDK environemnt
    client = boto3.client('lambda', region_name='eu-west-2')

    # call the target function lambda
    target_lambda_fctn = 'target-function-arn'

    # if required, package the data that needs to be sent to the other lambda function
    input_data = {'key': 'value'}

    # trigger the target function
    response = client.invoke(
        FunctionName=target_lambda_fctn,
        InvocationType='Event', # use RequestResponse for synchronous invocation
        Payload=json.dump(input_data)
    )

    # process the response (if needed)
    if 'Payload' in response:
        result = json.loads(response['Payload'].read())
        # do whatever you want with one 

    return 'Triggered Lambda function successfully!'
```

`invoke` will invoke a Lambda function synchronously (wait for its response) or asynchronously.

``` py
response = client.invoke(
    FunctionName='string',
    InvocationType='string',
    LogType='string',
    ClientContext='string',
    Payload=json.dump(dict()),
    Qualifier='string'
    )
```

`invoke` method arguments (*italic* is the default argument option)

* **FunctionName (string) (required)**: input *Lambda function ARN*

* **InvocationType (string)**: specifies invocation method from one of the below

  * *`RequestResponse`* - Invoke function synchronously (keeps request open until the function returns a response or times out)

  * `Event` - Invoke the function asynchronously (API response will only include status code)

  * `DryRun` - Validate parameter calues and verify that the user or role has permission to invoke the function

* **LogType (string)**: specifies whether you want to log execution details (applies to synchronously invoked functions only)

  * *`None`* - No logging

  * `Tail` - Include execution log in response

* **ClientContext (string)**: up to 3,583 bytes of base64-encoded data about the invoking client is pass to the function in the context object *(I dont understand look up more)*

* **Payload (bytes or seekable file-like object)**: JSON file you want to provide as an input to the invoked Lambda function

* **Qualifier (string)**: specify a version or alias to invoke a published version of function

Function returns a `dict` with the following response:

``` py
{
    'StatusCode': 123,
    'FunctionError': 'string',
    'LogResult': 'string',
    'PayLoad': StreamingBody(),
    'ExecutedVersion': 'string'
}
```

`response` dictionary keys

* **StatusCode (int)**: HTTP status in the range of 200 signifies sucessful request

  * `200` - Sucessful `RequestResponse`

  * `202` - Sucessful `Event`

  * `204` - Sucessful `DryRun`

* **FunctionError (string)**: if present, indicates the error that occured during the fucntion execution (details about the error can be found in `PayLoad`)

* **LogResults (string)**: last 4KB of the execution log (base64-encoded)

* **PayLoad (StreamingBody)**: response from the function, or an error object

* **ExecutedVersion (string)**: version of function invoked

### IAM Permissions for Invoking Lambda Function

When invoking other Lambda funtions within a Lambda function, ensure that necessary IAM permissions have been allocated. The source Lambda function should have the `lambda:InvokeFunction' permissions for the target Lambda function.

Example policy:

``` json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": "designated-lambda-function-arn"
        }
    ]
}
```

## AWS Lambda Destinations

After executing a Lambda function, you can send the invocation report to other downstream AWS Services. This feature allows for users to asynchronously invoke various AWS services. The following services that can be destinations are:

* Amazon SQS
* Amazon SNS
* Amazon Lambda
* Amazon Eventbridge

The execution records will contain details about the request and response in JSON format. AWS Lambda Destination will send the execution records to one of the above services whether the execution succeded or failed.

If the execution fails, the Lambda function will continue to invoke the Lambda function a maximum number or times or until the event expires in the queue. Otherwise, *Dead Letter Queues* (DLQ) are a great way of handling asynchronous Lambda failures.

Example of successful invocation:

``` json
{
 "version": "1.0",
 "timestamp": "2019-11-24T23:08:25.651Z",
 "requestContext": {
  "requestId": "c2a6f2ae-7dbb-4d22-8782-d0485c9877e2",
  "functionArn": "arn:aws:lambda:sa-east-1:123456789123:function:event-destinations:$LATEST",
  "condition": "Success",
  "approximateInvokeCount": 1
 },
 "requestPayload": {
  "Success": true
 },
 "responseContext": {
  "statusCode": 200,
  "executedVersion": "$LATEST"
 },
 "responsePayload": null
}
```

Example of unsuccessful invocation:

``` json
{
    "version": "1.0",
    "timestamp": "2019-11-24T21:52:47.333Z",
    "requestContext": {
        "requestId": "8ea123e4-1db7-4aca-ad10-d9ca1234c1fd",
        "functionArn": "arn:aws:lambda:sa-east-1:123456678912:function:event-destinations:$LATEST",
        "condition": "RetriesExhausted",
        "approximateInvokeCount": 3
    },
    "requestPayload": {
        "Success": false
    },
    "responseContext": {
        "statusCode": 200,
        "executedVersion": "$LATEST",
        "functionError": "Handled"
    },
    "responsePayload": {
        "errorMessage": "Failure from event, Success = false, I am failing!",
        "errorType": "Error",
        "stackTrace": [ "exports.handler (/var/task/index.js:18:18)" ]
    }
}
```

The format of the JSON file that is passed to the destination will vary depending on the AWS service:

* SNS/SQS - Passed as a `Message` to the destination
* Lambda - Passed as a `Payload` to the function
* Eventbridge - Passed as the `Detail` in PutEvents call
  * Source is `Lambda`
  * Detail type is either:
    * `Lambda Function Invocation Result - Success`
    * `Lambda Function Invocation Result - Failure`

### IAM Permissions for AWS Lambda Destintion

The following IAM permissions must be provided so that the Lambda function is allowed to send invocation results to the destination function.

When invoking other Lambda funtions within a Lambda function, ensure that necessary IAM permissions have been allocated. The source Lambda function should have the `lambda:InvokeFunction' permissions for the target Lambda function.

``` YAML
Resources: 
  EventInvokeConfig:
    Type: AWS::Lambda::EventInvokeConfig
    Properties:
        FunctionName: “YourLambdaFunctionWithEventInvokeConfig”
        Qualifier: "$LATEST"
        MaximumEventAgeInSeconds: 600
        MaximumRetryAttempts: 0
        DestinationConfig:
            OnSuccess:
                Destination: “arn:aws:sns:us-east-1:123456789012:YourSNSTopicOnSuccess”
            OnFailure:
                Destination: “arn:aws:lambda:us-east-1:123456789012:function:YourLambdaFunctionOnFailure”
```

The permissions will also vary depending on what service is getting the records.

* Amazon SQS: sqs:SendMessage
* Amazon SNS: sns:Publish
* Lambda: InvokeFunction
* Eventbridge: event:PutEvents

### Asynchronous Invocation

For asynchronous invocation, Lambda places the event in a queue and returns a success response without additional information. A separate process reads events from the queue and sends them to your function. If an error is experienced, Lambda will attempt to run it two more times, with a one minute wait between first two attempts. It will continue to attempt execution two more times with a two minute gap inbetween invocation. This continues for another 6 hours with the maximum wait time between functions reaching five minutes.

If the queue gets very long, new events might age out before the Lambda function gets a chance to execute the event. If an event expires or fails all processing attempts, Lambda will discard of it.

### Dead Letter Queues

As an alternative to on-failure destination, dead letter queues can be used to save discared events for further processing. Dead letter queues are only used when an event fails all processing attempts or expires without being processed.

Events in dead letter queues can be reprocessed by setting the failed events as event sources for Lambda functions. Alternatively, events can be manually retrieved.

Both Amazon SQS standard queue and Amazon SNS standard topic can be used as dead letter queues. One of the two can use depending on the project specification.

* Amazon SQS Queue
  * Queue that holds failed events until retrieved
  * Better if only a single entity is processing events

* Amazon SNS Topic
  * Topic relays failed events to one or more destinations
  * Better if multiple entities are expected to fail

In order to send a policy, the fucntion will require additional permissions:

* Amazon SQS - `sqs:SendMessage`
* Amazon SNS - `sns:Publish`

When setting up th dead letter queue, there will be three editable attributes:

* **RequestID (string)**: ID of invocation request
* **ErrorCode (int)**:  HTTP status code
* **ErrorMessage (string)**: First 1KB of error message

If Lambda is unable to send the error message (due to lack of permissions) to the dead-letter queue, it will delete the event and omit the `DeadLetterErrors` metric.

