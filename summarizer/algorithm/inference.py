import importlib
from .IP_summarizer_prune import IP_summarizer
import string
import nltk.data
from tqdm import tqdm
from .Bert_base import inference


class Inference:
    def __init__(self, info_ratio, input_string, max_length):
        self.info_ratio = info_ratio
        self.input_string = input_string
        self.max_length = max_length

    def clean_lines(self, lines):
        cleaned = list()
        # prepare a translation table to remove punctuation
        table = str.maketrans('', '', string.punctuation)
        for line in lines:
            # strip source cnn office if it exists
            index = line.find('(CNN)')
            if index > -1:
                line = line[index+len('(CNN)'):]
            # tokenize on white space
            line = line.split()

            # convert to lower case
            line = [word.lower() for word in line]
            # remove punctuation from each token
            line = [w.translate(table) for w in line]
            # remove tokens with numbers in them
            line = [word for word in line if word.isalpha()]

            # store as string
            cleaned.append(' '.join(line))
        # remove empty strings
        cleaned = [c for c in cleaned if len(c) > 0]
        print(f"Cleaned text: {cleaned}")
        return cleaned

    def main(self):
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

        print("Began loading the Bert_base model...")

        model = inference.load_model()
        print('Pre-trained model is loaded')

        print("Model: " + str(model))

        sentenceData = []
        sentenceData.append(tokenizer.tokenize(self.input_string))

        result = []
        for sentence in tqdm(sentenceData):
            sentences_ = self.clean_lines(sentence)

            if sentences_[-1] == '':
                sentences_ = sentences_[:-1]

            if len(sentences_) == 1:
                output = sentence

            else:
                embeddings = inference.generate_vecs(
                    model, sentences_)
                summarizer = IP_summarizer(
                    sentence, embeddings, threshold=self.info_ratio, max_len=self.max_length)
                output = summarizer.Optimization()
            result.append(list(output))
        return result[0]
