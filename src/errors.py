class AyyashError(Exception):
    """Custom exception class for specific errors."""
    
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"CustomError: {self.message}"
