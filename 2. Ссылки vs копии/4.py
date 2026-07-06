import copy

base_configs = [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]


def clone_and_bump_lr_wrong(configs, factor):
    bumped_configs = configs.copy()
    for config in bumped_configs:
        config['lr'] *= factor
    return bumped_configs


def clone_and_bump_lr(configs, factor):

    bumped_configs = copy.deepcopy(configs)
    for config in bumped_configs:
        config['lr'] *= factor
    return bumped_configs

def clone_and_bump_lr_cheap(configs, factor):
    return [{**config, 'lr': config['lr'] * factor} for config in configs]


if __name__ == '__main__':
    wrong_result = clone_and_bump_lr_wrong(base_configs, 10)
    assert base_configs == [{'lr': 0.1, 'epochs': 10}, {'lr': 1.0, 'epochs': 5}]
    assert wrong_result[0] is base_configs[0]

    base_configs = [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]
    result = clone_and_bump_lr(base_configs, 10)
    assert result == [{'lr': 0.1, 'epochs': 10}, {'lr': 1.0, 'epochs': 5}]
    assert base_configs == [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]
    assert result[0] is not base_configs[0]


    result = clone_and_bump_lr_cheap(base_configs, 10)
    assert result == [{'lr': 0.1, 'epochs': 10}, {'lr': 1.0, 'epochs': 5}]
    assert base_configs == [{'lr': 0.01, 'epochs': 10}, {'lr': 0.1, 'epochs': 5}]
    assert result[0] is not base_configs[0]
    
    print("все тесты прошли")