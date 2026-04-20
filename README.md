# SenticGuard: AI-Powered Emotional Integrity & Media Resilience Framework  
### SenticGuard is an intelligent system designed to identify emotional manipulation mechanisms and sensationalism in Romanian news feeds, using BERT NLP technology.  

**The Problem: Fear Manipulation**  
Clickbait headlines and alarmist news are not just media noise; they are built on psychological triggers (e.g. fear, false urgency) that increase social anxiety and distort reality.  

**The Solution: Active Learning with Psychological Supervision**  
The system uses a learning cycle in which the AI ​​proposes and the specialist validates, constantly refining the detection criteria.

**Workflow: Active Learning & Deployment**  
The system works through a continuous improvement cycle between the administration and public applications:

* Collection & Pre-analysis (Admin App): Headlines are retrieved via RSS. The AI ​​model proposes a label (Informative/Alarmist) and a trust score.

* Human-in-the-Loop: The administrator confirms or corrects the AI's ticks. The data is saved in Google Sheets.

* Training (Google Colab): The model is periodically re-trained on new validated data to refine its accuracy.

* Update (Public App): The verification application automatically uses the newest model saved in Google Drive, providing increasingly accurate results. Demo (romanian) [here](https://senticguard-app.streamlit.app/)

**Technology Stack**

* AI: transformers (BERT Multilingual), PyTorch.

* Interface: Streamlit Cloud (Admin & Public Verifier).

* Storage: Google Sheets API (Dataset) & Google Drive (Model Storage).

* Infrastructure: Google Colab for GPU training.

**Vision**  
From the current binary detection (Informative vs. Alarmist), the project evolves towards the nuanced mapping of types of psychological manipulation (e.g. fear, demonization, false urgency, appeal to authority).
