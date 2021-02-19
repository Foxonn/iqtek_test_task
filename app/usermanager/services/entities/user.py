class User:
    def __init__(
            self,
            id: int = None,
            *,
            first_name: str,
            middle_name: str,
            last_name: str,
    ):
        self.id = id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name

    def __repr__(self):
        return "<object %s: id=%s>" % (self.__class__.__name__, self.id)


if __name__ == '__main__':
    user = User(first_name='ivan', middle_name='ivanovich', last_name='ivanov')
    print(user)
