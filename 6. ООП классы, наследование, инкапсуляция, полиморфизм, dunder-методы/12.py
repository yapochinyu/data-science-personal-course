class CSVDataset:
    def __init__(self, lines):
        self.lines = lines

    def __len__(self):
        return len(self.lines)
    
    def __getitem__(self, i):
        return float(self.lines[i].split(',')[0]), int(self.lines[i].split(',')[1])
    


def simple_loader(dataset, batch_size):
    for i in range(0, len(dataset), batch_size):
        end = min(i + batch_size, len(dataset))
        batch = [dataset[x] for x in range(i, end)]
        yield batch


if __name__ == '__main__':
    ds = CSVDataset(['1.5,0', '2.5,1', '3.5,0', '4.5,1', '5.5,0'])

    assert len(ds) == 5
    assert ds[0] == (1.5, 0)
    assert ds[4] == (5.5, 0)

    batches = list(simple_loader(ds, 2))
    assert batches == [
        [(1.5, 0), (2.5, 1)],
        [(3.5, 0), (4.5, 1)],
        [(5.5, 0)],
    ]

    # batch_size делит длину без остатка — нет неполного батча
    batches_exact = list(simple_loader(ds, 5))
    assert len(batches_exact) == 1
    assert len(batches_exact[0]) == 5

    # batch_size больше длины датасета — один неполный батч
    batches_big = list(simple_loader(ds, 100))
    assert batches_big == [[(1.5, 0), (2.5, 1), (3.5, 0), (4.5, 1), (5.5, 0)]]

    # для for достаточно __len__/__getitem__, __iter__ не нужен
    assert [x for x in ds] == [(1.5, 0), (2.5, 1), (3.5, 0), (4.5, 1), (5.5, 0)]

    print('all tests passed')