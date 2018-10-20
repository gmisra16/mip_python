# from src.logexception.exceptionhandler import CustomUserException
# Error & Exception handling
from log_exception import log_exception

@log_exception
def parse_csv_and_get_columns(filename):
    count = 0
    csvFile = open(filename, 'r')
    lines = csvFile.readlines()
    for line in lines[1:]:
        val = line.split(",")
        test_str_div = val[0] / val[11]
        print(test_str_div)
        test_zero_div =  (int(val[0]) / int(val[11]))


if __name__ == "__main__":
    parse_csv_and_get_columns(filename="data/flights.csv")
