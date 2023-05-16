# Description of APP

This app allows users to compare personal writing with AI to look for similarities in writing style. The user simply uploads their writing and the application will ask
chatGPT to generate an article based on a summary of the users article. This is then compared against the users article to search for similiarties in writing. <br />

The user can also compare multiple user written articles against each other to search for similarities in sentence structure between the articles.

<img width="959" alt="Screenshot 2023-05-16 130144" src="https://github.com/matthewgottwald/SentenceSimilarity/assets/45056814/4f710a92-9ab7-4ae7-9040-9ef7646afcbc">

User uploaded file + clusters of similarity
<img width="952" alt="Screenshot 2023-05-16 130214" src="https://github.com/matthewgottwald/SentenceSimilarity/assets/45056814/e0333a9c-a8ab-415a-8607-60b15faa00ff">

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
