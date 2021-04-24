import transformers
import pandas as pd 
import torch

from update_db import update_full

#import datasets
from transformers import BertTokenizer, EncoderDecoderModel, T5ForConditionalGeneration,T5Tokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = "cpu"


body_tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
body_model = EncoderDecoderModel.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")
body_model.to(device)

"""
title_tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
title_model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
title_model.to(device)
"""

batch_size = 8 #16  # change to 64 for full evaluation


def generate_summary(articles, title=False):
    # Tokenizer will automatically set [BOS] <text> [EOS]
    # cut off at BERT max length 512
    if title==True:
        text=' '.join(articles)
        inputs = title_tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids.to(device)
        attention_mask = inputs.attention_mask.to(device)

        outputs = title_model.generate(input_ids, attention_mask=attention_mask)

        output_str = title_tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return output_str
    else:
        text=' '.join(articles)
        inputs = body_tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids.to(device)
        attention_mask = inputs.attention_mask.to(device)

        outputs = body_model.generate(input_ids, attention_mask=attention_mask)

        output_str = body_tokenizer.batch_decode(outputs, skip_special_tokens=True)

        return output_str

clustered=pd.read_csv('./../manual_cluster.csv', header=None)
article_list=pd.read_csv('article_list.csv')

summ_titles = []
summ_texts = []
for cluster in clustered.groupby(2).groups:
    article_index = dict(clustered.groupby(2).groups)[cluster]
    article_ids = list(clustered.iloc[article_index,0])

    article_headlines = list(article_list[article_list.iloc[:,0].isin(article_ids)]['title'])
    article_links = list(article_list[article_list.iloc[:,0].isin(article_ids)]['link'])
    

    sum_title = article_headlines[0]
    #sum_title = generate_summary(list(article_list[article_list.iloc[:,0].isin(article_ids)]['title']), title=True)
    summ_txt = generate_summary(list(article_list[article_list.iloc[:,0].isin(article_ids)]['text']))
    
    summ_txt[0] = '. '.join(i.capitalize() for i in summ_txt[0].split('. '))
    #print(sum_title[0] , summ_txt[0], article_links , article_headlines)
    update_full(article_headlines[0] , summ_txt[0], article_links , article_headlines)
    

    summ_titles.append(sum_title)
    summ_texts.append(summ_txt)

summ_articles = pd.DataFrame(
    {
        'summ_titles' : summ_titles,
        'summ_texts' : summ_texts
    }
)


summ_articles.to_csv('summ_articles_2.csv', index=False)