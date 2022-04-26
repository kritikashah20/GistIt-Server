import nltk
# nltk.download('punkt')
import numpy as np

from nltk.tokenize import sent_tokenize

from sentence_transformers import SentenceTransformer

import torch
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer

import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import joblib

# Segmentation

# Tokenize the text to Sentences

def tokenize2sent(text):
  sentences = sent_tokenize(text)
  return sentences

# Generating Sentence Embeddings

# sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

# joblib.dump(sbert_model, 'sbert_model.pkl')

sbert_model_from_joblib = joblib.load('sbert_model.pkl')

def create_sentence_vectors(sentences):
  sentence_embeddings = sbert_model_from_joblib.encode(sentences)
  return sentence_embeddings

# Defining Similarity Function

def cosine(u, v):
  return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# Computing Similarity Between Every 2 Consecutive Sentences

def calculate_similarity(sim_sent, sentence_embeddings):
  similarity = []
  current = 0

  while current < len(sim_sent)-1:
    similarity.append(cosine(sentence_embeddings[current], sentence_embeddings[current+1]))
    current += 1
    
  return similarity


# Determining Paragraph Breaks and Storing the Paragraphs

def segment_text2para(sentences, similarity_values, threshold):
  paragraph_text = ''''''
  current = 0 
  segmented_paragraphs = []

  while current < len(sentences)-1:
    paragraph_text += sentences[current] + ' '

    if similarity_values[current] < threshold:
      segmented_paragraphs.append(paragraph_text)
      paragraph_text = ''''''

    current += 1
  paragraph_text += sentences[current]
  segmented_paragraphs.append(paragraph_text)

  return segmented_paragraphs


# utility function
def utility(raw_text, threshold):
    text_sentences2 = tokenize2sent(raw_text)

    sent_vectors2 = create_sentence_vectors(text_sentences2)

    sim2 = calculate_similarity(text_sentences2, sent_vectors2)

    seg2 = segment_text2para(text_sentences2, sim2, threshold) # not for user

    return seg2

# Summarization



# Abstractive summarization Using Transformer

# t_summarizer = pipeline('summarization', model="t5-small", tokenizer="t5-base")

# joblib.dump(t_summarizer, 't_summarizer.pkl')

t_summarizer_from_joblib = joblib.load('t_summarizer.pkl')

def t_on_paras(raw_text, threshold=0.45):
  segments = utility(raw_text, threshold) 
  summarised_seg = []
  final_summarised_seg = []
  for seg in segments:
    output = t_summarizer_from_joblib(seg, max_length=100, min_length=5) 
    summarised_seg.append(output[0]['summary_text'])

  for paragraph in summarised_seg:
    insents = paragraph.split(' . ')
    outsents = []
    formatted_sent = ''
    for sent in insents:
      formatted_sent = sent[0].upper() + sent[1:]
      outsents.append(formatted_sent)
    paragraph_formatted = '. '.join(outsents)
    paragraph_formatted_final = paragraph_formatted[0:len(paragraph_formatted)-2] + '.'
    final_summarised_seg.append(paragraph_formatted_final)
    
  return final_summarised_seg



# Pointwise Summarisation Using Hugging Face Title Generator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
# model = model.to(device)

# joblib.dump(model, 'transformer_model.pkl')
joblib.dump(tokenizer, 'tokenizer_model.pkl')

transformer_from_joblib = joblib.load('transformer_model.pkl')
tokenizer_from_joblib = joblib.load('tokenizer_model.pkl')

def points_from_para(raw_text, threshold=0.45):
  segments = utility(raw_text, threshold)
  summarised_seg = []
  for seg in segments:
    encoding = tokenizer.encode_plus(seg, return_tensors = "pt")
    input_ids = encoding["input_ids"].to(device)
    attention_masks = encoding["attention_mask"].to(device)
    beam_outputs = transformer_from_joblib.generate(
      input_ids = input_ids,
      attention_mask = attention_masks,
      max_length = 64,
      num_beams = 3,
      early_stopping = True,
    )
    result = tokenizer.decode(beam_outputs[0][1:-1])
    summarised_seg.append(result)
    
  return summarised_seg



# N Sentences from Each Sub Topic

def n_sent_from_para(raw_text, threshold=0.45, n=2):
  segments = utility(raw_text, threshold)
  summarised_seg = []
  for seg in segments:
    result = []

    my_parser = PlaintextParser.from_string(seg,Tokenizer('english'))
    lex_rank_summarizer = LexRankSummarizer()
    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=n)

    for sent in lexrank_summary:
      result.append(sent)
    summarised_seg.append(result)
    
  return summarised_seg



# raw_text1 = '''Growing up in Canada with a life-long fascination for Canadian geography, I have always been interested in returning to the country. Although my family moved to the US before I entered high school, I have always kept my eyes turned north, especially in recent years as I began to read journal articles about research conducted on John Evans Glacier, located about 80 N latitude. Graduating next semester with a B.S. in computer science and engineering and a minor in geographic information systems, I am interested in attending the University of Alberta for graduate study. Geographic information systems (GIS) is a field especially suited to investigating spatial patterns, modeling diverse scenarios, and overlaying spatial data. This semester, in my advanced GIS course, Spatial Data Structures and Algorithms, I am part of a team developing a temporal database and program for tracing historical trading data. My computer science skills have also been put to use in two summer internship projects, where I acquired proficiency with using LIDAR (light detection and ranging) technology, now favored by NASA in its current 10-year study of Greenland and changes in the ice cap extent. Through my coursework and project experience, I have also accrued skills in using Arc/Info, ArcView, Microstation, and RDBMS software packages, and I am equally comfortable programming in Visual Basic, C++, and Java. For my graduate research project, I would like to investigate methods for improving current GIS data models to better incorporate time as a variable in studying climate change. Changes in glaciers and polar environments occur rapidly, and these changes become important indicators of broader, potentially catastrophic, global changes. By developing and applying temporal GIS methods to glaciology, I can contribute to improved spatio-temporal analysis techniques for studying the polar environment and glaciers. Also, I can discern which temporal methods serve as the best predictors and provide benefits to the GIS research community that apply to areas other than glaciology. My long-term goals are to enter the GIS field as a consultant or to extend my research and earn my Ph.D. at a program of international reputation. Having advanced experience with temporal GIS technology would make me a valuable consultant to a company, especially in the twin burgeoning fields of computer science and GIS. In applying to the University of Alberta, I recognize your strengths in both computer science and glaciology, and the recent application of these areas to field research at Ellesmere Island in Nunavut, Canada, is especially appealing to me. With my deep-rooted interest in Canadian geology and recognition of the quality of your university programs, I hope you will give my application every consideration.
# '''
# abs1 = t_on_paras(raw_text1, 0.5)

# print(abs1)

# print('\n \n')

# for a in abs1:
#   print(a, '\n')

# print('===========================================\n')


# pointwise1 = points_from_para(raw_text1, 0.5)

# print('Summary in Points:')
# for paragraph in pointwise1:
#   print(f'{paragraph}\n\n')

# print('===========================================\n')


# n_sents = n_sent_from_para(raw_text1, 0.5, 2)

# print('Top 2 Sentences of Each SubTopic:')
# for paragraph in n_sents:
#   for s in paragraph:
#     print(s, end=' ')
#   print('\n')

# print('===========================================\n')
