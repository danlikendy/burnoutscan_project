
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Одиночный прогноз", layout="centered")

@st.cache_data
def load_features():
    return pd.read_csv("data/feats.csv")

feats_df = load_features()
id_list = feats_df["ID"].tolist()

# Инициализация session_state

default_values = {
    "selected_id": None,
    "show_reset_msg": False,
    "avg_sent": 5.0,
    "median_sent": 4.0,
    "max_sent": 10.0,
    "std_sent": 3.0,
    "active_days_x": 20,
    "night_ratio": 0.1,
    "weekend_ratio": 0.1,
    "avg_msgs_per_day": 5.0,
    "unique_recipients": 15
}
for k, v in default_values.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Очистить всё

if st.button("Очистить"):
    for k, v in default_values.items():
        st.session_state[k] = v
    st.session_state["show_reset_msg"] = True

# Сообщение сброса

if st.session_state["show_reset_msg"]:
    st.success("ID сброшен. Выберите сотрудника снова")
    st.session_state["show_reset_msg"] = False

# Выбор ID

st.selectbox(
    "Сотрудник (ID)",
    [None] + id_list,
    index=0 if st.session_state["selected_id"] is None else id_list.index(st.session_state["selected_id"]) + 1,
    key="selected_id"
)

# Автозаполнение при выборе ID

if st.session_state["selected_id"] is not None:
    selected_data = feats_df[feats_df["ID"] == st.session_state["selected_id"]]
    if not selected_data.empty:
        row = selected_data.iloc[0]
        st.session_state["avg_sent"] = row["avg_sent"]
        st.session_state["median_sent"] = row["median_sent"]
        st.session_state["max_sent"] = row["max_sent"]
        st.session_state["std_sent"] = row["std_sent"]
        st.session_state["active_days_x"] = row["active_days_x"]
        st.session_state["night_ratio"] = row["night_ratio"]
        st.session_state["weekend_ratio"] = row["weekend_ratio"]
        st.session_state["avg_msgs_per_day"] = row["avg_msgs_per_day"]
        st.session_state["unique_recipients"] = row["unique_recipients"]

# Форма ввода

with st.form("input_form"):
    avg_sent = st.number_input("Среднее писем в день", value=st.session_state["avg_sent"])
    median_sent = st.number_input("Медиана писем в день", value=st.session_state["median_sent"])
    max_sent = st.number_input("Максимум писем в день", value=st.session_state["max_sent"])
    std_sent = st.number_input("Стандартное отклонение", value=st.session_state["std_sent"])
    active_days_x = st.number_input("Активных дней", value=st.session_state["active_days_x"])
    night_ratio = st.slider("Доля писем ночью", 0.0, 1.0, st.session_state["night_ratio"])
    weekend_ratio = st.slider("Доля писем в выходные", 0.0, 1.0, st.session_state["weekend_ratio"])
    avg_msgs_per_day = st.number_input("Средняя активность в день", value=st.session_state["avg_msgs_per_day"])
    unique_recipients = st.number_input("Уникальных адресатов", value=st.session_state["unique_recipients"])
    submit = st.form_submit_button("Предсказать")

# Обработка запроса

if submit:
    input_data = {
        "avg_sent": avg_sent,
        "median_sent": median_sent,
        "max_sent": max_sent,
        "std_sent": std_sent,
        "active_days_x": active_days_x,
        "night_ratio": night_ratio,
        "weekend_ratio": weekend_ratio,
        "avg_msgs_per_day": avg_msgs_per_day,
        "unique_recipients": unique_recipients
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=input_data)
        result = response.json()

        if result["prediction"] == "норма":
            st.success(f"Прогноз: **{result['prediction']}**")
        else:
            st.error(f"Прогноз: **{result['prediction']}**")

        st.info(f"Вероятность риска: **{result['probability']}**")
    except:
        st.error("Не удалось связаться с API. Убедитесь, что FastAPI запущен")
