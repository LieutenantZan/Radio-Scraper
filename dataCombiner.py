import csv
import pprint


def remove(newList, master):
    unique = []
    for song in newList:
        if song not in master:
            unique.append(song)
    return unique


def combiner(newSongsFile):
    # masterFile = input("Enter master list file location: ")
    masterFile = "masterList.csv"
    # newSongsFile = input("Enter new song list filename: ") + ".csv"
    newSongsFile = newSongsFile + ".csv"
    with open(masterFile, 'r', encoding='utf-8', newline='') as csvFile:
        masterList = list(csv.reader(csvFile))
    # pprint.PrettyPrinter(width=100, compact=True).pprint(masterList)
    with open(newSongsFile, 'r', encoding='utf-8', newline='') as csvFile:
        newList = list(csv.reader(csvFile))
    # pprint.PrettyPrinter(width=100, compact=True).pprint(newList)
    print("Removing duplicates...")
    uniqueList = remove(newList, masterList) # returns only non-duplicate songs
    removed = len(newList)-len(uniqueList)
    print("There were " + str(removed) + " songs removed")

    # pprint.PrettyPrinter(width=100, compact=True).pprint(newList)
    print("Writing combined list...")

    with open(masterFile, "a", encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for song in uniqueList:
            writer.writerow(song)

    print("Done!")


def main():
    files = ["CompiledData"]
    for file in files:
        print("Working on " + file)
        combiner(file)

main()