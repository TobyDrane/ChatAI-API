# ChatAI-API

This is a very simple implementation of a FastAPI backend for a simple conversation with an LLM. Conversations can be created and their history persisted with the backend easily pluggable into an OpenAI model.

## Getting Started

Installs the required environment to test locally.

1. Ensure [pyenv](https://github.com/pyenv/pyenv) is installed and Docker is running
2. Run the setup command `make setup`
3. Install the Python virtual environment with the desired requirements `make venv`
4. Ensure you are in the virtual environment `source .venv/bin/activate`
5. Run the api locally `make api-run` you can then view the running API at the following http://0.0.0.0:8000/docs

## Testing Routes Locally

### Create new conversation

To create a new conversation and retrieve a conversation id to start chatting to you can `POST` the base conversations endpoint

```bash
curl -X POST localhost:8000/conversation
```

This will return a response like below

```bash
{
  "id": "248f789b-28cd-4cea-8c33-a2621430f81b",
  "messages": [],
  "created_at": "2023-12-04T17:28:52.678004Z"
}
```

### Chatting on a conversation

All messages are linked to conversations and are therefore persisted. When a conversation has been created and the conversation `id` generated you can create new messages

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "message": "What is the current day?",
  "stream": "false"
}' localhost:8000/conversation/completion/248f789b-28cd-4cea-8c33-a2621430f81b
```

This will generate a response like below

```bash
{
  "id": "d90aa31b-b4bc-46d1-8c39-8a06b3f7306c",
  "author": "assistant",
  "content": ".....",
  "created_at": "2023-12-04T17:31:19.842284Z"
}
```

#### Streaming

You can stream the response back enabling the stream parameter within the body object

```bash
curl -X POST -N -H "Content-Type: application/json" -d '{
  "message": "What is the current day?",
  "stream": "true"
}' localhost:8000/conversation/completion/248f789b-28cd-4cea-8c33-a2621430f81b
```

### Viewing Previous Conversations

To view previously persisted conversations you can make a `GET` request to the conversation endpoint

```bash
curl -X GET localhost:8000/conversation
```

This will generate a response like below

```bash
[
  {
    "id": "248f789b-28cd-4cea-8c33-a2621430f81b",
    "messages": [
      {
        "id": "08e6863d-1fa3-43b4-9175-2cb426ce84b5",
        "author": "user",
        "content": "What is the current day?",
        "created_at": "2023-12-04T17:34:35.567000"
      },
      {
        "id": "0b10fd23-e0aa-488d-8759-20dc5f1c01d6",
        "author": "assistant",
        "content": "Vel dolorem reprehenderit mollitia sit commodi consequuntur nobis qui. Similique doloremque molestiae quos consequatur quae debitis nobis neque. Sit ducimus atque id corporis est.",
        "created_at": "2023-12-04T17:34:35.639000"
      }
    ],
    "created_at": "2023-12-04T17:28:52.678000"
  }
]

```
