import re
import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")
list_series = []


def remove_dash(line):
    """
    Function for removing '-' in a line
    :param line:
    :return: line without '-'
    """
    word_list = line.split('-')
    return " ".join(word_list)


def parse_str(line):
    """
    Convert given line to list of item and Quantity
    :param line:
    :return: append current line to list_series
    """
    if line.find('-') < len(line):
        line = remove_dash(line)
    pat1 = re.compile(r'\S*\d')
    first_itr = re.finditer(pat1, line)
    for first in first_itr:
        index = first
        break
    start_index = index.start()
    list_series.append([line[:start_index].strip(), line[start_index:].strip()])


def parse_num_lines(line):
    """
    Parse the line which are starting with numbers
    :param line:
    :return: append current line to list_series
    """
    index = 0
    doc = nlp(line)
    for ent in doc.ents:
        if ent.label_ == 'CARDINAL' or ent.label_ == 'QUANTITY' or ent.label_ == 'PRODUCT':
            index = ent.end_char
    if index == 0:
        index = line.find("gm")+2
    list_series.append([line[index:].strip(), line[:index].strip()])


def parse(one_line):
    """
    Function to parse the lines one by one
    :param one_line:
    :return:
    """
    if len(one_line) <= 2:
        pass
    if one_line[0].isdigit():
        parse_num_lines(one_line)
    else:
        parse_str(one_line)

def add_Qantity(df_col):
	list_unit = []
	for row in df_col:
		doc = nlp(row)
		for ent in doc.ents:
			label = ent.label_
		if label == 'CARDINAL':
			list_unit.append('NaN')
		else:
			word = re.findall(r"[^\d]*", row)
			for a in word:
				if len(a)>1:
					list_unit.append(a)
	return list_unit



if __name__ == "__main__":
    with open('data.txt') as f:
        content = f.readlines()

    for curr_line in content:
        curr_line = curr_line.replace('\n', '')
        word_list = curr_line.split('-')
        curr_line = " ".join(word_list)
        if len(re.findall(r"\d+", curr_line)) > 2:
            lines = re.findall(r"[A-z]+\s\d*[A-z]+|\d+\s*[A-z|\s]*", curr_line)
            for line in lines:
                if len(line) > 2:
                    parse(line)
        else:
            if len(curr_line) > 2:
                parse(curr_line)
    df = pd.DataFrame(list_series, columns=['items', 'Quantity'])
    df["unit"] = add_Qantity(df["Quantity"])

    print(df.head(20))
    df.to_csv('file.csv')
