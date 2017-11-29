from src.data import data, bloodsugar_describe
from src.secrets import CONN_STR

def main():

    df = data(CONN_STR)


    df1 = bloodsugar_describe(df, 'week')



if __name__ == '__main__':
    main()

