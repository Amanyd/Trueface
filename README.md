# 🤖 Face Recognition Based Servo Control System

A real-time face recognition system with Arduino integration, designed to control a servo motor when a registered face is detected.

## 🚀 Features

- Real-time face detection and recognition
- Simple GUI for face registration and recognition
- Arduino integration for hardware control
- Cross-platform compatibility

## 🛠️ Prerequisites

### For Linux:
```bash
# System dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-dev python3-pip
sudo apt-get install -y build-essential cmake
sudo apt-get install -y libx11-dev libatlas-base-dev libgtk-3-dev
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
```

### For Windows:
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd face_robot_project
   ```

2. **Set up virtual environment**
   ```bash
   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install numpy==2.0.0 opencv-python==4.8.0.76 face_recognition==1.3.0 pillow==10.0.0 pyserial
   ```

4. **Run the application**
   ```bash
   python gui_main.py
   ```

## 🖥️ Usage

1. **Register Faces**
   - Click "Register Face"
   - Enter a name when prompted
   - Position your face in the camera view
   - Press 's' to capture multiple angles
   - Press 'q' when done

2. **Start Recognition**
   - Click "Start Recognition"
   - The system will identify registered faces
   - Recognized faces will be displayed with their names

3. **Arduino Integration**
   - Connect Arduino to the computer
   - Upload the provided Arduino sketch
   - The system will automatically detect and use the Arduino

## 🔌 Hardware Setup

### Components:
- Arduino Uno
- Servo Motor (SG90)
- Jumper wires

### Connections:
| Servo Wire | Arduino Pin |
|------------|-------------|
| Orange (Signal) | D9         |
| Red (VCC)      | 5V          |
| Brown (GND)    | GND         |

## 📁 Project Structure

```
face_robot_project/
├── gui_main.py          # Main application GUI
├── recognizer.py        # Face recognition logic
├── register.py          # Face registration script
├── models/              # Pre-trained models
├── images/              # Captured face images
├── encodings.pkl        # Face encodings database
└── README.md            # This file
```

## 🔧 Troubleshooting

### Common Issues:
1. **Qt/Wayland Warning**
   ```bash
   export QT_QPA_PLATFORM=xcb
   python gui_main.py
   ```

2. **Missing Dependencies**
   Ensure all system dependencies are installed (see Prerequisites)

3. **Arduino Not Detected**
   - Check USB connection
   - Verify correct port in code (usually `/dev/ttyUSB0` or `COM3`)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV and dlib teams for the computer vision libraries
- Python community for the amazing ecosystem
