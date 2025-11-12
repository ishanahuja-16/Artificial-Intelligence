def isclean(list,place):
  if(list[place]==1):
    list[place] = 0
    return False
  else:
    return True

list = [1,1]
place = 0
count  = 2

while(count!=0):
  if(place==0):
    if(isclean(list,place)):
      print("Location A is already cleaned")
    else:
      print("Location A is not clean")
      print("cleaning Location A")
      print("Locatin A has been cleaned")

    count = count-1
    place = 1
  
  if(isclean(list,place)):
    print("Location B is already cleaned")
  else:
    print("Location B is not clean")
    print("cleaning Location B")
    print("Locatin B has been cleaned")
  count = count-1