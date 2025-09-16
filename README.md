# 🌦️ Weather JSON-RPC API (FastAPI + Open-Meteo)

This project provides a **JSON-RPC API** built with **FastAPI** that fetches current weather information for any city using the [Open-Meteo API](https://open-meteo.com/).

---

## 🚀 Features
- JSON-RPC 2.0 compliant endpoint (`/jsonrpc`)
- Tool-based structure (easily extendable for more tools)
- Fetches:
  - City name
  - Coordinates (latitude, longitude)
  - Current weather (temperature, windspeed, etc.)
- Error handling for invalid cities or missing arguments

---

## 📦 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/weather-jsonrpc.git
   cd weather-jsonrpc
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (optional, if you plan to use **OpenWeather** in future):

   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

---

## ▶️ Running the Server

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

Server will be running at:

```
http://127.0.0.1:8000
```

---

## 📡 API Usage

### 1. List Available Tools

**Request:**

```json
POST /jsonrpc
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "id": "get_weather",
      "name": "Get current weather",
      "description": "Returns current weather for a city. Args: {city, units}",
      "input_schema": {
        "type": "object",
        "properties": {
          "city": {"type": "string"}
        }
      }
    }
  ]
}
```

---

### 2. Get Current Weather

**Request:**

```json
POST /jsonrpc
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "tool": "get_weather",
    "args": {
      "city": "Delhi",
      "units": "metric"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tool": "get_weather",
    "city": "Delhi",
    "latitude": 28.6667,
    "longitude": 77.2167,
    "weather": {
      "temperature": 30.2,
      "windspeed": 4.1,
      "winddirection": 120,
      "weathercode": 1,
      "time": "2025-09-17T00:00"
    }
  }
}
```

---

## ⚙️ Project Structure

```
.
├── main.py        # FastAPI + JSON-RPC logic
├── requirements.txt
├── .env           # API keys (optional)
└── README.md
```

---

## 📜 License
MIT License. Feel free to use and modify.

---

## 🙌 Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Open-Meteo](https://open-meteo.com/) for free weather & geocoding APIs
