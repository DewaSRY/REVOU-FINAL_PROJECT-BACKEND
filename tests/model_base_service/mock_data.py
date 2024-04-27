from dataclasses import dataclass, field


@dataclass
class MockData:
    name: str
    username: str = field(default_factory=lambda: "hallo")
    id: int = field(init=False, default_factory=lambda: 1000)

    def halloo():
        print("hallo")
