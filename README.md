Ticket Classification System — BiLSTM + Attention
An end-to-end NLP system that automatically classifies customer support tickets into departments using a Bidirectional LSTM with Attention mechanism, backed by a MongoDB database for full ticket lifecycle management.

What It Does
When a user submits a support ticket, the system:

Preprocesses and tokenises the ticket text
Runs it through a trained BiLSTM + Attention model
Classifies it into one of three departments:

IT / Technical Support
Customer Service
Billing / Finance


Stores the ticket and routes it to the correct MongoDB collection automatically


Download Trained Model
The trained model file is too large for GitHub. Download it here:
🔗 Download bilstm_attention_ticket_classifier.keras (Google Drive)
After downloading, place the file in the same directory as main.py before running the backend.

Project Structure
Ticket-classification-bilstm-attention/
│
├── Preprocessing.ipynb                       # Data loading, label mapping, multilingual translation
├── Model_trian_diff_categories_tickets.ipynb # BiLSTM + Attention model training
├── main.py                                   # MongoDB CRUD backend + inference pipeline
├── tokenizer.pkl                             # Saved Keras tokenizer
└── README.md

Model Architecture
Input (seq length: 500)
    → Embedding (vocab: 20,000 | dim: 128 | mask_zero=True)
    → Bidirectional LSTM (128 units, return_sequences=True)
    → Self-Attention (Keras Attention layer)
    → GlobalAveragePooling1D
    → Dropout (0.5)
    → Dense (3 units, softmax)

Loss: Sparse Categorical Cross-Entropy
Optimizer: Adam
Training: EarlyStopping on val_loss (patience=3), batch size 64, up to 10 epochs
Train/Val split: 90/10


Dataset & Preprocessing

Source: Tobi-Bueck/customer-support-tickets via HuggingFace Datasets
Dataset contained tickets in multiple languages (English and German)
Multilingual handling: German tickets were translated to English using Helsinki-NLP/opus-mt-de-en (MarianMT transformer) via HuggingFace Transformers, with GPU acceleration (CUDA) and batched inference
15+ original queue categories were remapped into 3 business departments
"General Inquiry" tickets were dropped (ambiguous label)
Labels: IT/Tech → 0, Customer Service → 1, Billing/Finance → 2


Database (MongoDB + PyMongo)
The main.py backend implements a multi-collection MongoDB architecture:
CollectionPurposeUser_infoMaster collection — stores all ticket data with user detailsIT_TechRouted IT/Technical ticketsCustomer_serviceRouted Customer Service ticketsBilling_financeRouted Billing/Finance tickets
Features:

JSON Schema validation ($jsonSchema) enforced at database level
Full CRUD: insert, read (name/email/phone/ticket/status/department), update, delete
On ticket update — old departmental record deleted, new prediction run, re-routed automatically
On delete — ticket removed from all collections


How to Run
1. Install dependencies
bashpip install tensorflow pymongo transformers datasets pandas numpy
2. Download the trained model
Download bilstm_attention_ticket_classifier.keras from the link above and place it in the project directory.
3. Preprocess data (optional — only if retraining)
Run Preprocessing.ipynb — loads the dataset, translates German tickets, maps labels, saves processed CSV.
4. Train the model (optional — only if retraining)
Run Model_trian_diff_categories_tickets.ipynb — tokenises text, trains the BiLSTM+Attention model, saves .keras and tokenizer.pkl.
5. Run the backend
bashpython main.py
Make sure MongoDB is running locally on mongodb://localhost:27017/.

Tech Stack
CategoryToolsLanguagePythonDeep LearningTensorFlow / KerasNLPKeras Tokenizer, Sequence PaddingTranslationHuggingFace Transformers (MarianMT)DataHuggingFace Datasets, Pandas, NumPyDatabaseMongoDB, PyMongoSerialisationPickle (.pkl), Keras (.keras)

Author
Ayush Anand
B.Sc. Data Science & AI, Christ University Delhi NCR
