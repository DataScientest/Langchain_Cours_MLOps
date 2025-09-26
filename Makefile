api: 
	uvicorn src.api.main:app --reload

streamlit: 
	streamlit run src/app.py

