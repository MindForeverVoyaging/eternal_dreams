# Eternal Dreams Radio

Eternal Dreams Radio is a web application that allows users to experience weekly audio diary entries from different eras, complete with music and ambiance from that time. It uses AI language models to generate narratives based on the provided year, location, gender, and age, bringing to life the stories and voices of the past.

## Features

-   Generate weekly audio diary entries from different years, locations, and demographics.
-   Seamlessly integrate music from the specified era into the audio experience.

## Technologies Used

-   HTML, CSS, and JavaScript for the front-end
-   FastAPI for the back-end server
-   Groq with Mistral for the language model integration
-   Spotify API for music integration

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your-username/eternal-dreams-radio.git
```

2. Install the required dependencies (assuming you have Python and pip installed).

3. Set up the necessary environment variables for the Spotify API credentials.

4. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

5. Open the application in your web browser at `http://localhost:8000`.

## Usage

1. Fill in the form fields with the desired year, location, gender, and age.
2. Click the "Get Diary Entry" button to generate a new audio diary entry.
3. Listen to the audio diary as it plays, accompanied by music from the specified era.
4. Use the "Replay" button to replay the audio diary entry.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

-   [OpenAI](https://openai.com/) for their language models
-   [Anthropic](https://www.anthropic.com/) for their language models
-   [Spotify](https://developer.spotify.com/) for their music API

## Obtaining Spotify Developer Credentials and Groq Key

To use the Spotify API for music integration and the Groq language model, you'll need to obtain the necessary credentials and API keys. Follow these steps:

1. **Spotify Developer Credentials**:

    - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account credentials. If you don't have a Spotify account, you'll need to create one first.
    - Once logged in, click on the "Create an App" button to create a new Spotify application.
    - Fill in the required information, such as the app name, description, and accept the terms and conditions.
    - After creating the app, you'll be redirected to the app dashboard. Here, you'll find your **Client ID** and **Client Secret**.

2. **Groq Key**:

    - Sign up for a Groq account at [https://www.groq.ai/](https://www.groq.ai/) and obtain your API key.

3. In your project's root directory, create a new file named `.env` (if it doesn't already exist) and add the following lines, replacing `YOUR_CLIENT_ID`, `YOUR_CLIENT_SECRET`, and `YOUR_GROQ_KEY` with the values from the respective platforms:

```
SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET
GROQ_KEY=YOUR_GROQ_KEY
```

4. Make sure to add the `.env` file to your `.gitignore` file to prevent your credentials from being committed to your version control system.

With your Spotify Developer credentials and Groq key set up, you should now be able to use the Spotify API for music integration and the Groq language model within your Eternal Dreams Radio application.

Note: Be sure to keep your Spotify Client ID, Client Secret, and Groq key confidential and never share them publicly or include them in your source code.
