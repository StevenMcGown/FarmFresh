read -p "Number of eggs gathered today: " num_eggs
read -p "Current inventory: " curr_inventory
python3 genInventory.py $num_eggs $curr_inventory
python3 googleCalendar.py
