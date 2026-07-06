import pandas as pd

df = pd.DataFrame({
    'age': [25, 35, 45, 22, 51],
    'salary': [50000, 65000, 80000, 42000, 90000],
})


def add_senior_segment(df):
    df2 = df[df['age'] > 30].copy()
    df2['segment'] = 'senior'
    return df2
    

if __name__ == '__main__':
    original = df.copy()

    result = add_senior_segment(df)

    # исходный df не должен измениться
    assert df.equals(original), "исходный df был изменён — функция не должна мутировать вход"

    # в результате должны остаться только age > 30
    assert (result['age'] > 30).all()
    assert len(result) == 3

    # у всех строк результата колонка segment == 'senior'
    assert (result['segment'] == 'senior').all()

    # в исходном df колонки segment быть не должно
    assert 'segment' not in df.columns

    print("все тесты прошли")


    # Она возникает, когда ты фильтруешь DataFrame (df2 = df[df['age'] > 30]) 
    # и потом пытаешься присвоить значение в df2 (df2['segment'] = 'senior'). 
    # Проблема в том, что pandas не гарантирует, вернула ли операция фильтрации view 
    # (общую память с df) или copy (независимый объект) — это зависит от внутренней реализации 
    # и типов данных. Поэтому pandas не может понять, 
    # попадёт ли твоя запись в df2 реально в исходный df или нет, 
    # и на всякий случай предупреждает: 
    # "ты, возможно, работаешь с промежуточным объектом, а не с тем, что думаешь".