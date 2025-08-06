# Anthropic-API
This project is a wrapper for Anthropic's Claude Sonnet v4 LLM chatbot. It's deployed using a serverless model on AWS Lambda and API Gateway. User session data is then stored to a DynamoDB table. 

The DDB table keeps track of user input, claude's responses, and the cost of using Anthropic's API. Anthropic uses 'tokens' to determine the pricing of a given API call; tokens measure the complexity of a given input or output. I calculate the cost of each interaction with Claude using the pricing on this page: [https://docs.anthropic.com/en/docs/about-claude/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing). The DDB tables stores:
- Lambda request ID (the partition key)
- Input tokens used
- Input cost (cents)
- Output tokens used
- Output cost (cents)
- User input
- Claude's response

# CI/CD
The core lambda function is automatically updated when changes are made to this github repo. An AWS CodeBuild project automatically builds a new zip file containing lambda_function.py along with its dependencies in requirements.txt, then uploads the artifact to an S3 bucket. When the build package is updated, a CodePipeline release is triggered that deploys the new version.
