from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.common import *
import sparknlp
from pyspark.ml import Pipeline
import pandas as pd
from reviewQueries import fetch_reviews, insert_reviews


def get_keywords(appid):
    insert_reviews(appid)
    p_reviews = fetch_reviews(appid, True)
    n_reviews = fetch_reviews(appid, False)
    if len(p_reviews) == 0 or len(n_reviews) == 0:
        return "No review data found"
    spark = sparknlp.start()
    steam_stopwords = []


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
    .setInputCols(["sentence"]) \
    .setOutputCol("token")\
    .setContextChars(["(", ")", "?", "!", ".", ","])

# Step 4: Stopwords

    stop_words = StopWordsCleaner().pretrained('stopwords_en', 'en')\
    .setInputCols(["token"])\
    .setOutputCol("cleanTokens")\
    .setCaseSensitive(False)

# Step 5: Lemmatizer
    
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

    p_light_result = light_model.fullAnnotate(p_reviews)[0]
    n_light_result = light_model.fullAnnotate(n_reviews)[0]
    p_keys_df = pd.DataFrame([(k.result, k.metadata['score']) for k in p_light_result['keywords']],
                            columns = ['keywords', 'score'])
    p_keys_df['score'] = p_keys_df['score'].astype(float)
    n_keys_df = pd.DataFrame([(k.result, k.metadata['score']) for k in n_light_result['keywords']],
                            columns = ['keywords', 'score'])
    n_keys_df['score'] = n_keys_df['score'].astype(float)
    print("DataFrames ready...dropping duplicates")
    return [p_keys_df.drop_duplicates(subset='keywords', inplace=False) , n_keys_df.drop_duplicates(subset='keywords', inplace=False)]


if __name__ == "__main__":
    data =  get_keywords(1151340)
    print(len(data[0]), len(data[1]))