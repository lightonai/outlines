from openai import OpenAI
import json
import pytest

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
model = models.data[0].id

schema = """{
    "title": "Character",
    "type": "object",
    "properties": {
        "name": {
            "title": "Name",
            "maxLength": 10,
            "type": "string"
        },
        "age": {
            "title": "Age",
            "type": "integer"
        },
        "armor": {"$ref": "#/definitions/Armor"},
        "weapon": {"$ref": "#/definitions/Weapon"},
        "strength": {
            "title": "Strength",
            "type": "integer"
        }
    },
    "required": ["name", "age", "armor", "weapon", "strength"],
    "definitions": {
        "Armor": {
            "title": "Armor",
            "description": "An enumeration.",
            "enum": ["leather", "chainmail", "plate"],
            "type": "string"
        },
        "Weapon": {
            "title": "Weapon",
            "description": "An enumeration.",
            "enum": ["sword", "axe", "mace", "spear", "bow", "crossbow"],
            "type": "string"
        }
    }
}"""
regex = "(-)?(0|[1-9][0-9]*)(\\.[0-9]+)?([eE][+-][0-9]+)?"


@pytest.mark.parametrize("stream", [False, True])
def test_completion(stream):
    print(f"=== Completion (stream={stream}) ===")
    completion = client.completions.create(
        model=model,
        temperature=0.0,
        max_tokens=100,
        prompt="Give me a character.",
        echo=False,
        stream=stream,
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())


@pytest.mark.parametrize("stream", [False, True])
def test_completion_json(stream):
    print(f"=== Completion JSON (stream={stream}) ===")
    completion = client.completions.create(
        model=model,
        temperature=0.0,
        max_tokens=100,
        prompt="Give me a character.",
        echo=False,
        stream=stream,
        extra_body={
            "json_schema": schema,
        },
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())
        print(json.loads(completion.choices[0].text))


@pytest.mark.parametrize("stream", [False, True])
def test_completion_regex(stream):
    print(f"=== Completion Regex (stream={stream}) ===")
    completion = client.completions.create(
        model=model,
        temperature=0.0,
        max_tokens=100,
        prompt="Give me the 10 first digits of PI: ",
        echo=False,
        stream=stream,
        extra_body={
            "regex": regex,
        },
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())


@pytest.mark.parametrize("stream", [False, True])
def test_chat(stream):
    print(f"=== Chat (stream={stream}) ===")
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Give me a character."},
        ],
        model=model,
        stream=stream,
        max_tokens=100,
        temperature=0.0,
        stop=["</s>"],
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())


@pytest.mark.parametrize("stream", [False, True])
def test_chat_json(stream):
    print(f"=== Chat JSON (stream={stream}) ===")
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Give me a character with a strength of 124."},
        ],
        model=model,
        stream=stream,
        max_tokens=100,
        temperature=0.0,
        stop=["</s>"],
        extra_body={
            "json_schema": schema,
        },
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())
        print(json.loads(completion.choices[0].message.content))


@pytest.mark.parametrize("stream", [False, True])
def test_chat_regex(stream):
    print(f"=== Chat Regex (stream={stream}) ===")
    completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Give me the 10 first digits of PI."},
        ],
        model=model,
        stream=stream,
        max_tokens=100,
        temperature=0.0,
        stop=["</s>"],
        extra_body={
            "regex": regex,
        },
    )
    if stream:
        for c in completion:
            print(c.model_dump_json())
    else:
        print(completion.model_dump_json())
