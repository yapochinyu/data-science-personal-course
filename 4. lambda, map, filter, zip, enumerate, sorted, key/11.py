staff = [
    {'name': 'Anna', 'dept': 'ML', 'salary': 200},
    {'name': 'Boris', 'dept': 'Data', 'salary': 180},
    {'name': 'Vera', 'dept': 'ML', 'salary': 220},
    {'name': 'Gleb', 'dept': 'Data', 'salary': 180}
    ]


print(sorted(staff, key=lambda s: (s['dept'], -s['salary'], s['name'])))

print(sorted(sorted(sorted(staff, key=lambda x : x['name']), key=lambda x : x['salary'], reverse=True), key=lambda x : x['dept']))