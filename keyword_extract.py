from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.common import *
import sparknlp
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StopWordsRemover
import pyspark.sql.functions as F
import pandas as pd
from reviewQueries import fetch_reviews, insert_reviews, get_last_review
from gameQueries import fetch_game_name
from datetime import date


def get_keywords(appid, sentiment):
    today = date.today()
    date_of_last_review_fetch = get_last_review(appid)
    print(f'Today: {today} Last Review Date: {date_of_last_review_fetch}')
    if date_of_last_review_fetch is not None and date_of_last_review_fetch[0] >= today:
        reviews = fetch_reviews(appid, sentiment)
    else:
        insert_reviews(appid)
        reviews = fetch_reviews(appid, sentiment)
    if len(reviews) == 0:
        return "No review data found"
    
    spark = sparknlp.start()
    # code to add game_name into list of stop words. Impacted quality of data
    # game_name = fetch_game_name(appid).lower().split(" ")
    steam_stopwords = []
    # 'recommendation', 'game'
# Step 1: Transforms raw texts to 'document' annotation
    document = DocumentAssembler() \
        .setInputCol("text") \
        .setOutputCol("document")

# Step 2: Sentence Detection

    sentenceDetector = SentenceDetector()\
    .setInputCols("document") \
    .setOutputCol("sentence")

#step 3: tokenization
    token = Tokenizer() \
    .setInputCols("sentence") \
    .setOutputCol("token")\
    .setContextChars(["(", ")", "?", "!", ".", ","])

# Bonus Step: Stopwords

    stop_words = StopWordsCleaner().pretrained('stopwords_en', 'en')\
    .setInputCols(["token"])\
    .setOutputCol("cleanTokens")\
    .setCaseSensitive(False)

# Extra Bonus Step: Lemmatizer
    
    lemmatizer = LemmatizerModel.pretrained()\
    .setInputCols(["token"])\
    .setOutputCol("lemma")

# step4: keywordExtraction
    keywords = YakeKeywordExtraction()\
    .setInputCols(["lemma"])\
    .setOutputCol("keywords")\
    .setMinNGrams(1)\
    .setMaxNGrams(3)\
    .setNKeywords(200)\
    .setStopWords(stop_words.getStopWords()+steam_stopwords)
# setNKeywords is untested and may need to be turned off, not sure if it will skew data. Extracts the top n keywords
# another function to check is setThreshold(float) - each keyword will be given a keyword score greater than 0, lower the score the better. Set an upper bound for the keyword score from this method
# setWindowSize(int) Yake will construct a co-occurence matrix. (default window =3) 
# You can set the window size for the cooccurence matrix construction from this method. e.g. windowSize=2 will look at two words to both left and right of a candidate word
    

# Define the pipeline
    yake_pipeline = Pipeline(stages=[document, sentenceDetector, token, lemmatizer, keywords])

#create an empty dataframe

    empty_df = spark.createDataFrame([['']]).toDF("text")

# Fit the dataframe to get the
    yake_Model = yake_pipeline.fit(empty_df)

# LightPipeline can handle strings or an array of strings, lightweight version of Spark ML. Computes everything locally

    light_model = LightPipeline(yake_Model)

    light_result = light_model.fullAnnotate(reviews)[0]
    keys_df = pd.DataFrame([(k.result, k.metadata['score']) for k in light_result['keywords']],
                            columns = ['keywords', 'score'])
    keys_df['score'] = keys_df['score'].astype(float)

    print("DataFrame ready...dropping duplicates")
    return keys_df.drop_duplicates(subset='keywords', inplace=False)

if __name__ == "__main__":
    wcf_input = {}
    for word in get_keywords(1091500, False).to_dict(orient='records'):
         wcf_input.update({word['keywords']: word['score']})
    print(wcf_input)