import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from nltk import sent_tokenize, word_tokenize
from pathlib import Path

import json
import numpy as np

class NamedEntityRecognition:
    def __init__(self,model_name,user_id): 
        dir_path = Path(f'../uploads/{user_id}/{model_name}')
        model_path = dir_path / "modelToUpload.keras"
        meta_data_path = dir_path/"metaDataToUpload.json"
        tokenizer_path = dir_path / "tokenizerToUpload.json"
        self.model = load_model(model_path)
        self.word_tokenizer = tokenizer_from_json(self.get_tokenizer_json(tokenizer_path))
        with open(meta_data_path) as file:
            self.meta_data = json.load(file)

    def get_tokenizer_json(self,file_name):
        with open(file_name) as file:
            tokenizer_json  = file.read()
        return tokenizer_json
    
    def preprocess_sentences(self, text, tokenizer, max_len):
        """
        Preprocesses a text split into sentences and tokens.
        Returns a list of tokenized sequences and the corresponding original tokens.
        """
        sentences = sent_tokenize(text)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        token_sequences = tokenizer.texts_to_sequences(tokens)
        padded_sequences = pad_sequences(token_sequences, maxlen=max_len, padding='post')
        return padded_sequences, tokens

    def predict_ner_multi_sentence(self, text, model, tokenizer, max_len, index_to_tag):
        # Preprocess the text with multiple sentences
        padded_sequences, tokens = self.preprocess_sentences(text, tokenizer, max_len)
        # Predict NER tags for each sentence
        predictions = model.predict(padded_sequences)
        # Convert predictions back to tags
        formatted_output = {'sentences': []}

        for i, sentence_predictions in enumerate(predictions):
            # Get the tokens for the current sentence
            current_tokens = tokens[i]
            # Map the highest probability index to the corresponding tag
            sentence_tags = [index_to_tag.get(str(np.argmax(pred)), 'O') for pred in sentence_predictions]
            
            # Match tags with original tokens (ignoring padding)
            word_tag_pairs = [
                {'token': token, 'ner': tag}
                for token, tag in zip(current_tokens, sentence_tags[:len(current_tokens)])
            ]
            # Add each sentence's word-tag pairs to the formatted output
            formatted_output['sentences'].append({'tokens': word_tag_pairs})

        return formatted_output
    
    def run(self,data):
        output = self.predict_ner_multi_sentence(data[0].contents, self.model, self.word_tokenizer, self.meta_data['max_len'], self.meta_data['tag_map'])
        
        return output