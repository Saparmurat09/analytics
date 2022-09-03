import csv


class CSVHandler:

    def __init__(self, file_name='data.csv'):
        self.header = ['date', 'bids', 'asks']
        # write header to csv
        # self.writer.writerow(self.header)

    def write(self, row):
        self.fhand = open('data.csv', 'a')
        self.writer = csv.writer(self.fhand)
        self.writer.writerow(row)
        self.fhand.close()

    def read(count=10):
        pass
