import csv

data = [["Names", "Phone"], ["Bekzat", 87772491653], ["Nurik", 87051442666], ["A", 11111111111], ["B", 22222222222]]
with open("PhoneBook.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)