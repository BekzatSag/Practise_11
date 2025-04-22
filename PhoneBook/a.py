import csv

data = [["Names", "Phone"], ["z", 87772491653], ["Nurik", 87051442666], ["A", 87772491653], ["B", 87772491653], ["C", 87772491653], ["a", 22222222222], ["b", 11111111111]]
with open("PhoneBook.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)