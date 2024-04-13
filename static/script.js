let currentDiaryEntry = null;
let replayBtn = null;
let speakerWordsDiv = null;
let stopBtn = null;

document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('diaryForm'); // Make sure you have the correct ID for your form
	speakerWordsDiv = document.getElementById('speaker-words');
	replayBtn = document.getElementById('replay');

	form.addEventListener('submit', (event) => {
		event.preventDefault(); // Prevent the form from submitting traditionally
		fetchDiaryEntry();
	});

	replayBtn.addEventListener('click', async () => {
		if (currentDiaryEntry) {
			await playDiary(currentDiaryEntry);
		}
	});
});

const fetchDiaryEntry = async () => {
	try {
		replayBtn.disabled = true;
		const response = await fetch('/create-weekly_diary-entry/', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				year: document.getElementById('year').value,
				location: document.getElementById('location').value,
				gender: document.getElementById('gender').value,
				age: document.getElementById('age').value,
			}),
		});

		if (!response.ok) {
			alert('Error creating diary entry. Please try again.');
			throw new Error(`HTTP error, status = ${response.status}`);
		}

		const data = await response.json();
		currentDiaryEntry = data.result.diaryentry;
		playDiary();
	} catch (error) {
		console.error('Error fetching diary entry:', error.message);
	}
};

const playDiary = async () => {
	speakerWordsDiv.innerHTML = '';
	await speak(currentDiaryEntry.intro, 'intro');
	for (const paragraph of currentDiaryEntry.paragraphs) {
		await speak(paragraph.paragraph, 'paragraph');
		await playSong(paragraph.song_url, paragraph.song, paragraph.artist);
	}
	await speak(currentDiaryEntry.gratitude, 'gratitude');
	replayBtn.disabled = false;
};

const speak = (text, type) => {
	const speakerWordsDiv = document.getElementById('speaker-words');

	return new Promise((resolve) => {
		const utterance = new SpeechSynthesisUtterance(text);

		utterance.onstart = () => {
			speakerWordsDiv.innerHTML += `${text}<br><br>`;
			speakerWordsDiv.scrollTop = speakerWordsDiv.scrollHeight;
		};
		utterance.onend = resolve;
		window.speechSynthesis.speak(utterance);
	});
};

const playSong = (url, title, artist) => {
	const songTitlesDiv = document.getElementById('song-titles');
	return new Promise((resolve) => {
		if (!url) {
			resolve(); // If no URL is provided, resolve immediately.
			return;
		}
		songTitlesDiv.innerHTML += `<p>Now playing: ${title} by ${artist}.</p>`;

		const audio = new Audio(url);
		audio.onended = () => {
			songTitlesDiv.innerHTML = '';
			resolve();
		};
		audio.play();
	});
};
