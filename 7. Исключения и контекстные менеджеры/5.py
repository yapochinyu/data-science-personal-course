# try:
#     user = load_user(user_id)          # может бросить KeyError

# except KeyError:
#     print(f'Пользователь {user_id} не найден')
# else:
#     try:
#         permissions = user['permissions']   # тоже может бросить KeyError!
#     except KeyError:
#         print(f'У пользователя {user_id} нет разрешения')
#     else:
#         grant_access(permissions)