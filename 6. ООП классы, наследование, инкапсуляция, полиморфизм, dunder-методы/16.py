from dataclasses import dataclass, field


@dataclass
class TrainConfig:
    lr: float = 0.01
    epochs: int = 10
    batch_size: int = 32
    callbacks: list = field(default_factory=list)


if __name__ == '__main__':
    c1 = TrainConfig()

    # __repr__ появился бесплатно
    assert repr(c1) == 'TrainConfig(lr=0.01, epochs=10, batch_size=32, callbacks=[])'

    # __eq__ появился бесплатно: сравнение по полям, а не по identity
    c2 = TrainConfig()
    assert c1 == c2
    assert c1 is not c2

    c3 = TrainConfig(lr=0.1)
    assert c1 != c3

    # default_factory даёт каждому объекту свой независимый список
    c1.callbacks.append('early_stop')
    assert c1.callbacks == ['early_stop']
    assert c2.callbacks == []  # не затронут

    # обычные позиционные/именованные аргументы конструктора работают как обычно
    c4 = TrainConfig(0.05, 20, 64)
    assert c4.lr == 0.05
    assert c4.epochs == 20
    assert c4.batch_size == 64

    print('all tests passed')