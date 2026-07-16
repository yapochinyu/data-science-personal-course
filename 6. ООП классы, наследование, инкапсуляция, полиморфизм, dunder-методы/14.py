class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name\
        
    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.name == other.name and self.user_id == other.user_id
    
    def __hash__(self):
        return hash(self.user_id)


if __name__ == '__main__':
    u1 = User(1, 'Anna')
    u2 = User(1, 'Anna')
    u3 = User(2, 'Boris')

    # равенство по полям, а не по identity
    assert u1 == u2
    assert u1 is not u2
    assert u1 != u3
    assert u1 != 'not a user'

    # объект хешируем — можно класть в set/dict
    users = {u1: 'admin'}
    assert users[u2] == 'admin'  # u2 == u1 и hash(u2) == hash(u1)

    s = {u1, u2, u3}
    assert len(s) == 2  # u1 и u2 равны -> в set один элемент

    assert hash(u1) == hash(u2)
    assert hash(u1) == hash(User(1, 'другое_имя'))  # хеш зависит только от user_id

    print('all tests passed')