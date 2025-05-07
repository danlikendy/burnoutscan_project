
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

st.set_page_config(page_title="Массовый прогноз", layout="centered")
st.title("Массовый прогноз выгорания")

st.markdown("Загрузите CSV-файл с признаками сотрудников для пакетной оценки риска")

uploaded_file = st.file_uploader("Загрузите файл (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.write("Предпросмотр загруженных данных:")
        st.dataframe(df.head())

        response = requests.post(
            "http://127.0.0.1:8000/bulk_predict",
            json=df.to_dict(orient="records")
        )

        if response.status_code == 200:
            predictions = pd.DataFrame(response.json())
            result_df = pd.concat([df.reset_index(drop=True), predictions], axis=1)

            st.success("Прогнозы получены:")
            st.dataframe(result_df)

            # Визуализация Топ-25 сотрудников
            if "ID" in result_df.columns and "probability" in result_df.columns:
                try:
                    top25_df = result_df.sort_values(by="probability", ascending=False).head(25)

                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.barplot(
                        data=top25_df,
                        x="probability",
                        y="ID",
                        hue="prediction",
                        dodge=False,
                        palette="Blues_r",
                        ax=ax
                    )
                    ax.set_xlabel("Вероятность риска")
                    ax.set_ylabel("ID сотрудника")
                    ax.set_title("Топ 25 сотрудников с наивысшим риском выгорания")
                    ax.grid(axis="x", linestyle="--", alpha=0.3)
                    ax.legend(title="prediction")
                    plt.tight_layout()

                    # Вставка графика как изображения
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    image_base64 = base64.b64encode(buf.read()).decode()

                    image_html = f'''
                    <div style="background-color: #111827; padding: 25px; border-radius: 20px; margin-bottom: 30px;">
                        <h3 style="color: white; text-align: center; margin-bottom: 20px;">Топ 25 сотрудников по риску</h3>
                        <img src="data:image/png;base64,{image_base64}" style="width: 100%; border-radius: 20px;" />
                    </div>
                    '''
                    st.markdown(image_html, unsafe_allow_html=True)

                except Exception as vis_err:
                    st.warning(f"Ошибка визуализации: {vis_err}")

            # Кнопка для скачивания результата
            csv = result_df.to_csv(index=False).encode("utf-8")
            st.download_button("Скачать результат (CSV)", data=csv, file_name="burnout_predictions.csv", mime="text/csv")

        else:
            st.error(f"Ошибка при запросе к API: {response.status_code}")

    except Exception as e:
        st.error(f"Ошибка обработки файла: {e}")
