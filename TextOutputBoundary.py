class TextOutputBoundary:
    """
    Class with single method for outputting a string to an abstract boundary

    This class is an interface, the thing being written to could be anything

    """
    def write(self, text: any):
        raise NotImplementedError
