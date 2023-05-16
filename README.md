# Description of APP

This app allows users to compare personal writing with AI to look for similarities in writing style. The user simply uploads there writing and the application will ask
chatGPT to generate an article based on a summary of the users article. This is then compared against the users article to search for similiarties in writing.

# To setup the SentenceSimilarity-Backend

Inside the SentenceSimilarity-Backend folder enter the following commands into commandline:
bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

Navigate to the app.py file and enter your personally generated API key into the API_Key Constant https://platform.openai.com/overview
This will be used for all the calls to ChatGPT API

# To run the SentenceSimilarity-Backend once setup is complete

bash
source venv/bin/activate
python3 app.py

# To setup the SentenceSimilarity-Frontend

Inside the SentenceSimilarity-Frontend folder enter the following commands into commandline:
npm i

# To run the SentenceSimilarity-Frontend once setup is complete

bash
npm start
