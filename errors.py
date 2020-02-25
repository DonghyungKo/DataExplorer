class ParameterTypeError(Exception):
    ''' 파라미터 타입이 일치하지 않을 경우 발생하는 예외 '''

    def __init__(self, msg="파라미터 타입이 일치하지 않습니다."):
        self.msg = msg

    def __str__(self):
        return self.msg


class IndexTypeError(Exception):
    def __init__(self, msg="Index 타입이 일치하지 않습니다."):

        self.msg = msg

    def __str__(self):
        return self.msg
