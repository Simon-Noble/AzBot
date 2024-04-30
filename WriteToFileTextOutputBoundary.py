from TextOutputBoundary import TextOutputBoundary


class WriteToFileTextOutputBoundary(TextOutputBoundary):

    file_name: str  # Name of file to write to

    def __init__(self, file_name: str):
        self.file_name = file_name

    def write(self, text: str):
        with open(self.file_name, mode="w") as f:
            f.write(text)
