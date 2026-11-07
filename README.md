# 🏎️ F1 Pitwall & Live Race Intelligence Dashboard

A full-stack Formula 1 telemetry analyzer and live pitwall telemetry station built with Python, Streamlit, OpenF1, and tif1/FastF1.

Designed for both seasoned race engineers and casual motorsport fans, this dashboard translates complex high-frequency car telemetry into interactive, plain-English race analytics.

---

## 🌟 Key Features

### 📡 1. Live Grand Prix Race Control (Powered by OpenF1)
* **Real-Time Timing Tower:** P1–P20 live leaderboard, sector splits ($S1, S2, S3$), gap to leader, intervals between cars, and speed traps.
* **F1 Cockpit HUD & Steering Wheel:** 
  * 15 RPM LED shift lights (Green $\to$ Red $\to$ Purple upshift cue).
  * Real-time gear indicator ($1$ to $8$, Neutral, Reverse).
  * Dynamic throttle & brake pressure meters.
  * Live DRS status indicator (`DRS OPEN` / `DRS CLOSED`).
* **Team Radio Audio Streamer:** Listen to official FIA driver-to-engineer broadcast radio clips in real time.
* **FIA Stewards & Flag Feed:** Instant alerts for Green, Yellow, Red flags, Safety Cars, and Track Limits notices.
* **Live Pitwall Weather Station:** Real-time asphalt temperature, ambient temperature, humidity, wind velocity, and rainfall tracking.
* **⚡ Live Auto-Poll Mode:** Set automatic polling every 10s, 15s, or 30s to keep timing fresh while watching the race.

### 🏎️ 2. Deep Telemetry & Lap Archives (Powered by tif1)
* **Driver Comparison Matrix:** Select any two drivers across any Grand Prix weekend (Practice, Qualifying, Sprint, Race).
* **🤖 Pitwall AI Race Analyst Verdict:** Automatic 3-bullet plain-English breakdown of straightline top speed advantage, minimum cornering speeds, and throttle aggression (% full throttle).
* **Synchronized Telemetry Stack:** Overlay Speed, Delta Time ($\Delta t$), Throttle/Brake application, Gear shifts, and RPM over distance.
* **2D Circuit GPS Map:** Interactive track layout colorable by Speed Heatmap, Gear Distribution, or Throttle/Braking zones.
* **Braking & Traction Dynamics:** Deceleration G-force bar charts and Traction Circle (G-G friction circle diagram).

---

## 🚀 Quickstart (Local)

### 1. Clone the repository
```bash
git clone https://github.com/thecarlover/f1-telemetry-analyzer.git
cd f1-telemetry-analyzer
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## 📱 Mobile Phone Access
When running locally on your Wi-Fi network:
* Access via `http://<your-local-ip>:8501`
* Or scan the QR code displayed directly in the dashboard sidebar.

---

## ☁️ Deployment

### Free 1-Click Deployment on Streamlit Community Cloud (Recommended):
1. Push this repository to your GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and click **New App**.
4. Select repository `thecarlover/f1-telemetry-analyzer`, branch `main`, and main file path `app.py`.
5. Click **Deploy!**

---

## 🛠️ Tech Stack
* **Frontend / Framework:** [Streamlit](https://streamlit.io/)
* **Visualization:** [Plotly](https://plotly.com/python/), [Matplotlib](https://matplotlib.org/)
* **Live Telemetry & API:** [OpenF1](https://openf1.org/)
* **Archive Telemetry:** [tif1](https://github.com/Casper-Guo/tif1) / FastF1
* **Data Processing:** Pandas, NumPy
