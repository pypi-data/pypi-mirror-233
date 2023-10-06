# A lame test, change the test answer value to get an assertion error
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
