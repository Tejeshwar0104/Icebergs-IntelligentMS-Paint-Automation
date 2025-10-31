# Icebergs-IntelligentMS-Paint-Automation
🖌️ AI Paint Bot — Text-to-Image Drawing Automation using MS Paint
📘 Overview

This project demonstrates an AI-powered drawing agent that interprets user text commands and automatically draws corresponding scenes in Microsoft Paint using Python automation.

Example commands:

“Draw a house”

“Add a tree next to the house”

“Add sun”

“Clear canvas”

The system uses Flask for the backend, HTML/CSS/JS for the frontend, and PyAutoGUI to control MS Paint. It can understand sequential instructions to build a complete scene.

🧠 Features

🏠 Draws professional elements like house, tree, sun, person, and grass.

🧩 Maintains context — for example, a tree is placed next to the last drawn house.

⚡ Automates MS Paint actions (opening, focusing, and drawing).

🌐 Interactive web interface with responsive design.

🧠 Extensible architecture for integrating NLP or pretrained AI models in the future.

⚙️ Tech Stack
Component	Technology
Frontend	HTML5, CSS3, JavaScript
Backend	Python Flask
Automation	PyAutoGUI, PyGetWindow
Additional Tools	subprocess, logging
IDE	Visual Studio Code
🚀 How It Works

The user types a text command in the web UI.

The Flask backend receives the command and passes it to the drawing engine (draw_bot.py).

The script opens or focuses MS Paint, interprets the command, and executes drawing functions.

PyAutoGUI simulates mouse actions to draw shapes on the Paint canvas.

The result is shown in MS Paint in real-time.

🧩 Project Structure
AI-Paint-Bot/
│
├── app.py              # Flask backend for handling routes and commands
├── draw_bot.py         # Core automation logic and drawing functions
├── templates/
│   └── index.html      # Frontend user interface
└── Output.png          # Sample output image

🧭 Installation & Setup
Prerequisites

Windows OS (for MS Paint)

Python 3.8+

MS Paint pre-installed

Step 1: Clone Repository
git clone https://github.com/your-username/AI-Paint-Bot.git
cd AI-Paint-Bot

Step 2: Install Dependencies
pip install flask pyautogui pygetwindow

Step 3: Run the Application
python app.py

Step 4: Open in Browser

Visit: http://127.0.0.1:5000/

Then type a command like draw house or add tree.

🧱 Example Commands
Command	Action
draw house	Draws a modern house
add tree	Adds a tree near the house
add person	Draws a person in front
add sun	Adds the sun in the sky
draw scene	Creates a complete landscape
clear	Clears the canvas
🎯 Future Enhancements

Integrate voice input for voice-based drawing.

Add pretrained text-to-image model for intelligent sketching.

Implement undo/redo features.

Introduce 3D drawing support or export options.

📄 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Tejeshwar K
B.Tech – Artificial Intelligence and Data Science
B.S. Abdur Rahman Crescent Institute of Science and Technology
