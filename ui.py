class UI:

    @staticmethod
    def set_loc(loc_name: str):
        print('--------------------------------------------------\n\n'+loc_name)

    @staticmethod
    def get_user_input(info: str, next: callable, *args):
        print(info)
        next(input(), *args)
