# Description of APP

This app allows users to compare personal writing with AI to look for similarities in writing style. The user simply uploads their writing and the application will ask
chatGPT to generate an article based on a summary of the users article. This is then compared against the users article to search for similiarties in writing. <br />

The user can also compare multiple user written articles against each other to search for similarities in sentence structure between the articles.

# Demo Video
https://github.com/matthewgottwald/SentenceSimilarityDetector/assets/45056814/e9b0dd6b-eb54-4149-88c2-38c7fae0bff3



# Loading screen of application
<img width="959" alt="Screenshot 2023-05-16 130144" src="https://github.com/matthewgottwald/SentenceSimilarityDetector/assets/45056814/3f5bbd11-63d4-4140-9721-5da68a97d9de">


# User uploaded file + clusters of similarity with ChatGPT
<img width="952" alt="Screenshot 2023-05-16 130214" src="https://github.com/matthewgottwald/SentenceSimilarityDetector/assets/45056814/4ac41710-5ab6-4d1d-b8d5-85d4e77cde6a">

# To setup the SentenceSimilarity-Backend

Inside the SentenceSimilarity-Backend folder enter the following commands into commandline: <br />
bash <br />
python3 -m venv venv <br />
source venv/bin/activate <br />
pip3 install -r requirements.txt <br />

Navigate to the app.py file and enter your personally generated API key into the API_Key Constant https://platform.openai.com/overview <br />
This will be used for all the calls to ChatGPT API

# To run the SentenceSimilarity-Backend once setup is complete

bash <br />
source venv/bin/activate <br />
python3 app.py <br />

# To setup the SentenceSimilarity-Frontend

Inside the SentenceSimilarity-Frontend folder enter the following commands into commandline: <br />
npm i <br />

# To run the SentenceSimilarity-Frontend once setup is complete

bash <br />
npm start <br />
