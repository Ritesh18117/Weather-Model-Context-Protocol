import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

# ----------------------------
# Helper functions for JSON-RPC
# ----------------------------
def jsonrpc_result(id, result):
    return {"jsonrpc": "2.0", "id": id, "result": result}

def jsonrpc_error(id, code, message):
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}


# ----------------------------
# MCP Weather function (for Streamlit / direct call)
# ----------------------------
def get_weather(city: str, units: str = "metric"):
    """
    Fetch current weather for a city using Open-Meteo API
    """
    city_clean = city.strip().title()

    # Step 1: get latitude & longitude
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_resp = requests.get(
        geo_url,
        params={"name": city_clean, "count": 1, "language": "en", "format": "json"}
    )
    geo_resp.raise_for_status()
    geo_data = geo_resp.json()

    if "results" not in geo_data or len(geo_data["results"]) == 0:
        raise ValueError(f"Could not find coordinates for '{city_clean}'")

    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]

    # Step 2: get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_resp = requests.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
            "timezone": "auto"
        }
    )
    weather_resp.raise_for_status()
    weather_data = weather_resp.json()
    current_weather = weather_data.get("current_weather")

    return {
        "city": city_clean,
        "latitude": lat,
        "longitude": lon,
        "weather": current_weather
    }


# ----------------------------
# JSON-RPC Endpoint
# ----------------------------
@app.post("/jsonrpc")
async def jsonrpc(req: Request):
    body = await req.json()
    method = body.get("method")
    req_id = body.get("id")

    # List tools
    if method == "tools/list":
        tools = [
            {
                "id": "get_weather",
                "name": "Get current weather",
                "description": "Returns current weather for a city. Args: {city, units}",
                "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}}
            }
        ]
        return jsonrpc_result(req_id, tools)

    # Call a tool
    if method == "tools/call":
        params = body.get("params", {})
        tool = params.get("tool")
        args = params.get("args", {})

        if tool == "get_weather":
            city = args.get("city")
            units = args.get("units", "metric")
            if not city:
                return jsonrpc_error(req_id, -32602, "Missing 'city' argument")
            try:
                result = get_weather(city, units)
                return jsonrpc_result(req_id, {"tool": "get_weather", **result})
            except Exception as e:
                return jsonrpc_error(req_id, -32000, str(e))

        return jsonrpc_error(req_id, -32601, "Method not found")
