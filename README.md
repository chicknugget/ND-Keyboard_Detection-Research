# 🎭 Emotion Detection via Keystroke Dynamics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.1%2B-orange.svg)](https://kivy.org/)

**Mobile research app that captures keystroke dynamics across induced emotions (happy, sad, frustrated, bored, relaxed, stressed) for AI emotion detection models.**

## 🎯 Research Overview

Traditional emotion detection uses cameras/microphones. **This app captures subtle patterns in *how people type***:
- Typing speed between keys (flight time)
- Key press duration (dwell time)  
- Error patterns and backspaces
- Rhythm changes per emotional state

**Hypothesis**: Emotions create unique "typing fingerprints" detectable by ML models.

**Target datasets**: Compatible with EmoSet 118K, FindingEmo-Light, custom keystroke datasets.

## 🏗️ Architecture

emotion_study_app/

├── app/

│ ├── screens/ # User journey (consent → games → debrief)

│ ├── games/ # Emotion induction tasks (happy_game.py, etc.)

│ ├── keyboard/ # Custom keystroke-capturing keyboard

│ ├── data/ # SQLite + CSV export for ML training

│ └── managers/ # Session/task sequencing

├── assets/ # Images, sounds, fonts

└── kv/ # Kivy UI layouts (.kv files)


**Key Components**:
- **BaseGame ABC**: Standardized game interface (score, timing, feedback)
- **CustomKeyboard**: Millisecond-precise keystroke logging
- **TaskSequencer**: Randomizes emotion order, prevents order effects

## 🚀 Quick Start

### 1. Development (Desktop)
```bash
# Clone & install
git clone <your-repo>
cd emotion_study_app
pip install -r requirements.txt

# Run on desktop
python main.py
2. Android APK (Research Deployment)
bash
# Install Buildozer
pip install buildozer

# First build (downloads Android SDK)
buildozer android debug

# Deploy to phone
buildozer android debug deploy run
Requirements: Ubuntu/macOS, 8GB+ RAM, Android phone for testing.
```
## 📱 Research Protocol
1. Consent & Demographics
2. Instructions: "Follow game → feel emotion → type required sentence"
3. 6 Games (random order): happy → sad → frustrated → bored → relaxed → stress
4. Post-task: Self-reported emotion (1-10 scale)
5. Data export: CSV with keystroke timings + metadata

## 🧪 Example Data Analysis
python
import pandas as pd
df = pd.read_csv('keystrokes.csv')

## 📄 License

MIT License - see LICENSE
