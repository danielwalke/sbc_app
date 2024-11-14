# SBC-SHAP
Web application for predicting sepsis and visualizing SHAP values for increased interpretability.

Requirements:
python>=3.X
node v16.14.0
npm 8.3.1

Install frontend:
```bash
cd frontend/sbc/
npm run install
```

Install backend:
```bash
cd backend
pip install -r .\requirements.txt
```

Run frontend:
```bash
cd frontend/
npm run dev
```


Run backend:
```bash
cd backend/
uvicorn main:app --reload
```
