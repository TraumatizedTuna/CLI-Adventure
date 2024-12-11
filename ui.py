class UI:
    @staticmethod
    def next(): pass

    @staticmethod
    def set_loc(loc_name: str):
        print('--------------------------------------------------\n\n'+loc_name)

    @staticmethod
    def get_user_input(info: str, next: callable, *args):
        UI.next = next
        UI.args = args
        print(info)
        next(input(), *args)
