class Messages:
    def __init__(self) -> None:
        pass

    @staticmethod
    def notify_new_user(name:str):
        response = {'status':'new_user', 'data':name}