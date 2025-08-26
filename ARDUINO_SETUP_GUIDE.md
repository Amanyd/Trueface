# TrueFace Arduino Integration Guide

## 🔧 Hardware Setup

### Components Required:
- Arduino Uno
- Servo Motor (SG90 recommended)
- 3 Jumper wires
- USB cable for Arduino

### Wiring Connections:
```
Arduino Uno    →    Servo Motor
5V             →    Red wire (VCC)
GND            →    Brown/Black wire (GND)
Pin 9          →    Orange/Yellow wire (Signal)
```

## 💻 Software Setup

### Step 1: Upload Arduino Code
1. Open Arduino IDE
2. Open the file: `arduino_servo_control.ino`
3. Connect Arduino Uno via USB
4. Select correct board: **Tools → Board → Arduino Uno**
5. Select correct port: **Tools → Port → COM[X]** (note the COM port number)
6. Click **Upload** button

### Step 2: Find COM Port
1. Open **Device Manager** (Windows + X → Device Manager)
2. Expand **Ports (COM & LPT)**
3. Look for **Arduino Uno (COM[X])** - note the number
4. If not visible, try different USB port or reinstall Arduino drivers

### Step 3: Update Python Code COM Port
1. Open `gui_main.py`
2. Find line: `arduino = serial.Serial('COM4', 9600, timeout=1)`
3. Change `'COM4'` to your actual COM port (e.g., `'COM3'`, `'COM5'`)

## 🧪 Testing

### Test Arduino Separately:
1. Open Arduino IDE Serial Monitor (Tools → Serial Monitor)
2. Set baud rate to **9600**
3. Type `1` and press Enter → Servo should move to 90°
4. Type `0` and press Enter → Servo should return to 0°

### Test with TrueFace:
1. Ensure Arduino is connected and code uploaded
2. Run TrueFace application
3. Register your face
4. Start recognition
5. When your face is detected → Servo should move
6. When unknown face/no face → Servo returns to rest

## 🔧 Troubleshooting

### Arduino Not Detected:
- Check USB cable connection
- Try different USB port
- Reinstall Arduino drivers
- Check Device Manager for COM port

### Servo Not Moving:
- Verify wiring connections
- Check power supply (5V)
- Test servo with simple Arduino sketch
- Ensure correct COM port in Python code

### Python Connection Error:
- Update COM port number in `gui_main.py`
- Close Arduino Serial Monitor before running Python
- Check if another program is using the COM port

## 🎯 How It Works

1. **Face Recognition** → Python detects known/unknown faces
2. **Serial Communication** → Python sends `'1'` or `'0'` to Arduino
3. **Servo Control** → Arduino moves servo based on command:
   - `'1'` = Face recognized → Move to 90°
   - `'0'` = Unknown face → Return to 0°
4. **LED Indicator** → Built-in LED shows status

## 🚀 Next Steps

- Customize servo positions in Arduino code
- Add more servos for complex movements
- Integrate buzzer for audio feedback
- Add LCD display for status messages
