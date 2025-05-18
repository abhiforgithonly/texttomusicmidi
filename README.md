# 🎵 Text-to-Music Generation App

A Streamlit-based web application that transforms text prompts into original music using Meta's [Audiocraft](https://github.com/facebookresearch/audiocraft) and other powerful deep learning libraries.

---

## 🚀 Features

- Generate music directly from text prompts using Audiocraft.
- Streamlit UI for seamless interaction.
- Uses models like MusicGen and Encodec.
- Optional support for MIDI and audio processing.

---


---

## ⚙️ Setup Instructions


> **Note:** Due to the large size of Audiocraft and its models, this app is best run locally on a machine with at least 8GB RAM.



```bash
1. git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Clone Audiocraft Manually
Since Audiocraft is large, clone it separately in the same directory:
git clone https://github.com/facebookresearch/audiocraft.git
Make sure the folder structure looks like this:
your-repo-name/
├── app.py
├── requirements.txt
├── audiocraft/          ✅ Cloned manually


3. Create a Virtual Environment
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
4. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt
⚠️ Installation might take time due to heavy libraries like torch, torchaudio, transformers, and audiocraft.

5. Run the App
streamlit run app.py
