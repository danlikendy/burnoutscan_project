# burnoutscan_project

Прогнозирование риска выгорания сотрудников на основе метрик электронной почты и корпоративной переписки.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

### 1. FastAPI (backend)
```bash
cd api
uvicorn main:app --reload
```

### 2. Streamlit (одиночный прогноз)
```bash
cd apps
streamlit run streamlit_app.py
```

### 3. Streamlit (массовый прогноз)
```bash
cd apps
streamlit run bulk_prediction_app.py
```

## Структура проекта

```
BurnoutScan/
│
├── apps/                   
│   ├── streamlit_app.py           ← одиночный прогноз
│   └── bulk_prediction_app.py     ← массовый прогноз
│
├── api/
│   └── main.py             ← FastAPI backend
│
├── models/
│   └── rf_balanced_model.pkl  ← обученная модель
│
├── data/
│   ├── feats.csv               ← признаки по сотрудникам
│   └── burnout_predictions.csv ← результат массового прогноза
│
├── requirements.txt
├── README.md
└── .bat
```

## Описание

- `main.py`: сервер с эндпоинтами `/predict` и `/bulk_predict`
- `streamlit_app.py`: UI для прогноза по одному сотруднику
- `bulk_prediction_app.py`: массовый прогноз с графиком и выгрузкой
- `feats.csv`: агрегированные поведенческие фичи
