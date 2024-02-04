"""
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import tokenize

# nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

text = "Amazon is to invest up to $4bn (£3.2bn) in the startup Anthropic, which has created a rival to ChatGPT called Claude, as the Silicon Valley giant seeks to keep pace with rivals including Microsoft and Google in the race to dominate the artificial intelligence space. Under the terms of the deal, Amazon will invest an initial $1.25bn into Anthropic, which was founded about two years ago by former research executives from the ChatGPT developer OpenAI, and take a minority stake in the business. Amazon said its investment in Anthropic, which recently announced its new AI chatbot Claude 2, can be increased to up to $4bn. “We have tremendous respect for Anthropic’s team and foundation models, and believe we can help improve many customer experiences, short- and long-term, through our deeper collaboration,” said the Amazon chief executive, Andy Jassy. Amazon’s move to strike a strategic partnership with a successful AI startup follows Microsoft’s multibillion-dollar deal with OpenAI in January, which included becoming its exclusive cloud provider. Under the terms of Amazon’s deal, Anthropic will use Amazon Web Services as its primary cloud provider for the “majority of workloads”, although it is not an exclusive arrangement, and use AWS-designed chips in the foundation models that underpin its AI applications. Foundation models are large AI programs trained on vast amounts of data, so they can be adapted to solve a wide range of tasks. Amazon is seeking to make its Trainium and Inferentia chips viewed as alternatives to those developed by Nvidia, the early market leader in the generative AI space, for training and running models. As part of the deal, Anthropic will provide customers that use Amazon’s AWS services with early access to unique features for “model customisation and fine-tuning capabilities”. The chief executive and co-founder of Anthropic, Dario Amodei, said: “By significantly expanding our partnership, we can unlock new possibilities for organisations of all sizes, as they deploy Anthropic’s safe, state-of-the-art AI systems together with AWS’s leading cloud technology.” Anthropic is one of the main competitors to OpenAI in the fledgling, but rapidly growing, AI sector. Last year, Google invested $300m in Anthropic and the company said it would train its models on Google’s chips and use its cloud services. In June, another rival, the year-old Silicon Valley-based Inflection AI, raised $1.3bn in funding led by Microsoft and Nvidia."

entities = ["Amazon", "Microsoft", "Google"]

#
sentences = tokenize.sent_tokenize(text)

for sentence in sentences:
    for entity in entities:
        if entity in sentence:
            sentiment_score = sid.polarity_scores(sentence)
            print(f"Sentence: {sentence}, Sentiment Score: {sentiment_score}")
        print("Entity not found in sentence")
#

for entity in entities:
    if entity in text:
        sentiment_score = sid.polarity_scores(text)
        print(f"Entity: {entity}, Sentiment Score: {sentiment_score}")
    else:
        print(f"Entity {entity} not found in text")
"""

from textblob import TextBlob

# Text containing opinions about different entities
text = "The iPhone 12 has a great camera but its battery life is not good. However, Samsung Galaxy S21's camera is worse but it has an excellent battery life."

# Entities we're interested in
entities = ["iPhone 12", "Samsung Galaxy S21"]

# For each entity, find sentences mentioning the entity and compute sentiment
for entity in entities:
    entity_sentences = [sentence for sentence in text.split('. ') if entity in sentence]
    entity_sentiment = [TextBlob(sentence).sentiment.polarity for sentence in entity_sentences]
    average_sentiment = sum(entity_sentiment) / len(entity_sentiment) if entity_sentiment else 0
    print(f"Entity: {entity}, Average Sentiment: {average_sentiment}")