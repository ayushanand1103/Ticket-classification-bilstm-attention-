# Ticket Classification System — BiLSTM + Attention

An end-to-end NLP system that automatically classifies customer support tickets into departments using a Bidirectional LSTM with Attention mechanism, backed by a MongoDB database for full ticket lifecycle management — now with a fully connected web frontend.

---

## What It Does

When a user submits a support ticket, the system:

1. Preprocesses and tokenises the ticket text
2. Runs it through a trained BiLSTM + Attention model
3. Classifies it into one of three departments:
   - IT / Technical Support
   - Customer Service
   - Billing / Finance
4. Stores the ticket and routes it to the correct MongoDB collection automatically
5. Returns a unique **Ticket ID** to the user for future lookup, updates, or deletion

---

## Download Trained Model

The trained model file is too large for GitHub. Download it here:
**[bilstm_attention_ticket_classifier.keras — Google Drive](https://drive.google.com/file/d/1KtZErsJ60C_STEIg5TXL9DbbUVYXE1tv/view?usp=drive_link)**

After downloading, place the file in the same directory as `main.py` before running the backend.

---

## Project Structure

```
Ticket-classification-bilstm-attention/
│
├── Preprocessing.ipynb                      # Data loading, label mapping, multilingual translation
├── Model_trian_diff_categories_tickets.ipynb # BiLSTM + Attention model training
├── main.py                                  # MongoDB CRUD backend + inference pipeline
├── app.py                                   # Flask REST API — connects frontend to backend
├── ticketing_frontend.html                  # Web frontend — raise, lookup, update, delete tickets
├── tokenizer.pkl                            # Saved Keras tokenizer
└── README.md
```

---

## Frontend

A dark, terminal-style web interface built in plain HTML/CSS/JS. No frameworks required — just open the file in a browser.

**Features:**
- **Raise Ticket** — submit name, email, phone, and ticket description; department is auto-assigned by the ML model; Ticket ID is returned on success
- **Lookup** — fetch any field (name, email, phone, ticket text, status, department) using a Ticket ID
- **Update** — update any field; updating the ticket description re-runs ML classification and re-routes automatically
- **Delete** — permanently removes the ticket from all MongoDB collections

**To run the frontend:**

```bash
# Install Flask dependencies (one time)
pip install flask flask-cors

# Start the backend API
python app.py

# Then open ticketing_frontend.html in your browser
```

The frontend communicates with the Flask API running at `http://localhost:5000`.

---

## Model Architecture

```
Input (seq length: 500)
→ Embedding (vocab: 20,000 | dim: 128 | mask_zero=True)
→ Bidirectional LSTM (128 units, return_sequences=True)
→ Self-Attention (Keras Attention layer)
→ GlobalAveragePooling1D
→ Dropout (0.5)
→ Dense (3 units, softmax)
```

- **Loss:** Sparse Categorical Cross-Entropy
- **Optimizer:** Adam
- **Training:** EarlyStopping on val_loss (patience=3), batch size 64, up to 10 epochs
- **Train/Val split:** 90/10

---

## Dataset & Preprocessing

- **Source:** Tobi-Bueck/customer-support-tickets via HuggingFace Datasets
- Dataset contained tickets in multiple languages (English and German)
- **Multilingual handling:** German tickets were translated to English using `Helsinki-NLP/opus-mt-de-en` (MarianMT transformer) via HuggingFace Transformers, with GPU acceleration (CUDA) and batched inference
- 15+ original queue categories were remapped into 3 business departments
- "General Inquiry" tickets were dropped (ambiguous label)
- **Labels:** IT/Tech → 0, Customer Service → 1, Billing/Finance → 2

---

## Database (MongoDB + PyMongo)

The `main.py` backend implements a multi-collection MongoDB architecture:

| Collection | Purpose |
|---|---|
| `User_info` | Master collection — stores all ticket data with user details |
| `IT_Tech` | Routed IT/Technical tickets |
| `Customer_service` | Routed Customer Service tickets |
| `Billing_finance` | Routed Billing/Finance tickets |

**Features:**
- JSON Schema validation (`$jsonSchema`) enforced at database level
- Full CRUD: insert, read (name / email / phone / ticket / status / department), update, delete
- On ticket update — old departmental record deleted, new prediction run, re-routed automatically
- On delete — ticket removed from all collections
- `insert()` returns the MongoDB `_id` as Ticket ID so users can reference their ticket

---

## How to Run

### 1. Install dependencies
```bash
pip install tensorflow pymongo transformers datasets pandas numpy flask flask-cors
```

### 2. Download the trained model
Download `bilstm_attention_ticket_classifier.keras` from the link above and place it in the project directory.

### 3. Preprocess data *(optional — only if retraining)*
Run `Preprocessing.ipynb` — loads the dataset, translates German tickets, maps labels, saves processed CSV.

### 4. Train the model *(optional — only if retraining)*
Run `Model_trian_diff_categories_tickets.ipynb` — tokenises text, trains the BiLSTM+Attention model, saves `.keras` and `tokenizer.pkl`.

### 5. Start the backend API
```bash
python app.py
```
Make sure MongoDB is running locally on `mongodb://localhost:27017/`.

### 6. Open the frontend
Double-click `ticketing_frontend.html` in File Explorer — it opens in your browser and connects to the running Flask API automatically.

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Deep Learning | TensorFlow / Keras |
| NLP | Keras Tokenizer, Sequence Padding |
| Translation | HuggingFace Transformers (MarianMT) |
| Data | HuggingFace Datasets, Pandas, NumPy |
| Database | MongoDB, PyMongo |
| Backend API | Flask, Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| Serialisation | Pickle (.pkl), Keras (.keras) |

---

## Author

**Ayush Anand**
B.Sc. Data Science & AI, Christ University Delhi NCR

