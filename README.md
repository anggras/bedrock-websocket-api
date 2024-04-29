
# Welcome to Amazon Bedrock WebSocket API sample project

This is a sample project to showcase how to expose Amazon Bedrock response stream through API Gateway WebSocket API

> [!NOTE]
> In this example, we are using the `meta.llama3-8b-instruct-v1:0` model. You can modify the model to be used in [on_sendmessage.py](functions/on_sendmessage.py) or [request for access](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess) using the console. 

> [!TIP]
> To quickly test the WebSocket connection, you can use [wscat](https://github.com/websockets/wscat) or Postman. 

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
