from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.common import *
import sparknlp
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StopWordsRemover
import pyspark.sql.functions as F
import pandas as pd
from reviewQueries import fetch_reviews
from gameQueries import fetch_game_name

def get_keywords(appid, sentiment):
    spark = sparknlp.start()
    reviews = fetch_reviews(appid, sentiment)
    game_name = fetch_game_name(appid).lower().split(" ")
    steam_stopwords = ['recommendation', 'game']+game_name
    
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
    .setMaxNGrams(1)\
    .setNKeywords(20)\
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

    keys_df = pd.DataFrame([(k.result, k.metadata['score'], k.metadata['sentence']) for k in light_result['keywords']],
                            columns = ['keywords', 'score', 'sentence'])
    keys_df['score'] = keys_df['score'].astype(float)

# ordered by relevance
    return keys_df.sort_values(['score'], ascending=False).head(10)

if __name__ == "__main__":
    print(get_keywords(10, False))