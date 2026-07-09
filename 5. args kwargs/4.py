def train(X, y, *, lr=0.01, epochs=10, verbose=False):
    return None

X_train = []
y_train = []
# Корректный вызов
train(X_train, y_train, lr=0.005, epochs=100, verbose=True)
# Неправильный вызов
try:
    train(X_train, y_train, 0.1)
except TypeError:
    print('Чтобы избежать путаницы в подборе гиперпараметров, каждый из них является keyword-only')