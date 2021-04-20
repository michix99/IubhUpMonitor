from monitor.Utils import dic_insert


def test_dic_insert():
    comp = {0: (1, 1), 1: (1, -1), 2: (-1, 1), 3: (1, -1), 4: (-1, 1), 5: (-1, -1), 6: (-1, -1), 7: (-1, -1)}
    dic = {}
    dic_insert(dic, 0, 1, 1)
    dic_insert(dic, 1, 1, -1)
    dic_insert(dic, 2, -1, 1)
    dic_insert(dic, 3, 1, -1)
    dic_insert(dic, 4, -1, 1)
    dic_insert(dic, 5, -1, -1)
    dic_insert(dic, 6, -1, -1)
    dic_insert(dic, 7, -1, -1)
    assert dic == comp  # Check if regular insertion works as expected
    dic_insert(dic, 0, 5, 5)
    dic_insert(dic, 1, 5, -1)
    dic_insert(dic, 2, -1, 5)
    dic_insert(dic, 3, -1, -1)
    assert dic == comp  # Check that existing values won't get replaced
    dic_insert(dic, 3, -1, 10)
    dic_insert(dic, 4, 10, -1)
    dic_insert(dic, 5, 10, 10)
    comp[3] = (1, 10)
    comp[4] = (10, 1)
    comp[5] = (10, 10)
    assert dic == comp  # Check if value insertion works properly
