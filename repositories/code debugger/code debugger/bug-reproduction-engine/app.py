import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import sqlite3
from datetime import datetime

# =========================================================
# 1. ALL CORE FUNCTIONS (NLP + EXECUTION + DETECTION)
# =========================================================

def extract_steps(text):
    steps = []
    lines = text.lower().split("\n")

    for line in lines:
        url = re.findall(r'(https?://[^\s]+)', line)
        if url:
            steps.append(("open", url[0]))

        elif "open" in line:
            steps.append(("open", "https://example.com"))

        elif "username" in line:
            steps.append(("enter", {"type": "username", "value": "admin"}))

        elif "password" in line:
            steps.append(("enter", {"type": "password", "value": "123456"}))

        elif "enter" in line or "type" in line:
            steps.append(("enter", {"type": "text", "value": "test123"}))

        elif "click" in line:
            if "login" in line:
                steps.append(("click", "login"))
            elif "submit" in line:
                steps.append(("click", "submit"))
            else:
                steps.append(("click", "button"))

    return steps


def find_input(driver, field_type):
    inputs = driver.find_elements(By.TAG_NAME, "input")

    for inp in inputs:
        placeholder = (inp.get_attribute("placeholder") or "").lower()
        name = (inp.get_attribute("name") or "").lower()

        if field_type in placeholder or field_type in name:
            return inp

    return inputs[0] if inputs else None


def find_button(driver, text):
    buttons = driver.find_elements(By.TAG_NAME, "button")

    for btn in buttons:
        if text in btn.text.lower():
            return btn

    return buttons[0] if buttons else None


def run_steps(steps, run_id=0):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    screenshots = []
    logs = []

    for i, (action, value) in enumerate(steps):
        try:
            if action == "open":
                driver.get(value)
                logs.append(f"[Run {run_id}] Opened {value}")

            elif action == "enter":
                field = find_input(driver, value["type"])
                if field:
                    field.clear()
                    field.send_keys(value["value"])
                    logs.append(f"[Run {run_id}] Entered {value['type']}")

            elif action == "click":
                btn = find_button(driver, value)
                if btn:
                    btn.click()
                    logs.append(f"[Run {run_id}] Clicked {value}")

            time.sleep(2)

            file = f"run{run_id}_step_{i}.png"
            driver.save_screenshot(file)
            screenshots.append(file)

        except Exception as e:
            logs.append(f"[Run {run_id}] Error: {e}")
            break

    return driver, screenshots, logs


def detect_bug(driver):
    try:
        page = driver.page_source.lower()
        keywords = ["error", "invalid", "failed", "exception"]

        for word in keywords:
            if word in page:
                return True, word

        return False, None

    except:
        return False, "browser_closed"


def is_driver_alive(driver):
    try:
        driver.current_url
        return True
    except:
        return False


def run_multiple_times(steps, runs=3):
    results = []
    all_logs = []
    all_screenshots = []

    for i in range(runs):
        driver, screenshots, logs = run_steps(steps, i)

        if is_driver_alive(driver):
            result, _ = detect_bug(driver)
        else:
            result = False

        results.append(result)
        all_logs.extend(logs)
        all_screenshots.extend(screenshots)

        try:
            driver.quit()
        except:
            pass

    return results, all_logs, all_screenshots


def analyze_results(results):
    true_count = sum(results)

    if true_count == len(results):
        return "confirmed", "🚨 Bug Consistently Reproduced"
    elif true_count > 0:
        return "flaky", "⚠️ Flaky Bug (Sometimes Occurs)"
    else:
        return "none", "✅ No Bug Detected"


# =========================================================
# 2. DATABASE FUNCTIONS
# =========================================================

def init_db():
    conn = sqlite3.connect("bug_results.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bug_text TEXT,
        runs INTEGER,
        status TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_result(bug_text, runs, status):
    conn = sqlite3.connect("bug_results.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO results (bug_text, runs, status, timestamp) VALUES (?, ?, ?, ?)",
        (bug_text, runs, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("bug_results.db")
    c = conn.cursor()

    c.execute("SELECT * FROM results ORDER BY id DESC")
    data = c.fetchall()

    conn.close()
    return data


# =========================================================
# 3. INITIALIZE DATABASE
# =========================================================

init_db()


# =========================================================
# 4. UI CODE
# =========================================================

st.title("🐞 Bug Reproduction Engine – Phase 3 🚀")
st.write("Now supports real website testing + smart detection")

bug_text = st.text_area("Enter Bug Report")
runs = st.slider("Number of test runs", 1, 5, 3)

if st.button("Run"):
    if not bug_text.strip():
        st.warning("Enter bug report!")
    else:
        steps = extract_steps(bug_text)

        st.write("### 🧠 Extracted Steps")
        st.write(steps)

        st.write(f"### 🔁 Running {runs} times...")
        results, logs, screenshots = run_multiple_times(steps, runs)

        status, message = analyze_results(results)

        save_result(bug_text, runs, status)

        st.write("### 📊 Final Result")
        if status == "confirmed":
            st.error(message)
        elif status == "flaky":
            st.warning(message)
        else:
            st.success(message)

        st.write("### 🧾 Execution Logs")
        for log in logs:
            st.write(log)

        st.write("### 📸 Screenshots")
        for img in screenshots:
            st.image(img)

        st.info("Testing Completed ✅")


# =========================================================
# 📊 HISTORY SECTION
# =========================================================
st.write("## 📊 Test Dashboard")

history = get_history()

if history:
    df = pd.DataFrame(history, columns=[
        "ID", "Bug Report", "Runs", "Status", "Timestamp"
    ])

    # Short text
    df["Bug Report"] = df["Bug Report"].apply(
        lambda x: x[:60] + "..." if len(x) > 60 else x
    )

    # -------------------------------
    # 🔍 SEARCH
    # -------------------------------
    search = st.text_input("🔍 Search Bug Report")

    if search:
        df = df[df["Bug Report"].str.contains(search, case=False)]

    # -------------------------------
    # 🎯 FILTER
    # -------------------------------
    filter_option = st.selectbox(
        "Filter by Status",
        ["All", "confirmed", "flaky", "none"]
    )

    if filter_option != "All":
        df = df[df["Status"] == filter_option]

    # -------------------------------
    # 📊 METRICS
    # -------------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tests", len(df))
    col2.metric("🚨 Confirmed", (df["Status"] == "confirmed").sum())
    col3.metric("⚠️ Flaky", (df["Status"] == "flaky").sum())
    col4.metric("✅ None", (df["Status"] == "none").sum())

    # -------------------------------
    # 📋 TABLE
    # -------------------------------
    st.write("### 📋 Test History Table")
    st.dataframe(df, use_container_width=True)

    # -------------------------------
    # 📈 CHART
    # -------------------------------
    st.write("### 📈 Bug Distribution")

    status_counts = df["Status"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(status_counts.index, status_counts.values)
    ax.set_xlabel("Status")
    ax.set_ylabel("Count")

    st.pyplot(fig)

    # -------------------------------
    # 🗑️ CLEAR BUTTON
    # -------------------------------
    if st.button("🗑️ Clear History"):
        conn = sqlite3.connect("bug_results.db")
        c = conn.cursor()
        c.execute("DELETE FROM results")
        conn.commit()
        conn.close()
        st.success("History cleared! Refresh page")

else:
    st.info("No history yet")
