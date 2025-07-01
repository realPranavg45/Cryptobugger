# Secure WebRTC Video/Audio Calling Application

A production-ready Python application for secure peer-to-peer video and audio calling using WebRTC with post-quantum Kyber encryption.

## 🚀 Features

- **Real-time Communication**: High-quality video and audio calls
- **Post-Quantum Security**: Kyber key exchange resistant to quantum attacks
- **End-to-End Encryption**: AES-256 encryption of all media streams
- **Modern GUI**: Intuitive interface built with Tkinter
- **Peer-to-Peer**: Direct WebRTC connections between users
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam and microphone
- Network connectivity

### Install Dependencies

```bash
pip install -r requirements.txt
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-opencv libopencv-dev
sudo apt-get install portaudio19-dev python3-pyaudio
sudo apt-get install libavformat-dev libavcodec-dev libavdevice-dev
```

**macOS:**
```bash
brew install opencv portaudio ffmpeg
```

**Windows:**
- Install Visual Studio Build Tools
- Dependencies should install automatically with pip

## 🎯 Quick Start

### 1. Start the Signaling Server

In one terminal:
```bash
python server.py
```

### 2. Run the Application

In another terminal:
```bash
python main.py
```

### 3. Connect and Call

1. Enter a unique User ID
2. Click "Connect" to join the server
3. Select a user from the online list
4. Click "Video Call" or "Audio Call"
5. Accept/reject incoming calls

## 🏗️ Architecture

```
src/
├── crypto/
│   └── kyber.py              # Post-quantum key exchange
├── webrtc/
│   └── peer_connection.py    # WebRTC connection management
├── signaling/
│   ├── websocket_client.py   # Client-side signaling
│   └── websocket_server.py   # Server-side signaling
└── gui/
    ├── main_window.py        # Main application window
    ├── call_window.py        # Active call interface
    └── settings_window.py    # Configuration settings
```

## 🔐 Security Features

### Kyber Key Exchange
- Post-quantum cryptographic algorithm
- Resistant to both classical and quantum attacks
- Secure key establishment between peers

### AES-256 Encryption
- Industry-standard symmetric encryption
- Applied to all video and audio frames
- Real-time encryption/decryption

### Secure Signaling
- WebSocket-based signaling protocol
- Can be upgraded to WSS (WebSocket Secure)
- Minimal metadata exposure

## 🎮 Usage Guide

### Making Calls

1. **Connect to Server**: Enter your User ID and server URL
2. **Select Recipient**: Choose from the online users list
3. **Choose Call Type**: Video call includes camera, audio call is voice-only
4. **Wait for Response**: The recipient can accept or reject

### During Calls

- **Mute/Unmute**: Toggle microphone on/off
- **Video Toggle**: Enable/disable camera (video calls only)
- **End Call**: Terminate the connection
- **Local Preview**: See your own video feed

### Settings Configuration

Access via the Settings button:

- **Audio/Video**: Configure devices and quality
- **Network**: Set server URLs and STUN/TURN servers
- **Security**: Manage encryption settings and keys
- **General**: Behavior and notification preferences

## 🔧 Configuration

### Server Configuration

Edit `server.py` to change:
- Server host/port
- Connection limits
- Logging levels

### Client Configuration

Settings are stored in `settings.json`:
```json
{
  "video_device": 0,
  "audio_device": "default",
  "video_quality": "720p",
  "audio_quality": "high",
  "encryption_enabled": true,
  "server_url": "ws://localhost:8765"
}
```

## 🌐 Network Setup

### Local Network
- Default configuration works for same-network users
- Server runs on `localhost:8765`

### Internet Deployment
- Deploy signaling server to cloud (AWS, GCP, etc.)
- Configure STUN/TURN servers for NAT traversal
- Use WSS for secure signaling

### STUN/TURN Servers
```python
# Example STUN server configuration
stun_servers = [
    "stun:stun.l.google.com:19302",
    "stun:stun1.l.google.com:19302"
]
```

## 🐛 Troubleshooting

### Common Issues

**Camera/Microphone Not Working:**
- Check device permissions
- Verify device indices in settings
- Test with other applications

**Connection Failed:**
- Ensure signaling server is running
- Check firewall settings
- Verify network connectivity

**Poor Video Quality:**
- Adjust video quality in settings
- Check network bandwidth
- Close other applications using camera

**Audio Issues:**
- Check audio device selection
- Verify microphone permissions
- Test system audio settings

### Debug Mode

Enable detailed logging:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Deployment

### Production Deployment

1. **Signaling Server**: Deploy to cloud platform
2. **HTTPS/WSS**: Use SSL certificates
3. **STUN/TURN**: Configure for NAT traversal
4. **Monitoring**: Add health checks and metrics

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8765

CMD ["python", "server.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **aiortc**: WebRTC implementation for Python
- **Kyber**: Post-quantum cryptographic algorithm
- **OpenCV**: Computer vision library
- **Tkinter**: GUI framework

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the logs in `webrtc_app.log`

---

**Built with ❤️ for secure communications**