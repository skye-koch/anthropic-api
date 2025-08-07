# Anthropic-API
This project is a wrapper for Anthropic's Claude Sonnet v4 LLM. It's built using a serverless model on AWS Lambda, API Gateway, and DynamoDB. 
  1. Users interact with Claude using the API gateway endpoint.
  2. The anthropic API is called in the lambda function, and claude's response is returned to the user.
  3. Session data is stored in a DynamoDB table.

The DDB table keeps track of user input, claude's responses, and the cost of using Anthropic's API. Anthropic uses 'tokens' to determine the pricing of a given API call; tokens measure the complexity of a given input or output. I calculate the cost of each interaction with Claude using the pricing on this page: [https://docs.anthropic.com/en/docs/about-claude/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing). The DDB tables stores:
- Lambda request ID (the partition key)
- Input tokens used
- Input cost (cents)
- Output tokens used
- Output cost (cents)
- User input
- Claude's response

# CI/CD
The core lambda function is automatically updated when changes are made to this github repo. An AWS CodeBuild project automatically builds a new zip file containing lambda_function.py along with its dependencies in requirements.txt and uploads the artifact to an S3 bucket. When the build package is updated, a CodePipeline release is triggered that deploys the new version.

# Security & Cost Control
- My anthropic API key is stored in Secrets Manager and retrieved at runtime.
- This is a personal/educational project, so I've limited my Anthropic costs to $15/month via the Spend Limits setting in the anthropic console. However, this still allows me to process several million tokens per month with current pricing; $3/MTok for input and $15/MTok for output.
- I've also throttled my API gateway endpoint to allow 5 requests/second.
