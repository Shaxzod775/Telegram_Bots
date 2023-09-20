def test_func(a):
    return a[::-1]



result = test_func('абвгд')

print(result)


# products = ['рис', 'мясо', 'морковь']
#
# products.insert(2, 'пельмени')
#
# print(products)



# hello_list = [str(i) + ('. Hello') for i in range(1, 11)]
#
# print(hello_list)
#
#
#
# num_list = []
#
# for i in range(1, 11):
#     num_list.append(str(i) + ". Hello")
#
# print(num_list)

# musor = ['apple', 'burger', 5, 2, 'banana', 7]
#
# list_str = []
# list_int = []
#
# for i in musor:
#     if type(i) is str:
#         list_str.append(i)
#     else:
#         list_int.append(i)
#
# print(list_str)
# print(list_int)

str1 = 'Hello World'
str2 = str1[::-1]
str3 = ' '.join(str1.split(' ')[::-1])
print(str3)






