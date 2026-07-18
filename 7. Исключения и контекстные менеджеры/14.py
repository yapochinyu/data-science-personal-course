# import json

# def process_dataset(paths):
#     results = []
#     for path in paths:
#         try:
#             with open(path) as f:
#                 data = json.load(f)
#                 results.append(transform(data))
#         except (OSError, json.JSONDecodeError) as e:
#             print(f'Путь: {path} Ошибка: {e}')
#         except (AttributeError) as e:
#             print(f'Трансформация не определена')
#     return results