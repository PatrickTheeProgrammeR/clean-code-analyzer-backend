class AIProviderError(Exception):
    """Raised when OpenAI API fails (connection, auth, rate limit)"""
    pass


class InvalidAIResponseError(Exception):
    """Raised when AI returns unexpected or unparseable response"""
    pass


class InvalidCodeInputError(Exception):
    """Raised when user input is not valid code for analysis"""
    pass