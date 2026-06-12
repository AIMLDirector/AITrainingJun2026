# list - add, modify, delete, duplicate, sort, reverse, index, count, copy, clear
l2 = [6, 2.5, "python", [1, 2, 3], (4, 5, 6), {7, 8, 9}, {"name": "John", "age": 30}]  # dont do this


l1 = [10,20,30,40,50]  # index 0  1  2  3  4 or index -5 -4 -3 -2 -1

l3 = [50,70,90]
print(l1)
print(l1[0])
print(l1[-5])
print(l1[1:4])
#add data
l1.append(60)
print(l1)
l1.insert(2, 25)
print(l1)
l1.extend(l3)
print(l1)

l1.sort(reverse=True)
print(l1)
l1.reverse()
print(l1)

# removing the data

l1.remove(70)
print(l1)
l1.pop()  # removes the last element
print(l1)
# l1.clear()
# print(l1)


for i in l1:
    if i > 30:
        print("greater than 30", i)
  

