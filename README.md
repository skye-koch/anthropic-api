- API endpoint: https://6j0dej433e.execute-api.us-east-1.amazonaws.com/test/claude-sonnet

- Give claude a message: https://6j0dej433e.execute-api.us-east-1.amazonaws.com/test/claude-sonnet?message=text
  - The "message" parameter should be plain text, not wrapped in quotes e.g <https://6j0dej433e.execute-api.us-east-1.amazonaws.com/test/claude-sonnet?message=hello%20claude>

- The API will respond with two fields; "conversation_id" in uuid4 format, and "body", which is Claude's response.
- To continue your conversation with Claude, use the provided conversation id 
    - https://6j0dej433e.execute-api.us-east-1.amazonaws.com/test/claude-sonnet?message=more text&conversation_id=
