from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class MockData:
    name: str = field(default_factory=lambda: "hallo")
    username: str = field(default_factory=lambda: "hallo")
    id: int = field(init=False, default_factory=lambda: str(uuid4()))

    def halloo():
        print("hallo")


# @dataclass
# class UpdateData(MockData):
#     test: str = field(default_factory=lambda: "hallo")

#     def __init__(self, data: MockData):
#         super().__init__(**data)
#         self.test = "hallo"
