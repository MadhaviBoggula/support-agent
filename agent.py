
import os
import sys
import asyncio
from typing import List, Dict

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


# ============================================================
# CREATE MCP SERVER
# ============================================================

mcp = FastMCP("Travel Agent")


# ============================================================
# 1. FLIGHT SEARCH
# ============================================================

@mcp.tool()
def search_flights(
    source: str,
    destination: str,
    travel_date: str,
    passengers: int = 1
) -> List[Dict]:
    """
    Search available flights between source and destination.
    """

    return [
        {
            "airline": "IndiGo",
            "flight_number": "6E-123",
            "source": source,
            "destination": destination,
            "date": travel_date,
            "departure": "08:00 AM",
            "arrival": "09:30 AM",
            "duration": "1h 30m",
            "price": 4500,
            "available_seats": 12,
            "passengers": passengers
        },
        {
            "airline": "Air India",
            "flight_number": "AI-456",
            "source": source,
            "destination": destination,
            "date": travel_date,
            "departure": "11:00 AM",
            "arrival": "12:40 PM",
            "duration": "1h 40m",
            "price": 5200,
            "available_seats": 8,
            "passengers": passengers
        },
        {
            "airline": "Akasa Air",
            "flight_number": "QP-789",
            "source": source,
            "destination": destination,
            "date": travel_date,
            "departure": "03:00 PM",
            "arrival": "04:30 PM",
            "duration": "1h 30m",
            "price": 4800,
            "available_seats": 15,
            "passengers": passengers
        }
    ]

m
# ============================================================
# 2. HOTEL SEARCH
# ============================================================

@mcp.tool()
def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    guests: int = 1
) -> List[Dict]:
    """
    Search available hotels.
    """

    return [
        {
            "name": "Beach View Hotel",
            "location": destination,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "rating": 4.5,
            "price_per_night": 3000,
            "room_type": "Deluxe Room",
            "amenities": [
                "WiFi",
                "Swimming Pool",
                "Breakfast",
                "Parking"
            ]
        },
        {
            "name": "City Center Hotel",
            "location": destination,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "rating": 4.2,
            "price_per_night": 2500,
            "room_type": "Standard Room",
            "amenities": [
                "WiFi",
                "Breakfast",
                "Restaurant"
            ]
        },
        {
            "name": "Budget Stay",
            "location": destination,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "rating": 4.0,
            "price_per_night": 1800,
            "room_type": "Standard Room",
            "amenities": [
                "WiFi",
                "Parking"
            ]
        }
    ]


# ============================================================
# 3. WEATHER
# ============================================================

@mcp.tool()
def get_weather(destination: str) -> Dict:
    """
    Get weather information.
    """

    return {
        "destination": destination,
        "temperature": "28°C",
        "condition": "Sunny",
        "humidity": "65%",
        "wind_speed": "15 km/h",
        "rain_probability": "10%",
        "recommendation": (
            "Weather is suitable for sightseeing "
            "and outdoor activities."
        )
    }


# ============================================================
# 4. TOURIST ATTRACTIONS
# ============================================================

@mcp.tool()
def search_attractions(destination: str) -> List[Dict]:
    """
    Find popular tourist attractions.
    """

    return [
        {
            "name": "Beach",
            "type": "Nature",
            "best_time": "Morning and Evening",
            "recommended_duration": "2-3 hours"
        },
        {
            "name": "Historic Fort",
            "type": "Historical",
            "best_time": "Morning",
            "recommended_duration": "2 hours"
        },
        {
            "name": "City Museum",
            "type": "Museum",
            "best_time": "Afternoon",
            "recommended_duration": "1-2 hours"
        },
        {
            "name": "Local Market",
            "type": "Shopping",
            "best_time": "Evening",
            "recommended_duration": "2 hours"
        },
        {
            "name": "Famous Temple",
            "type": "Religious",
            "best_time": "Morning",
            "recommended_duration": "1-2 hours"
        }
    ]


# ============================================================
# 5. LOCAL TRANSPORTATION
# ============================================================

@mcp.tool()
def search_transportation(destination: str) -> List[Dict]:
    """
    Find local transportation.
    """

    return [
        {
            "type": "Taxi",
            "estimated_cost": "₹300 - ₹800",
            "availability": "Available"
        },
        {
            "type": "Auto Rickshaw",
            "estimated_cost": "₹100 - ₹300",
            "availability": "Available"
        },
        {
            "type": "Rental Bike",
            "estimated_cost": "₹400 - ₹700 per day",
            "availability": "Available"
        },
        {
            "type": "Rental Car",
            "estimated_cost": "₹1500 - ₹2500 per day",
            "availability": "Available"
        },
        {
            "type": "Public Bus",
            "estimated_cost": "₹20 - ₹100",
            "availability": "Available"
        }
    ]


# ============================================================
# 6. RESTAURANTS
# ============================================================

@mcp.tool()
def search_restaurants(
    destination: str,
    cuisine: str = "Any"
) -> List[Dict]:
    """
    Find restaurants.
    """

    restaurants = [
        {
            "name": "Local Spice Restaurant",
            "cuisine": "Indian",
            "rating": 4.5,
            "average_cost": "₹500 for two",
            "location": destination
        },
        {
            "name": "Sea View Restaurant",
            "cuisine": "Seafood",
            "rating": 4.4,
            "average_cost": "₹800 for two",
            "location": destination
        },
        {
            "name": "Family Restaurant",
            "cuisine": "Multi-cuisine",
            "rating": 4.2,
            "average_cost": "₹600 for two",
            "location": destination
        }
    ]

    if cuisine.lower() != "any":

        filtered = [
            restaurant
            for restaurant in restaurants
            if cuisine.lower()
            in restaurant["cuisine"].lower()
        ]

        if filtered:
            return filtered

    return restaurants


# ============================================================
# 7. CURRENCY CONVERSION
# ============================================================

@mcp.tool()
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> Dict:
    """
    Convert currency.
    """

    rates = {
        "USD_INR": 84.0,
        "EUR_INR": 91.0,
        "GBP_INR": 108.0,
        "INR_USD": 0.0119,
        "INR_EUR": 0.0110,
        "INR_GBP": 0.0093
    }

    key = (
        f"{from_currency.upper()}_"
        f"{to_currency.upper()}"
    )

    if from_currency.upper() == to_currency.upper():

        converted_amount = amount

    elif key in rates:

        converted_amount = amount * rates[key]

    else:

        return {
            "error": "Currency conversion rate not available",
            "from": from_currency,
            "to": to_currency
        }

    return {
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "amount": amount,
        "converted_amount": round(converted_amount, 2)
    }


# ============================================================
# 8. TRAVEL DISTANCE
# ============================================================

@mcp.tool()
def calculate_travel_distance(
    source: str,
    destination: str,
    transport_mode: str = "car"
) -> Dict:
    """
    Get approximate travel distance and time.
    """

    return {
        "source": source,
        "destination": destination,
        "transport_mode": transport_mode,
        "distance": "650 km",
        "estimated_travel_time": "10 hours",
        "note": "Distance and time are approximate."
    }


# ============================================================
# 9. GENERAL TRAVEL INFORMATION
# ============================================================

@mcp.tool()
def get_travel_information(
    source: str,
    destination: str
) -> Dict:
    """
    Provide general travel information.
    """

    return {
        "source": source,
        "destination": destination,
        "recommended_transport": [
            "Flight",
            "Train",
            "Bus"
        ],
        "travel_tips": [
            "Carry a valid government ID.",
            "Keep hotel booking details available.",
            "Check weather before travelling.",
            "Keep emergency contact information.",
            "Carry required medicines and personal items."
        ],
        "important_documents": [
            "Government ID",
            "Travel ticket",
            "Hotel reservation"
        ]
    }


# ============================================================
# 10. DAILY TRAVEL PLAN
# ============================================================

@mcp.tool()
def create_daily_plan(
    destination: str,
    number_of_days: int
) -> List[Dict]:
    """
    Create a basic daily sightseeing plan.
    """

    places = [
        "Beach",
        "Historic Fort",
        "City Museum",
        "Local Market",
        "Famous Temple"
    ]

    itinerary = []

    for day in range(1, number_of_days + 1):

        place1 = places[(day - 1) % len(places)]
        place2 = places[day % len(places)]

        itinerary.append(
            {
                "day": day,
                "destination": destination,
                "morning": place1,
                "afternoon": place2,
                "evening": "Local Market / Restaurant"
            }
        )

    return itinerary


# ============================================================
# 11. TRIP BUDGET
# ============================================================

@mcp.tool()
def estimate_trip_budget(
    number_of_days: int,
    hotel_price_per_night: float,
    flight_price: float,
    daily_food_budget: float,
    daily_transport_budget: float
) -> Dict:
    """
    Estimate trip budget.
    """

    hotel_cost = (
        hotel_price_per_night
        * number_of_days
    )

    food_cost = (
        daily_food_budget
        * number_of_days
    )

    transport_cost = (
        daily_transport_budget
        * number_of_days
    )

    total = (
        flight_price
        + hotel_cost
        + food_cost
        + transport_cost
    )

    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "food_cost": food_cost,
        "transport_cost": transport_cost,
        "estimated_total": total
    }


# ============================================================
# MCP SERVER MODE
# ============================================================

def run_mcp_server():
    """
    Start the same Python file as an MCP server.
    """

    mcp.run(transport="stdio")


# ============================================================
# GROQ + MCP CLIENT
# ============================================================

async def run_travel_agent():

    from langchain_groq import ChatGroq
    from langchain_mcp_adapters.client import (
        MultiServerMCPClient
    )
    from langchain.agents import create_agent

    # --------------------------------------------------------
    # CREATE GROQ LLM
    # --------------------------------------------------------

    model = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=GROQ_API_KEY,
        temperature=0.2
    )

    # --------------------------------------------------------
    # CREATE MCP CLIENT
    # --------------------------------------------------------

    client = MultiServerMCPClient(
        {
            "travel": {
                "command": sys.executable,
                "args": [
                    os.path.abspath(__file__),
                    "--server"
                ],
                "transport": "stdio"
            }
        }
    )

    # --------------------------------------------------------
    # LOAD MCP TOOLS
    # --------------------------------------------------------

    tools = await client.get_tools()

    print("\n==============================================")
    print("          GROQ MCP TRAVEL AGENT")
    print("==============================================")

    print("\nMCP server connected successfully.")

    print("\nAvailable MCP tools:")

    for tool in tools:
        print(f" - {tool.name}")

    # --------------------------------------------------------
    # CREATE AGENT
    # --------------------------------------------------------

    agent = create_agent(
        model=model,
        tools=tools
    )

    # --------------------------------------------------------
    # USER INPUT
    # --------------------------------------------------------

    print("\n==============================================")
    print("Enter your travel requirement")
    print("Example:")
    print(
        "I want to travel from Vijayawada to Goa "
        "for 3 days. Find flights, hotels, weather "
        "and create a travel plan."
    )
    print("==============================================")

    user_request = input("\nYou: ")

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an AI Travel Agent.

Help the user create a useful travel plan.

User request:
{user_request}

You have access to MCP travel tools.

Use the appropriate MCP tools whenever necessary.

Available capabilities:

- flight search
- hotel search
- weather
- tourist attractions
- transportation
- restaurants
- currency conversion
- distance calculation
- travel information
- daily itinerary
- budget estimation

Do not invent tool results.

Use the MCP tools to obtain information.

Then prepare a clear travel plan.

Include:

1. Travel summary
2. Flight information
3. Hotel information
4. Weather
5. Attractions
6. Transportation
7. Restaurants if useful
8. Daily itinerary
9. Estimated budget if enough information is available
10. Important travel tips

Remember:
The information returned by the MCP tools is sample
data for this demonstration project.
"""

    # --------------------------------------------------------
    # CALL GROQ AGENT
    # --------------------------------------------------------

    print("\nTravel Agent is preparing your plan...\n")

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    # --------------------------------------------------------
    # DISPLAY FINAL RESPONSE
    # --------------------------------------------------------

    messages = response.get("messages", [])

    for message in reversed(messages):

        if getattr(message, "type", None) == "ai":

            print("\n==============================================")
            print("              TRAVEL PLAN")
            print("==============================================\n")

            print(message.content)

            break


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    if "--server" in sys.argv:

        run_mcp_server()

    else:

        asyncio.run(run_travel_agent())