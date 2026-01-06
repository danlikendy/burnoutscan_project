# Система прогнозирования риска выгорания сотрудников

Прогнозирование риска выгорания сотрудников на основе метрик электронной почты и корпоративной переписки

[Ссылка на текст статьи](https://esj.today/PDF/04FAVN325.pdf)

## Возможности

- Оценка риска выгорания по поведенческим паттернам
- Визуализация Топ 25 сотрудников с высоким риском
- API для интеграции с внутренними системами
- Использование ML-модели (RandomForest / XGBoost)
- Локальный запуск, без утечки данных

## Стек технологий

- **Python 3.9+**
- `FastAPI`, `Streamlit`, `pandas`, `xgboost`, `scikit-learn`, `matplotlib`

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

## Установка

```bash
git clone https://github.com/danlikendy/burnoutscan_project.git
cd burnoutscan_project
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

## Приватность

- Все вычисления производятся локально
- Нет передачи данных в сеть
- Возможность удалить все результаты и модели

## Автор

Цыганцов Артём Сергеевич — [danlikendy](https://github.com/danlikendy)
