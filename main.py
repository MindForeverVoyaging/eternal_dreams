"""
This module provides an API for generating weekly diary entries 
given parameters like location, year, age and gender. It uses 
the Groq AI assistant to generate the diary text and includes
functions for searching Spotify to add music tracks.
"""

import base64
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
from pydantic import BaseModel

# from openai import OpenAI
from groq import Groq

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Optionally, directly add a route for the favicon
@app.get("/favicon.ico")
async def favicon():
    """
    Serves the favicon.
    """
    return FileResponse("static/img/favicon.ico")


# client = OpenAI()
# model = "gpt-3.5-turbo"

CLIENT = Groq()
MODEL = "mixtral-8x7b-32768"


class DiaryEntryRequest(BaseModel):
    """
    Pydantic model for request parameters like location,
    year, age and gender.
    """

    location: str
    year: int
    gender: str
    age: int


class SpotifyAccessTokenError(Exception):
    """Custom exception for Spotify access token retrieval errors."""


class SpotifySearchError(Exception):
    """Custom exception for Spotify search-related errors."""


def spotify_get_access_token():
    """
    Get Spotify access token.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    try:
        response = httpx.post(
            "https://accounts.spotify.com/api/token", headers=headers, data=data
        )
        response.raise_for_status()  # Raises an httpx.HTTPStatusError for 4xx/5xx responses
        return response.json()["access_token"]
    except httpx.HTTPStatusError as e:
        raise SpotifyAccessTokenError(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        ) from e
    except httpx.RequestError as e:
        raise SpotifyAccessTokenError(f"Request error occurred: {e}") from e
    except httpx.HTTPError as e:
        raise SpotifyAccessTokenError(f"HTTP error occurred: {e}") from e


def spotify_get_songs_preview_url(search_criteria, access_token):
    """
    Retrieves the Spotify preview URL of tracks based on the search criteria.
    """
    auth_header = {"Authorization": f"Bearer {access_token}"}
    search_url = "https://api.spotify.com/v1/search"
    params = {"q": search_criteria, "type": "track", "limit": 5}
    try:
        response = httpx.get(search_url, headers=auth_header, params=params)
        response.raise_for_status()  # Raises an httpx.HTTPStatusError for 4xx/5xx responses

        search_results = response.json()
        tracks = search_results["tracks"]["items"]
        preview_url = None
        if tracks:
            for track in tracks:
                if track["preview_url"]:
                    # Return the first preview URL found
                    preview_url = track["preview_url"]
                    break
        return preview_url
    except httpx.HTTPStatusError as e:
        raise SpotifySearchError(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        ) from e
    except httpx.RequestError as e:
        raise SpotifySearchError(f"Request error occurred: {e}") from e
    except httpx.HTTPError as e:
        raise SpotifySearchError(f"HTTP error occurred: {e}") from e


def add_song_tracks(data):
    """
    Add Spotify track URLs to diary entry paragraphs
    """
    access_token = spotify_get_access_token()

    # get urls from paragraphs
    for index, paragraph in enumerate(data["diaryentry"]["paragraphs"]):
        print(f"""Search for: {paragraph['song']} by {paragraph['artist']} """)
        search_criteria = (
            f"""artist={paragraph['artist']} AND name={paragraph['song']}"""
        )
        song_url = spotify_get_songs_preview_url(search_criteria, access_token)
        data["diaryentry"]["paragraphs"][index]["song_url"] = song_url

    return data


@app.post("/create-weekly_diary-entry/")
async def create_diary_entry_api(diary_entry_request: DiaryEntryRequest):
    """
    API endpoint for creating a weekly diary entry.
    """
    messages = [
        {
            "role": "system",
            "content": """Your role is that given an age, a gender, a location
                       and a year, to produce a weekly diary entry, for an
                       individual, based on the age, location and year
                       properties provided. The Individual should reflect on the
                       past week, discussing the current events at the provided
                       location and provided year and their own concerns.  Begin
                       with the individual introducing themselves, mentioning
                       the year, where they live, and their occupation. The
                       introduction should be followed by a continued story of
                       300 words in three paragraphs. In each paragraph, the
                       individual should mention a song and its artist popular
                       in the year provided and that matches the paragraph"s
                       vibe. Conclude by adding a section to express the
                       individuals gratitude for the opportunity to share the
                       week"s experiences.  The choice of songs should follow
                       there rules [ 1. song must match the vibe of the
                       paragraph.  2. songs release date must be in or before
                       the provided year.  3. at least two of the songs should
                       be in the language of the location provided.  ] Write the
                       response in json in the following format.  {
                       "diaryentry": { "intro": "introduction", "paragraphs": [
                       { "paragraph": "paragraph", "song": "song", "artist":
                       "artist",  "release date": "Release Date" } ],
                       "gratitude": "gratitude" } } Before writing, check your
                       work and ensure that you have properly followed the
                       instructions, particularly that the diary entry should
                       match the culture and be consistent with the location,
                       the year, the individual"s age and their gender. """
            + f"""The json format is very important. Take a deep breath and
               carefully consider the request before creating the json.
               Location:{diary_entry_request.location}
               Year:{diary_entry_request.year}
               Gender:{diary_entry_request.gender}
               Age:{diary_entry_request.age}""",
        },
    ]

    try:

        response = CLIENT.chat.completions.create(
            messages=messages,
            model=MODEL,
        )

        diary_entry_script = json.loads(response.choices[0].message.content)
        diary_with_song_tracks = add_song_tracks(diary_entry_script)
        return {"result": diary_with_song_tracks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI call failed: {e}") from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
