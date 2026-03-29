import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="店販収益シミュレーター | Luxia", layout="wide")

st.title("📊 サロン店販収益シミュレーター")
st.markdown("サロン様への導入特典（利益額）をその場で即座に決断します。")

# --- 入力エリア（サイドバー） ---
st.sidebar.header("1. 商品・仕入条件の設定")
product_name = st.sidebar.text_input("商品名", value="ROMAN スキンケアローション")
retail_price = st.sidebar.number_input("販売価格（税込）", min_value=0, value=3980, step=100)
wholesale_rate = st.sidebar.slider("仕入掛率（％）", min_value=30, max_value=80, value=60, step=5)

st.sidebar.divider()
# ※ダブっていた部分を1つに統合しました
st.sidebar.header("2. サロン側の設定")
staff_commission = st.sidebar.number_input("スタッフ店舗割引（1個あたり円）", min_value=0, value=500, step=100)
monthly_sales_target = st.sidebar.slider("月間販売目標（個）", min_value=1, max_value=200, value=30, step=1)

# --- 計算ロジック ---
# 卸値（サロンの仕入原価）
wholesale_price = int(retail_price * (wholesale_rate / 100))
# サロンの1個あたり粗利
gross_profit_per_item = retail_price - wholesale_price
# サロンの1個あたり純利益（手当控除後）
net_profit_per_item = gross_profit_per_item - staff_commission

# 月間・年間の利益計算
monthly_gross_profit = gross_profit_per_item * monthly_sales_target
monthly_net_profit = net_profit_per_item * monthly_sales_target
annual_net_profit = monthly_net_profit * 12

# --- メイン画面（結果表示） ---
st.header(f"✨ 【{product_name}】導入シミュレーション結果")

# KPI指標のハイライト表示
col1, col2, col3 = st.columns(3)
col1.metric("サロン様仕入先", f"{wholesale_price:,}円")
col2.metric("1個あたりのサロン純利益", f"{net_profit_per_item:,}円")
col3.metric("年間見込・純利益", f"{annual_net_profit:,}円", "↑ スタッフ手当支払い後")

st.divider()

# 月間と年間の利益詳細
st.subheader("📈 利益構造の内訳")
col4, col5 = st.columns(2)

with col4:
    st.markdown(f"**月間販売目標**: {monthly_sales_target} 個 （1日約 {monthly_sales_target//30} 個）")
    st.markdown(f"- 月間売上: {retail_price * monthly_sales_target:,}円")
    st.markdown(f"- 月間仕入原価: {wholesale_price * monthly_sales_target:,}円")
    st.markdown(f"- スタッフ還元総額: {staff_commission * monthly_sales_target:,}円")
    st.markdown(f"**▶︎ サロン月間純利益: {monthly_net_profit:,}円**")

with col5:
    # グラフ化のためのデータフレーム作成
    df = pd.DataFrame({
        "項目": ["売上高", "仕入原価", "スタッフ手当", "サロン純利益"],
        "金額（月間）": [
            retail_price * monthly_sales_target,
            wholesale_price * monthly_sales_target,
            staff_commission * monthly_sales_target,
            monthly_net_profit
        ]
    })
    # シンプルな棒グラフで視覚化
    st.bar_chart(df.set_index("項目"))

st.info("💡 経営のポイント：スタッフ様への手当を考えても、年間でこれだけのキャッシュがサロンに残る構造が作れます。")