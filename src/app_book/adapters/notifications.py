from typing import Protocol


class INotification(Protocol):
    async def send(self, destination: str, message: str) -> None: ...


class EmailNotification:
    async def send(self, destination: str, message: str) -> None:
        print(f"Sending email to {destination}: {message}")


class TestNotification:
    async def send(self, destination: str, message: str) -> None:
        # I can use this for testing purposes
        ...
