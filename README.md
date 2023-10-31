# Essence Extractor 📜✨

Essence Extractor is a dynamic tool designed to transform YouTube videos into engaging and concise blog posts. 🎥➡️📄 This utility automates the process of downloading videos, extracting audio, transcribing speech, and generating a summary to create a ready-to-publish blog post. 

## Requirements 🛠️
In addition to the dependencies listed in `pyproject.toml`, this project requires:
- [FFmpeg](https://ffmpeg.org/download.html): A complete, cross-platform solution to record, convert, and stream audio and video.
- [Poetry](https://python-poetry.org/docs/#installation): A tool for dependency management and packaging in Python.

## Installation 🖥️

Follow these steps to set up Essence Extractor on your local machine:

1. **Clone the Repository:** 
   ```bash
   git clone https://github.com/Jurik-001/EssenceExtractor.git
   cd EssenceExtractor
   ```

2. **Create and Activate a Virtual Environment:** 
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:** 
   ```bash
   poetry install
   ```

## Usage 🚀

To unleash the power of Essence Extractor, you'll need an API key from OpenAI. Sign up on OpenAI's platform to get yours.

Once you have your API key, run:
```bash
python main.py "output_directory" "YOUR_API_KEY"
```
- **output_directory**: Where the magic happens - all your output files will land here.
- **YOUR_API_KEY**: Your secret key to OpenAI's capabilities.

Next, you'll be prompted to enter the YouTube video URL:
```bash
Please enter the YouTube video URL: "https://www.youtube.com/watch?v=yourvideoid"
```

## What’s in the Box? 🎁

Running Essence Extractor will populate your output directory with:
- **Video File**: The original YouTube video, downloaded for reference.
- **Audio File**: The extracted audio from the video.
- **Transcription File**: A text file with everything that was said in the video.
- **Blog Post File**: Your brand new blog post, ready for the world to see.

## Join the Essence Extractor Community 🤝

Got ideas or found a bug? We’d love to have you in our contributor community! 🚀 Check out our [contributing guidelines](.github/CONTRIBUTING.md) to get started.

## Roadmap 🗺️

Wondering what's coming next for Essence Extractor? Check out our [project roadmap](https://github.com/users/Jurik-001/projects/1) to stay up to date with the latest features and improvements. We're constantly working to make Essence Extractor better, and we value your input! Feel free to share your suggestions and feedback to help shape the future of this project.