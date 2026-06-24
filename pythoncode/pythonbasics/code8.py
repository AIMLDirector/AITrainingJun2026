# evens = [x for x in range(10) if x % 2 == 0]


event_list = []
odd_list = []
for i in range(10):
    if i % 2 == 0:
        event_list.append(i)
    else:
        odd_list.append(i)



event_list = [ i for i in range(10) if i % 2 == 0]
odd_list = [ i for i in range(10) if i % 2 != 0]

package_check = sys.argv[1] if len(sys.argv) > 1 else 'pandas numpy'


package_check = []
if len(sys.argv) > 1:
    package_check = sys.argv[1]
else:
   package_check = ['pandas', 'numpy'] 



labels = ["Even" if x % 2 == 0 else "Odd" for x in range(5)]
print(labels) 

labels= []
for x in range(5):
    if x % 2 == 0:
        print(even)
        labels.append(even)
    else:
        print(odd)
        labels.append(odd)


labels = [ even if x % 2 ==0 else odd for x in range(5)]
labes1 = [even for i in range(10) if x % 2 == 0 ]