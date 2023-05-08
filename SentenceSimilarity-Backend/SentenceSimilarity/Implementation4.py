# source: https://github.com/UKPLab/sentence-transformers/blob/master/examples/application_clustering.py

"""
Sentences are mapped to sentence embeddings and then k-mean clustering is applied.
"""
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

#Downloads the tokenizer
embedder = SentenceTransformer('bert-base-nli-mean-tokens')

# Corpus with example sentences
corpus = ['In light of the latest developments and directives issued by the government of Ontario, Conestoga Mall will be closed to the public, as of midnight March 24th until at least April 7th, 2020', 
 '  Essential services will be maintained', 'In light of the latest developments and directives issued by the government of Ontario, Mapleview Shopping Centre will be closed to the public, as of midnight March 24th until at least April 7th, 2020', 
 "  We are committed to ensuring our communities' essential needs are met, while supporting public health and their efforts to contain the spread of COVID-19", 
 ' As per direction from our provincial government, only essential retailers will be open', 
 ' We will continue to support our communities during these unprecedented times and update you as the situation evolves', 
 ' We look forward to bringing our community back together', 'The safety and security of our guests, tenants, and employees is our utmost priority', 
 ' According to the latest government direction to help prevent the spread of COVID-19, only essential services remain open at Burlington Centre',
 'Landmark Cinemas is now closed', ' We are committed to the health and well-being of our cast and crew, our Guests, and the communities in which we operate', 
 ' We will continue to adhere to the directives of federal, provincial and municipal health authorities and will reopen when it is deemed appropriate', 
 ' We ask that you take care of yourselves, your families, and each other during these uncertain times', ' We look forward to welcoming you back soon', 
 'Please note, operating hours might temporarily vary due to the new COVID-19 coronavirus', 
 'To help protect the community and flatten the curve of COVID-19, the Government of Ontario has ordered the mandatory closure of all non-essential businesses as of 11:59 pm, Tuesday, March 24th', 
 '  This closure will be in effect for 14 days with the possibility of extending this order as the situation evolves', 
 ' Milton Mall will diligently enforce these new measures by restricting mall access to essential services only',
 '  This includes the immediate suspension of all formal or informal mall walking programs', 
 ' We will continue to take our direction in terms of operating and safety protocols from the Province of Ontario and Town of Milton and will communicate any further announcements as they become known to us',
 '  If unsure, we encourage you to call the store or service you are looking to visit to verify whether they are open or closed', 
 '  Store and service phone numbers may be found on our website under store directory', 
 ' Stay safe, keep washing those hands and we look forward to welcoming you back as soon as it’s safe to do so', 
 'The health and safety of our tenants and guests is of the utmost importance', 
 ' In accordance with the province of Ontario state of emergency, only the following tenants are open and may be accessed by the closest entrance', 
 ' Patrons visiting to walk the shopping centre will be asked to leave', ' Thank you for your cooperation', 'The health and safety of our customers, all employees at Square One and our community will always be our highest priority', 
 ' To help keep everyone as safe as possible, and to play our part in the containment of COVID-19, in compliance with the order of the Government of Ontario on March 23, 2020 and further clarified in a press conference by Premier Ford on March 24, 2020, we are closing Square One effective 11:59 pm, on Tuesday, March 24 for the next 14 days During this time, stores deemed essential will remain open and operational to ensure our community has access to essential services', 
 '   We understand this is a highly dynamic and evolving situation and we commit to providing you with regular updates', ' To help you prepare as much as possible, we will also be in contact as soon as we’re notified that it is appropriate to re-open Square One', ' CONTROLLED ACCESS WILL ONLY BE PROVIDED THROUGH ENTRANCE 7', ' We continue to encourage you to closely follow the advice of our local health authorities', 
 ' Our thoughts are with those impacted in our community and around the world', 'The health and safety of all who visit Eastgate Square is the property management team’s foremost priority, and as we are all learning in these challenging times, everybody has a role to play to protect the safety and well-being of our community', ' BGO is working in partnership with our tenants and we have advised tenants to follow the advice of the public health authority, as BGO is doing, and require that any employee who has been suspected or confirmed of COVID-19 exposure, or has come into contact with anyone suspected or confirmed to be infected with COVID-19, should immediately proceed with self-quarantine and provide notification to the local public health authorities', 
 'CF Toronto Eaton Centre is now closed', " We are committed to ensuring our communities' essential needs are met, while supporting public health and their efforts to contain the spread of COVID-19", ' As per direction from our provincial government, only essential retailers will be open', ' If you are an employee of the CF Toronto Eaton Centre access to the mall will be restricted to Level 2 Queen Street, between Yonge and James Street', 
 ' We will continue to support our communities during these unprecedented times and update you as the situation evolves', ' We look forward to bringing our community back together', ' For more information, we encourage you to review the following resources', 'To help protect the community and flatten the curve of COVID-19, the Government of Ontario has ordered the mandatory closure of all non-essential businesses as of Tuesday, March 24th', ' This closure will be in effect for 14 days with the possibility of extending this order as the situation evolves', ' Dixie Outlet Mall will diligently enforce these new measures by restricting mall access to essential services only', 
 ' At this time Guest Services will not be available and all walking programs have been removed due to COVID 19', ' We will continue to take our direction in terms of operating and safety protocols from the Province of Ontario and City of Mississauga and will communicate any further announcements as they become known to us', ' If unsure, we encourage you to call the store or service you are looking to visit to verify whether they are open or closed', '  Store and service phone numbers may be found on our website under store directory', ' Stay safe, keep washing those hands and we look forward to welcoming you back as soon as it’s safe to do so', 
 'In accordance with the State of Emergency declared in Ontario, Dufferin Mall, along with many of our shops and services, will be closed until further notice', ' If a store is not listed above then it is currently closed until further notice', ' We continue to monitor this situation very closely and we thank you for your co-operation as we navigate these challenging times together', 'According to the latest government direction to help prevent the spread of COVID-19, only essential services remain open at Oakville Place', ' Please contact the essential services directly to confirm their hours of operation', ' This is a highly dynamic situation', 
 ' As the COVID-19 situation evolves, RioCan remains committed to implementing appropriate actions and providing updaters to guests, tenants and employees as they become available', 'Heartland Town Centre plays a vital role in the Mississauga Community', ' We are a Centre that provides dining, services and places to get basic needs', ' The uncertainty created by COVID-19 has resulted in some retailers adjusting their store hours or temporarily closing their doors', 
 '  Please call the specific store you are looking to visit to confirm hours of operation', ' Due to the nature of the Heartland Town Centre being a non-enclosed Shopping Centre the hours of operation vary', ' Please contact the individual merchant directly for their designated hours', 'The health and safety of our customers, all employees at Yorkdale Shopping Centre and our community will always be our highest priority', ' To help keep everyone as safe as possible, and to play our part in the containment of COVID-19, in compliance with the order of the Government of Ontario on March 23, 2020 and further clarified in a press conference by Premier Ford on March 24, 2020, we are closing Yorkdale Shopping Centre effective 11:59 pm, on Tuesday, March 24 for the next 14 days', 
 ' During this time, stores deemed essential will remain open and operational to ensure our community has access to essential services', ' We understand this is a highly dynamic and evolving situation and we commit to providing you with regular updates', ' To help you prepare as much as possible, we will also be in contact as soon as we’re notified that it is appropriate to re-open Yorkdale Shopping Centre', ' We continue to encourage you to closely follow the advice of our local health authorities', ' Our thoughts are with those impacted in our community and around the world',
 'In light of the latest developments and directives issued by the government of Ontario, Outlet Collection at Niagara will be closed to the public, as of midnight March 24th until at least April 7th, 2020', ' Essential services will be maintained', ' Please check opening and closing hours with these tenants directly, as they may have reduced hours of operation', 'The mall is temporarily closed', ' Essential retailers remain open on a reduced schedule', ' Please contact individual retailers for details', 'At Yorkville Village, the health and safety of our community, customers and tenants is our highest priority', 
 ' We have increased sanitization procedures for all hand touch surfaces, installed hand sanitizers at all entrances, and have removed all seating in our Food Hall to adhere to social distancing practices', ' In the global effort to contain the spread of COVID-19, many of our retailers have elected to close', ' Please refer to individual store websites and social media accounts for current information, as well as options to purchase products online', ' Access to Yorkville Village will remain unchanged so that tenants providing essential services to our community can operate', ' We understand the growing concern in our community and are taking all appropriate measures to ensure our shopping centre remains safe', 
 ' We will continue to monitor information from the World Health Organization (WHO) and the Public Health Agency of Canada (PHAC) and will issue updates as necessary', 'In accordance with the State of Emergency declared in Ontario, commencing Wednesday, March 25th, 2020, Canada One will be closed until further notice', ' Thank you for your co-operation', 'Bramalea City Centre continues to be committed to the health and safety of our tenants, guests, staff and communities', 
 ' As a precautionary measure to help contain the spread of COVID-19, and per the order from the Government of Ontario on March 23, 2020, and further clarified in a press conference by Premier Ford on March 24, 2020, access to Bramalea City Centre will be maintained only to stores considered essential services for a 14-day period, effective March 24 at 11:59 pm', ' Currently, access to essential stores and services are available through Entrances 3 and 4(located by Dollarama and Shoppers Drug Mart)', ' Please see map below', ' We will continue to monitor this evolving situation and communicate with you as updates and events require additional attention', ' Please see below for a list of essential stores and services that remain open in Bramalea City Centre',
 ' Please contact each retailer for updated hours', 'The health & safety of our shoppers, employees and community is always our top priority', ' To help keep everyone in our community as safe as possible, to do our part to slow the spread of COVID-19, and in accordance with the order issued by the Government of Ontario, Promenade Shopping Centre will be closed commencing Wednesday, March 25th, 2020 for the next 14 days', ' During this time, only stores that are deemed essential will remain open and operational to ensure that our community has access to essential services', ' We continue to monitor this situation closely and commit to providing you with regular updates', ' We will also be in contact as soon as we’re notified that it is appropriate to re-open Promenade Shopping Centre',
 ' We continue to encourage you to closely follow the advice of our local health authorities', ' Our thoughts are with you all', 'Given the evolving situation concerning COVID-19, as a precautionary measure, Morguard is offering its retailers the option to reduce their store operating hours', ' Though some retailers will operate on reduced hours, Centerpoint Mall will remain open to the public during our regular operating hours to provide access to stores that have decided to operate as normal or are essential services', ' Morguard is committed to the health and safety of our tenants, guests, staff and communities', ' We will continue to monitor and communicate with you as updates and events require additional attention']


corpus_embeddings = embedder.encode(corpus)


num_clusters = 16
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(corpus_embeddings)
cluster_assignment = clustering_model.labels_    
 
def get_cluster_dict(clusters, sentences):
    max_cluster = max(clusters)
    cluster_dict = {}
    for i in range(-1, max_cluster + 1):
        cluster_dict[i] = []
    
    for i in range(len(clusters)):
        cluster = clusters[i]
        sentence = sentences[i]
        cluster_dict[cluster].append(sentence)
    
    return cluster_dict

print(get_cluster_dict(cluster_assignment, corpus))
