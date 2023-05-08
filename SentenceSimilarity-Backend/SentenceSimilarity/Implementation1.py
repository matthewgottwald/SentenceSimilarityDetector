#source: https://nlpforhackers.io/wordnet-sentence-similarity/


from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag (noun, verb, adjective ...) """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) for ss in synsets2])
 
        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1
 
    # Average the values
    if count == 0:
        score = 0
    else:
        score /= count
    return score

# Given a text file of document transcripts (divided by * symbols) 
# creates list of lists, each containing a sentence string,
# an index for the document it is from, and an index for the sentence 
# in the overall list
def make_sentence_list_from_file(myFile):
    f = open(myFile, 'r')
    f = f.read()
    f = ' '.join(f.splitlines()).replace(',', '')
    f.close()
    transcripts = f.split('*')
    mySentences = []
    for i in range(len(transcripts)):
        paragraph = transcripts[i].split('.')
        for sentence in paragraph:
            mySentences.append([sentence, i, len(mySentences)])
    return mySentences


# Given a string of document transcripts (divided by * symbols) 
# creates list of lists, each containing a sentence string,
# an index for the document it is from, and an index for the sentence 
# in the overall list
def make_sentence_list_from_string(myString):
    transcripts = myString.split('*')
    mySentences = []
    for i in range(len(transcripts)):
        paragraph = transcripts[i].split('.')
        for sentence in paragraph:
            mySentences.append([sentence, i, len(mySentences)])
    return mySentences

# Given a sentence list, constructs a matrix (list of lists)
# where each row and each column represent a sentence and then the entry (i,j)
# is the sentence_similarity score of the sentence i and sentence j
def make_distance_matrix(sentences):
    distanceMatrix = []
    length = len(sentences)
    for i in range(length):
        scores = []
        for j in range(length):
            if sentences[i][0] != '' and sentences[j][0] != '':
                scores.append(1 - sentence_similarity(sentences[i][0], sentences[j][0]))
            else:
                scores.append(0)
        distanceMatrix.append(scores)
    return(distanceMatrix)

myInput = (
    "As the world confronts COVID-19, we hope for your safety and wellbeing. We’ve heard from learners worldwide that they’re using this time to practice a language on Duolingo. With new updates coming, we hope Duolingo will help you stay motivated, too. Stay strong, and thank you for learning with us."
    + "*Hillel Ontario’s leadership has been meeting regularly to discuss the ever shifting and changing landscape within which we are now operating. With the imperative to make decisions that we believe to be in the best interest of our students, our staff and our community, and understanding the need to enforce social distancing for the betterment of all Canadians, we will be closing all of our campus Hillel spaces by the end of today. I appreciate that this is, for some, an incredibly stressful and potentially isolating time. Hillel Ontario’s campus staff will work hard to main virtual connectivity with students by moving as many programs online as possible and are already brainstorming ways to support our Jewish campus communities from afar. Wishing everyone good health, strength and patience as we navigate these uncharted waters."
    + "*With growing global concerns around COVID-19 (“coronavirus”), I wanted to provide you with an update on our response to date and our commitment to you moving forward. The health, safety and well-being of our employees and guests is Cineplex’s top priority and we are following the lead of Canadian public health authorities at this important time. We are committed to providing comfortable and safe entertainment experiences at our theatre circuit and locations of The Rec Room and Playdium across the country. First and foremost, I want to assure our guests that we are taking all appropriate measures to ensure our venues are safe and that we have existing plans and training protocols in place to ensure they stay that way. While the Public Health Agency of Canada has assessed the current public health risk associated with coronavirus as low, we continue to monitor for developments very closely."
    + "*Effective immediately, we are temporarily closing all stores in the US, Canada and Puerto Rico through March 28, due to COVID-19. Our top priority right now is the health, safety and security of our employees and our customers. Knowing that our company is the lifeblood of so many, we will continue to pay all store staff who were scheduled through this time. Our team will continue to monitor the situation daily, as it's fluid and continues to change. We understand that shopping for shoes may not be top of mind, but we are here to serve you when you are ready. We also have a 365-day return policy, so you can take your time when returning any purchases.We are all in this together and need to support one another. Over the next few weeks, we will continue to serve our Journeys community and family with creativity, positivity and inspiration through our digital channels, and we encourage you to do the same. Let’s all do our part to lift each other up in these tough times. We appreciate your patience and understanding."
    + "*We know that information about COVID-19 is probably overwhelming your screen, but we wanted to reach out and offer you some clarity and reassurance during this time of uncertainty. We’re doing everything we can to maintain our safe and healthy service and continue to meet all of your vision needs. Right now, the most important thing to us is the health and safety of our customers and our team members. With that in mind, we’re taking every precaution to make sure our stores, products, and supply chains remain clean and safe. We’ve implemented increased cleaning and sanitization procedures and are closely monitoring the wellbeing of our staff and suppliers. As the situation develops, we’ll keep you posted with any changes that may affect you. Our thoughts and priorities lie with our customers and our team, and we’ll continue to do everything we can to ensure the health and safety of the Clearly community."
    + "*Together with you, we are watching with increased concern the coronavirus health crisis that is affecting our world. What we know is that no one knows when it will end and how it will impact our daily lives both in the short and longer terms. Every day brings new regulations as nationally - both in Israel, and across North America - and individually, we search for responsible ways to respond and ensure the health and safety of ourselves and others. As an Institute we have responded proactively and cancelled all staff travel and large gatherings. We will continue to monitor the situation and respond accordingly. As is required by our tradition, the safety and concern for human life must always come first. We are also working to create online and other resources for our program participants across North America, not only to replace the programs that we have cancelled but also to strengthen the bonds of community and the opportunities for engagement and learning that many people are seeking in these complicated and often isolated times. We will continue to be in communication with you if anything becomes clearer in the meantime. With hopes and prayers for health in these trying times."
    + "*Like all of you, we’ve been closely monitoring the evolving Coronavirus pandemic as we hunker down and “socially distance” in hopes of flattening the curve. However, in many ways, we’re operating business as usual: We’ve always been a distributed company and every one of our 700 employees works from home. We are not the norm here, though. Many of you may be dealing with a sudden transition to working in a completely different manner—on top of acutely feeling the emotional and practical effects of this crisis within our community. While so many things are out of our control at the moment, the one thing we can do here at InVision is offer resources to aid this transition and keep the design community working productively throughout this unprecedented event. We’ve tailored our digest this week to be a resource to foster creativity, focus, and collaboration during this uncertain time, and will continue to focus on helping our community work creatively and seamlessly throughout the pandemic."
    + "*CAA was founded over a century ago with the core value and mission of keeping our Members safe. This has always been our top priority and takes on added importance during the COVID-19 pandemic. I wanted to reach out to you personally about what we are doing at CAA to keep our Members, Customers and Associates safe. Our Members continue to be impacted by this extraordinary situation and we have taken steps to ensure your safety and well-being. Road service will continue to operate without interruption. However, steps have been taken to prepare our roadside network. Drivers have been asked to limit physical contact with Members (no hand shaking). We have increased the frequency of cleaning and disinfecting of CAA trucks. Best practices to reduce the risk of illness have been shared across the network. Contact centres will continue to operate as normal, please call us for inquiries and service. We continue to offer services via phone and online seven days a week. We will be temporarily closing all stores across South Central Ontario starting March 17, 2020. Global Affairs Canada has advised all travellers to avoid non-essential travel outside of Canada until further notice. The safety and well-being of CAA Associates continues to be paramount. Effective immediately, CAA Associates who can work from home have been encouraged to do so. We are doing our part to help contain this pandemic. Despite the economic impacts of the pandemic on the travel industry, we will not layoff Associates or downsize the organization. Our Associates will be taken care of during this difficult time. Our priority is, as always, the safety and well-being of our Members and Associates. While we modify how we deliver on our services, rest assured that we remain committed to being there for our Members during these uncertain times."
    + "*In unprecedented times like these, we’re doing everything we can to serve thousands of communities across the U.S. We’re taking preventive measures to keep our stores clean and maintain a healthy environment. We’re working to keep products stocked and prices fair. And as the largest employer in the country, we’re working to take care of our associates, too, offering a new leave policy to ensure they have the support they need."
    + "*As we all continue to monitor the novel coronavirus (COVID-19) situation very closely, we wanted to reach out and share the actions Sephora North America is taking to keep our stores safe and clean for you, our employees, and the community at large. As your trusted partner in beauty, we are committed to delivering the Sephora experience you know and love in an environment that promotes and protects the well-being of all across the US and Canada. Hygiene standards for our people, store environment, products, and tools are and will always be a top priority. However, as the situation continues to evolve in North America, we have taken additional actions to ensure our entire organization is here to serve you in the safest way possible. All store employees have been trained to uphold and practice these measures, and we are closely following the latest guidance from the CDC, WHO, local governments, and public health agencies. We are prepared to navigate these challenging circumstances with everyone’s safety in mind. While our stores currently remain open for business, we recognize you may choose to shop from home."
)

sentenceList  = make_sentence_list_from_string(myInput)
distanceMatrix = make_distance_matrix(sentenceList)

from sklearn.cluster import DBSCAN
import numpy as np

# this clustering doesn't really work yet
clustering = DBSCAN(eps=.3, min_samples=3, metric="precomputed").fit(distanceMatrix)


labels = clustering.labels_