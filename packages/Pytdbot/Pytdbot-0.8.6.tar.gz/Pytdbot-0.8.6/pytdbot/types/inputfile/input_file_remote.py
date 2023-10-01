from .base import InputFile


class InputFileRemote(InputFile):
    """A file defined by its remote ID. The remote ID is guaranteed to be usable only if the corresponding file is still accessible to the user and known to TDLib. For example, if the file is from a message, then the message must be not deleted and accessible to the user. If the file database is disabled, then the corresponding object with the file must be preloaded by the application

    Args:
        id (``str``):
            The remote ID of the file
    """

    def __init__(self, id: str) -> None:
        self.id = id
        self.data = {"@type": "inputFileRemote", "id": self.id}
