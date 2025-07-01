#!/usr/bin/env python3
"""
Secure WebRTC Video/Audio Calling Application
Main entry point
"""
import sys
import logging
import asyncio
from src.gui.main_window import MainWindow

def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('webrtc_app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main application entry point"""
    print("🔐 Secure WebRTC Calling Application")
    print("=====================================")
    print("Features:")
    print("• Post-quantum Kyber key exchange")
    print("• End-to-end encrypted video/audio calls")
    print("• Real-time peer-to-peer communication")
    print("• Modern GUI with call management")
    print()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create and run main application
        app = MainWindow()
        logger.info("Starting WebRTC calling application")
        app.run()
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    finally:
        logger.info("Application shutdown")

if __name__ == "__main__":
    main()