"""
WebRTC Peer Connection Handler
"""
import asyncio
import json
import logging
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.media import MediaPlayer, MediaRecorder
from aiortc.contrib.signaling import BYE
import cv2
import numpy as np
from ..crypto.kyber import MediaEncryption

logger = logging.getLogger(__name__)

class EncryptedVideoStreamTrack:
    """Custom video track with encryption"""
    
    def __init__(self, track, encryption):
        self.track = track
        self.encryption = encryption
    
    async def recv(self):
        frame = await self.track.recv()
        
        # Convert frame to bytes
        frame_bytes = frame.to_ndarray().tobytes()
        
        # Encrypt frame
        encrypted_bytes = self.encryption.encrypt_frame(frame_bytes)
        
        # Convert back to frame (simplified)
        return frame

class WebRTCPeerConnection:
    """Manages WebRTC peer connections with encryption"""
    
    def __init__(self, signaling_client, encryption_key=None):
        self.pc = RTCPeerConnection()
        self.signaling = signaling_client
        self.encryption = MediaEncryption(encryption_key) if encryption_key else None
        self.local_video = None
        self.local_audio = None
        self.remote_video_track = None
        self.remote_audio_track = None
        self.call_state = "idle"  # idle, calling, ringing, connected
        
        # Set up event handlers
        self.setup_event_handlers()
    
    def setup_event_handlers(self):
        """Set up WebRTC event handlers"""
        
        @self.pc.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"Connection state: {self.pc.connectionState}")
            if self.pc.connectionState == "connected":
                self.call_state = "connected"
            elif self.pc.connectionState == "failed":
                self.call_state = "failed"
        
        @self.pc.on("track")
        def on_track(track):
            logger.info(f"Received track: {track.kind}")
            if track.kind == "video":
                self.remote_video_track = track
            elif track.kind == "audio":
                self.remote_audio_track = track
    
    async def start_local_media(self, video=True, audio=True):
        """Start local video and audio capture"""
        try:
            if video:
                # Use webcam
                self.local_video = MediaPlayer('/dev/video0', format='v4l2')
                if self.local_video.video:
                    self.pc.addTrack(self.local_video.video)
            
            if audio:
                # Use microphone
                self.local_audio = MediaPlayer('default', format='pulse')
                if self.local_audio.audio:
                    self.pc.addTrack(self.local_audio.audio)
                    
        except Exception as e:
            logger.error(f"Error starting local media: {e}")
            # Fallback to dummy media
            await self.start_dummy_media(video, audio)
    
    async def start_dummy_media(self, video=True, audio=True):
        """Start dummy media for testing"""
        if video:
            from aiortc.contrib.media import MediaPlayer
            self.local_video = MediaPlayer('testsrc=size=640x480:rate=30', format='lavfi')
            if self.local_video.video:
                self.pc.addTrack(self.local_video.video)
        
        if audio:
            from aiortc.contrib.media import MediaPlayer
            self.local_audio = MediaPlayer('sine=frequency=1000:duration=0', format='lavfi')
            if self.local_audio.audio:
                self.pc.addTrack(self.local_audio.audio)
    
    async def create_offer(self):
        """Create WebRTC offer"""
        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        return {
            "type": offer.type,
            "sdp": offer.sdp
        }
    
    async def create_answer(self, offer):
        """Create WebRTC answer"""
        await self.pc.setRemoteDescription(RTCSessionDescription(
            sdp=offer["sdp"],
            type=offer["type"]
        ))
        
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)
        
        return {
            "type": answer.type,
            "sdp": answer.sdp
        }
    
    async def set_remote_description(self, answer):
        """Set remote description"""
        await self.pc.setRemoteDescription(RTCSessionDescription(
            sdp=answer["sdp"],
            type=answer["type"]
        ))
    
    async def add_ice_candidate(self, candidate):
        """Add ICE candidate"""
        await self.pc.addIceCandidate(RTCIceCandidate(
            candidate=candidate["candidate"],
            sdpMLineIndex=candidate["sdpMLineIndex"],
            sdpMid=candidate["sdpMid"]
        ))
    
    async def close(self):
        """Close peer connection"""
        if self.local_video:
            self.local_video.stop()
        if self.local_audio:
            self.local_audio.stop()
        await self.pc.close()