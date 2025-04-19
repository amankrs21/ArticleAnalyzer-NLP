# Importing Required Libraries
import os
import re
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import cmudict
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer


# Funtion to save extracted articles to the text file
def SaveDataFile(url_id, article):
    try:
        with open(f"{'Articles'}/{url_id}.txt", 'w') as f:
            for lines in article:
                f.write(lines+'\n')
    except FileNotFoundError:
        os.system('mkdir Articles')
        with open(f"{'Articles'}/{url_id}.txt", 'w') as f:
            for lines in article:
                f.write(lines+'\n')
    print("Data Successfully Saved to {}.txt Text File.".format(url_id))


# Funtion to extract data from urls
def DataExtraction(url, url_id):
    page = requests.get(url)
    if (page.status_code == 200):
        print('Data Fetched Successfully from ->',url)

        # Now formating page data into proper html format
        soup = BeautifulSoup(page.content, 'html.parser')

        # Article List contains all required data from Page
        article = []    # initialised article list as empty

        # Extracting Title of the Page
        try:
            title = soup.findAll(attrs = {'class':'td-post-title'})
            title = title[0].text.replace('\n','').split("By")
        except:
            title = soup.findAll(attrs = {'class':'tdb-title-text'})
            title = title[0].text.replace('\n','').split("By")
        
        # Appending the Title value into Article List
        article.append(title[0])

        # Extracting all the content of the page
        try:
            content = soup.findAll(attrs = {'class':'td-post-content tagdiv-type'})
            content = content[0].text.replace('\xa0','').split('\n')
        except:
            content = soup.findAll(attrs = {'class':'tdb-block-inner td-fix-index'})
            content = content[19].text.replace('\xa0','').split('\n')
        
        # Appending content into Article List
        for line in content:
            if line.strip() != '':
                article.append(line)

        # Last line contain unnessary data, so popped it.
        article.pop()

        # Calling Function to save data into TextFile
        SaveDataFile(url_id, article)
    
    else:
        print("URL NOT FOUND ->",url)
        article = ['URL Not Found']

        # Calling Function to save data into TextFile
        SaveDataFile(url_id, article)



# Funtion to analyse all the required data
def AnalyseData(inc, id, url, article, stopwords, positive_words, negative_words, data):

    # Creating word tokens from article
    tokens = word_tokenize(article)
    for i in range(len(tokens)):
        tokens[i] = tokens[i].replace('“', '') # remove double quotes
        tokens[i] = tokens[i].replace("’", "") # remove single quotes
        tokens[i] = tokens[i].replace(",", "") # remove commas
        tokens[i] = tokens[i].replace(".", "") # remove full stops
        tokens[i] = tokens[i].replace("(", "") # remove left parenthesis stops
        tokens[i] = tokens[i].replace(")", "") # remove right parenthesis stops
        tokens[i] = tokens[i].translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    while "" in tokens:
        tokens.remove("")
    
    # Calculating Postive Score
    positive_score = sum(1 for token in tokens if token.lower() in positive_words and token.lower() not in stopwords)
    # Calculating Negative Score
    negative_score = sum(-1 for token in tokens if token.lower() in negative_words and token.lower() not in stopwords)*-1
    # Calculating Polarity Score
    polarity_score = (positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
    # # Calculating Subjectivity Score
    subjectivity_score = (positive_score + negative_score)/ ((len(tokens)) + 0.000001)


    # Calculating Average Sentence Length
    num_sentence = len(sent_tokenize(article))
    num_words = len(tokens)
    avg_sent_length = (num_words / num_sentence)

    # Calulating Total Complex Words
    complex_words = [w for w in tokens if len(re.findall(r'[aeiouy]+', w, re.IGNORECASE)) > 2]
    total_complex_word = len(complex_words)

    # Calculating Percentage of Complex Words
    perc_complex_word = (total_complex_word / len(tokens))

    # Calculating Fog Index
    fog_index = (0.4) * (avg_sent_length + perc_complex_word)

    # Calculating Average Number of Words per Sentence
    avg_num_words_per_sent = (num_words / num_sentence)

    # Calculating total number of Personal Pronouns
    personal_pronoun = ['i', 'we', 'my', 'ours', 'us']
    pattern = r'\b(?!(?:US\b))(' + '|'.join(personal_pronoun) + r')\b'
    counts = {}
    for pronoun in personal_pronoun:
        count = len(re.findall(r'\b' + pronoun + r'\b', article.lower()))
        counts[pronoun] = count
    count_personal_pronoun = sum(counts.values())

    # Calculating Average Word Length
    tokenizer = RegexpTokenizer(r'\w')
    num_character = len(tokenizer.tokenize(article))
    avg_word_length = (num_character / num_words)

    # Counting Syllables
    def count_syllables(word):
        vowel = "aeiou"
        count = 0
        if word[0] in vowel:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowel and word[i-1] not in vowel:
                count += 1
                if word.endswith("es") or word.endswith("ed"):
                    count -= 1
        if count == 0:
            count += 1
        return count
    words = re.findall(r'\b\w+\b', article)
    total_syllables = sum([count_syllables(word) for word in words])
    total_words = len(words)
    avg_syllable_count = total_syllables / total_words

    print(id, "Data Successfully Generated for URL ID ->",id)
    print("""\n Positive Score -> {}
           Negetive Score -> {}
           Polarity Score -> {}
           Subjectivity Score -> {}
           Average Sentance Length -> {}
           Total Complex Word -> {}
           Percentage Complex Word -> {}
           Fog Index -> {}
           Average Number of Words per Sentance -> {}
           Total Number of Words -> {}
           Personal Pronoun -> {}
           Average Word Length -> {}
           Average Syllable Count -> {}""".format(positive_score, negative_score, polarity_score, subjectivity_score, avg_sent_length,total_complex_word, perc_complex_word, fog_index, avg_num_words_per_sent, num_words, count_personal_pronoun, avg_word_length, avg_syllable_count))

    
    data.insert(inc,[id, url, positive_score, negative_score, polarity_score, subjectivity_score, avg_sent_length,total_complex_word, perc_complex_word, fog_index, avg_num_words_per_sent, num_words, count_personal_pronoun, avg_word_length, avg_syllable_count])


def ReadData(url_ID, url):

    # Collecting StopWords data from StopWords File
    stopwords_files = ['StopWords_Auditor.txt',
               'StopWords_Currencies.txt',
               'StopWords_DatesandNumbers.txt',
               'StopWords_GenericLong.txt',
               'StopWords_Generic.txt',
               'StopWords_Geographic.txt',
               'StopWords_Names.txt']
    stopwords = []
    for file in stopwords_files:
        with open(f"{'StopWords'}/{file}", 'r', encoding="latin-1") as f:
            stopwords += [word.strip() for word in f.readlines()]
    

    masterdictionary_files = ['negative-words.txt', 'positive-words.txt']
    positive_words = []
    negative_words = []
    for filename in masterdictionary_files:
        with open(f"{'MasterDictionary'}/{filename}", 'r', encoding="latin-1") as f:
            for word in f.read().split():
                word = word.lower()
                if word in stopwords:
                    continue
                if filename == "positive-words.txt":
                    positive_words.append(word)
                elif filename == "negative-words.txt":
                    negative_words.append(word)

    data = []
    for i in range(len(url_ID)):
        filename = f"{'Articles'}/{url_ID[i]}.txt"
        with open(filename, 'r') as f:
            article = f.read()
        
        AnalyseData(i, url_ID[i], url[i], article, stopwords, positive_words, negative_words, data)
    print("All Data Analysed Successfully!!")

    df = pd.DataFrame(data, columns = ['URL_ID','URL','POSITIVE SCORE','NEGETIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','COMPLEX WORD COUNT','PERCENTAGE OF COMPLEX WORD','FOG INDEX','AVG NO OF WORDS PER SENTENCE','TOTAL WORD COUNT','PERSONAL PRONOUNS','AVG WORD LENGTH','AVG SYLLABLES PER WORD'])
    print("\n\n",df)
    df.to_excel('Output.xlsx', engine='openpyxl')
    print("Data Successfully Extracted to 'Output.xlsx' File!!")


# Reading data from 'Input.xlsx' file
local = pd.read_excel('Input.xlsx')

url_list = local['URL'].tolist()    # storing all urls into list
url_ID = local['URL_ID'].tolist()   # stroring all url_id into list

# Calling DataExtraction funtion in the loop which cause all url execute once and save data into text file.
for i in range(len(url_list)):
    DataExtraction(url_list[i], url_ID[i])

print("\n All Data Successfully Save to Text Files")
ReadData(url_ID, url_list)
