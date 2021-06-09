from datetime import date, timedelta
import sys

today = date.today()
current_inventory = int(sys.argv[2])
eggs_gathered = int(sys.argv[1])
num_eggs_per_day = 12
eggs_past_7_days = []
number_of_days_displayed = 30

reservations = {
   '''
   '2021-06-09': 12,
   '2021-06-11': 18,
   '2021-06-19': 12
   '''
}
calendar = {}

"""
Predicts number of eggs laid each day
"""
def predictNumEggs (gathered):
   print("Predicting number of eggs each day...")
   #Read file
   eggs = []
   num = ""
   with open('eggs_past_week.txt') as f:
      lines = str(f.readlines())

   #Interpret file
   for character in lines:
      if character.isdigit():
         num+=character
      elif len(num) > 0 and character == '\'':
         eggs.append(int(num))
         num = ""
      elif character == '[' or character == '\'' or character == ']':
         num = ""
      else:
         eggs.append(int(num))
         num = ""

   #Add egg count to array
   eggs.reverse()
   eggs.pop()
   eggs.reverse()
   eggs.append(gathered)

   #Write string to file
   with open('eggs_past_week.txt',"+w") as f:
      string = ""
      for egg in eggs:
         string += (str(egg) + " ")
      f.write(string)

   #Determine average number of eggs over the past seven days
   avg = 0
   for egg_count in eggs:
      avg += egg_count
   avg /= len(eggs)

   #Use floor() for worst case scenario. Casting to int acts as floor()
   print("New number of eggs each day:",int(avg))
   return int(avg)


"""
Generates the calendar and accounts for reservations
"""
def generateCalendar (inventory, number_of_days, eggs_per_day):

   print("Generating calendar...")

   #Projects egg count, does not account for reservations
   for day in range(0, number_of_days):
      current_date = str(today + timedelta(day))
      calendar[current_date] = inventory
      inventory += eggs_per_day
      if current_date in reservations:
         inventory -= reservations[current_date]
         calendar[current_date] = inventory

"""
Adds a reservation to the calendar
"""
def reserveEggs (number_of_eggs, order_date):
   print("\nReserving", number_of_eggs, "eggs for", order_date, "...")

   if(number_of_eggs % 6 != 0):
      print("Number of eggs must be modulo 6")
      return

   if(number_of_eggs > calendar[order_date]):
      print("Not enough eggs available on", order_date, "to fulfill an order of", number_of_eggs)
   else:
      reservations[order_date] = number_of_eggs
      print(number_of_eggs, "eggs successfully reserved for", order_date)

"""
============ Main ============
"""
num_eggs_per_day = predictNumEggs(eggs_gathered)

#Generating calendar with already-existing reservations
generateCalendar(current_inventory, number_of_days_displayed, num_eggs_per_day)

f = open("events.json", "a")

f.truncate(0)

f.write("{\n")

length = len(calendar)
counter = 0
for day in calendar:
   counter+=1
   if counter < length:
      f.write("\t\t\""+str(day)+"\":"+"\""+str(calendar[day])+" eggs available"+"\",\n")
   else:
      f.write("\t\t\""+str(day)+"\":"+"\""+str(calendar[day])+" eggs available"+"\"\n")

f.write("}")

f.close()
