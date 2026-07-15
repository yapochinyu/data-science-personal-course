class Experiment:
    total_experiments = 0

    def __init__(self, metrics=None):
        Experiment.total_experiments += 1
        if metrics is None:
            self.metrics = []
        else:
            self.metrics = metrics


if __name__ == '__main__':
    e1 = Experiment()
    e2 = Experiment()
    e3 = Experiment(['acc'])

    # счётчик общий на всех
    assert Experiment.total_experiments == 3
    assert e1.total_experiments == 3
    assert e2.total_experiments == 3
    assert e3.total_experiments == 3

    # metrics — независимые у каждого экземпляра
    e1.metrics.append('loss')
    assert e1.metrics == ['loss']
    assert e2.metrics == []
    assert e3.metrics == ['acc']

    # дефолтный список не расшарен между экземплярами (мина изменяемого дефолта)
    e4 = Experiment()
    assert e4.metrics == []

    print('OK')

