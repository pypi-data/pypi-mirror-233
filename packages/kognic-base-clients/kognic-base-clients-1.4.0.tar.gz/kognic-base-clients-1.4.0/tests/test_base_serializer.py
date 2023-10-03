from typing import List

from kognic.base_clients.models import BaseSerializer


class Task(BaseSerializer):
    task_name: str
    task_uuid: str


class User(BaseSerializer):
    user_name: str
    age: int
    tasks: List[Task]


user_dict_snake = {
    "user_name": "John Doe",
    "age": 42,
    "tasks": [{"task_name": "Task 1", "task_uuid": "uuid1"}, {"task_name": "Task 2", "task_uuid": "uuid2"}],
}

user_dict_camel = {
    "userName": "John Doe",
    "age": 42,
    "tasks": [{"taskName": "Task 1", "taskUuid": "uuid1"}, {"taskName": "Task 2", "taskUuid": "uuid2"}],
}

user_model = User(
    user_name="John Doe",
    age=42,
    tasks=[Task(task_name="Task 1", task_uuid="uuid1"), Task(task_name="Task 2", task_uuid="uuid2")],
)


def test_serialize_user_snake():
    user = User.from_json(user_dict_snake)
    assert user == user_model


def test_serialize_user_camel():
    user = User.from_json(user_dict_camel)
    assert user == user_model


# Should deserialize to camel case
def test_deserialize_user():
    user = user_model.to_dict()
    assert user == user_dict_camel
