import transformers
import pandas as pd 

#import datasets
from transformers import BertTokenizer, EncoderDecoderModel

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = EncoderDecoderModel.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")
model.to("cuda")

batch_size = 8 #16  # change to 64 for full evaluation


def generate_summary(articles):
    # Tokenizer will automatically set [BOS] <text> [EOS]
    # cut off at BERT max length 512
    text=' '.join(articles)
    inputs = tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")

    outputs = model.generate(input_ids, attention_mask=attention_mask)

    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    return output_str

clustered=pd.read_csv('manual_cluster.csv', header=None)
article_list=pd.read_csv('article_list.csv')

summ_titles = []
summ_texts = []
for cluster in clustered.groupby(2).groups:
    article_index = dict(clustered.groupby(2).groups)[cluster]
    article_ids = list(clustered.iloc[article_index,0])
    summ_titles.append(generate_summary(list(article_list[article_list.iloc[:,0].isin(article_ids)]['title'])))
    summ_texts.append(generate_summary(list(article_list[article_list.iloc[:,0].isin(article_ids)]['text'])))

summ_articles = pd.DataFrame(
    {
        'summ_titles' : summ_titles,
        'summ_texts' : summ_texts
    }
)


summ_articles.to_csv('summ_articles.csv', index=False)