import pandas as pd
import re
import argparse
from dataclasses import dataclass


@dataclass
class MetaData:
    name: str = ""
    email: str = ""


regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


def build_args():
    parser = argparse.ArgumentParser(description='verify txt emailbook format, and match with xlsx')
    parser.add_argument("-t", "--txt", type=str, default="", help="txt file path")
    parser.add_argument("-x", "--xlsx", type=str, default="", help="xlsx file path")
    args = parser.parse_args()
    return args


def is_email_valid(email):
    if re.fullmatch(regex, email):
        return True
    else:
        print("invalid email: ", email)
        return False


def read_txt(path):
    with open(path, "r") as f:
        lines = f.readlines()
    return lines


def read_xlsx(path):
    df = pd.read_excel(path)
    return df


def verify_email(info: str):
    if "@" in info:
        # Check if there is a tab in the info
        if "\t" not in info:
            print("You better use tab to separate the name and email: ", info)
        info = info.replace("\n", "").replace("\r", "").replace("\t", "").replace(" ", "")
        # check if there is ";" at the end of the info

        if info[-1] != ";":
            print("`;` must at the end of ", info)

        tmp = info.split("<")
        assert len(tmp) == 2, "There must be only one `<` in the info: {}".format(info)
        name = tmp[0]
        email = tmp[1].replace(">", "").replace(";", "")
        # print(name, "," ,email)
        # print(info)

        return MetaData(name, email)
    else:
        if len(info) > 1:
            raise Exception("No email found in: ", info)


def verify_df_row(row):
    has_email = False
    email = ""
    for t in row:
        if isinstance(t, str):
            if "@" in t:
                has_email = True
                email = t
                break
    if has_email:
        name = row[1].replace(" ", "")
        email = email.replace(" ", "")
        return MetaData(name, email)
    else:
        return None


def match_txt_and_xlsx(book_from_txt, book_from_xlsx):
    for d_x in book_from_xlsx:
        matched = False
        for d_t in book_from_txt:
            if d_x.email == d_t.email:
                matched = True
                break
        if not matched:
            print("Email not found in txt: ", "name: ", d_x.name, "email: ", d_x.email)


def vemail():
    args = build_args()
    if len(args.txt) > 0:
        txt = read_txt(args.txt)
    else:
        print("Please provide txt file path, current path is: ", args.txt)
        txt = None

    if len(args.xlsx) > 0:
        df = read_xlsx(args.xlsx)
    else:
        print("Please provide xlsx file path, current path is: ", args.xlsx)
        df = None

    book_from_txt = []
    if txt is not None:
        for t in txt:
            ret = verify_email(t)
            if isinstance(ret, MetaData):
                book_from_txt.append(ret)

    # print(book_from_txt)
    book_from_xlsx = []
    if df is not None:
        for index, row in df.iterrows():
            ret = verify_df_row(row)
            if isinstance(ret, MetaData):
                book_from_xlsx.append(ret)

    if len(args.xlsx) > 0 and len(args.txt) > 0:
        match_txt_and_xlsx(book_from_txt, book_from_xlsx)


if __name__ == "__main__":
    vemail()
