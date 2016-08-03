# logstash-aws-cloudwatch
##### AWS Lambda function for sending AWS CloudWatch logs to logstash in near real-time for processing and analysing

###### Example use cases:
* Forwarding AWS VPC flow Logs
* Forwarding AWS Lambda function logs
* [Forwarding AWS CloudTrail logs](http://docs.aws.amazon.com/awscloudtrail/latest/userguide/send-cloudtrail-events-to-cloudwatch-logs.html)
* Forwarding any other AWS CloudWatch logs

## Deploy the script on AWS Lambda
1. Create a new Lambda function

   ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step1.png)

2. On the "Select Blueprint" screen, press "Skip"

   ![Choose Blueprint](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step2.png)

3. Configure function:
   * Give your function a name
   * Set runtime to Python 2.7

   ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step3.png)

4. Edit code:
   * Edit the contents of ```logstash_config.py```
   * Replace values of ```log_token``` and ```debug_token``` with tokens obtained earlier.
   * Create a .ZIP file, containing the updated ```logstash_config.py```, ```logstash_cloudwatch.py``` and ```logstash_certs.pem```
     * Make sure the files are in the root of the ZIP archive, and **NOT** in a folder
   * Choose "Upload a .ZIP file" in AWS Lambda and upload the archive created in previous step

   ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step4.png)

5. Lambda function handler and role
   * Change the "Handler" value to ```logstash_cloudwatch.lambda_handler```
   * Create a new basic execution role (your IAM user must have sufficient permissions to create & assign new roles)

   ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step5.png)

6. Allocate resources:
   * Set memory to 128 MB
   * Set timeout to ~2 minutes (script only runs for seconds at a time)

  ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step7.png)

8. Enable function:
   * Click "Create function"

   ![Create Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step8.png)

## Configure CloudWatch Stream
1. Create a new stream:
   * Select CloudWatch log group
   * Navigate to "Actions / Stream to AWS Lambda"

   ![Stream to Lambda](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step9.png)

2. Choose destination Lambda function:
   * Select the AWS Lambda function deployed earlier from drop down menu
   * Click "Next" at the bottom of the page

   ![Select Function](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step10.png)

3. Configure log format:
   * Choose the correct log format from drop down menu
   * Specify subscription filter pattern
     * [Please see AWS Documentation for more details](http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html)
     * If this is blank / incorrect, only raw data will be forwarded to logstash
     * Amazon provide preconfigured filter patterns for some logs
   * Click "Next" at the bottom of the page

   ![Log Format](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step11.png)

4. Review and start log stream
   * Review your configuration and click "Start Streaming" at the bottom of the page

   ![Start stream](https://raw.githubusercontent.com/imduffy15/logstash-aws-cloudwatch/master/doc/step6.png)

5. Watch your logs come in:
   * Navigate to [your logstash account](https://logentries.com/app) and watch your CloudWatch logs appear
