# Customer Support ChatBot with Machine Learning, Ollema

## Overview
This project creates a modern customer service chatbot with a unique "speak aloud"
feature that makes it different from other chatbots that only interact with users through
text. Our chatbot, driven by machine learning, answers the world's problems with
customer engagement by efficiently translating spoken inquiries. In addition to text
messaging, the UI is enhanced with several features in one chatbot, such as a
microphone for voice input, an image-to-text converter, and a quick copy feature. This
novel approach seeks to provide fast, easy, and adaptable answers to consumer
questions, changing how customer service is provided by taking a thorough and
formally organized approach.

## Features
- **Intent Recognition:** Using ML models, the chatbot identifies the intent behind customer queries, allowing it to respond appropriately and direct users to the relevant information or support resources.

- **Multichannel Support:** The chatbot is designed to work across multiple communication channels, such as web chat, messaging apps, and more, ensuring a seamless and consistent customer support experience.

- **Learning and Improvement:** The chatbot incorporates a learning mechanism that allows it to continuously improve its responses over time based on user interactions. This ensures that the chatbot adapts to changing customer needs and evolves with the business.

- **Integration with Backend Systems:** The chatbot is integrated with backend systems, enabling it to retrieve real-time information and provide up-to-date responses to customer queries.

## Technologies Used

- **Frontend:**
  - HTML
  - CSS
  - JavaScript

- **Backend:**
  - MongoBb

- **Algorithms:**
  - Large Language Model (LLM)
  - Machine Learning (ML) algorithms

## Folder Structure
```
CHATBOTML/
|-- static/
|   |-- CSS/
|   |   |-- chathistory.css
|   |   |-- dashboard.css
|   |   |-- exit.css
|   |   |-- help.css
|   |   |-- index.css
|   |   |-- login.css
|   |   |-- notfound.css
|   |   |-- otp.css
|   |-- images/
|   |-- js/
|   |   |-- dashboard.js
|   |   |-- help.js
|   |   |-- notfound.js
|   |   |-- otp.js
|-- templates/
|   |-- dashboard.html
|   |-- exit.html
|   |-- help.html
|   |-- index.html
|   |-- login.html
|   |-- notfound.html
|   |-- otp.html
|   |-- register.html
|   |-- reset.html
|   |-- setpassword.html
|-- db.py
|-- main.py
|-- utils.py
```

## Prerequisites
- Python >3.10
- Pip
- Virtual Environment
- MongoDB

## Installation
1. Clone the repository:
```
git clone https://github.com/your-username/customer-support-chatbot.git
```

2. Navigate to the project directory:
```
cd customer-support-chatbot
```

3. Install Dependencies:
```
pip install -r requirements.txt
```

Note: Using virtualenv and installing requirements is more better way.
## Usage
1. Run the chatbot application:
```
python main.py
```

2. Access the chatbot through the specified endpoint or integration point.

## Some Images of the working webpages
<img src="Screenshot 2023-11-24 074151.png" alt="Image Alt text" width="300"/>

## Contact
For questions or inquiries, please contact chatbotwithml@gmail.com.
