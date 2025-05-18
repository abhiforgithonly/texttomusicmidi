# 🎶 Text-to-Music Generation App

This is a Streamlit-based web application that allows users to generate music from text prompts using Meta's [Audiocraft](https://github.com/facebookresearch/audiocraft) (MusicGen) and related models. 

## ✨ Features

- 🎼 Generate music from natural language prompts.
- 🎧 Play and download the generated music directly in the app.
- ⚙️ Built with `Streamlit`, `Torch`, `Torchaudio`, and Meta's `Audiocraft`.
- 🧠 Leverages pretrained AI models for music generation.
- 🎹 Optional: MIDI support and enhanced audio separation (Demucs).

## 🚀 Getting Started

### 1. Clone the repository and Audiocraft

git clone https://github.com/your-username/text-to-music-generation-app.git

cd text-to-music-generation-app

Clone Audiocraft: git clone https://github.com/facebookresearch/audiocraft.git


### 2. Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt
Note: This may take time as Audiocraft and torch are heavy dependencies.

### 4. Run the app
streamlit run app.py

### 🛠 Requirements
Python 3.10 or 3.11
Internet connection (to download models on first run)

📃 License
This project is for educational and non-commercial use. Please refer to Audiocraft's license for model usage.

🙋‍♂️ Author
Abhijeet
Built with ❤️ using open-source AI tools.
