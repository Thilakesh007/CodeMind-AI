"""Head-pose (head-turn) placeholder — mirrors ai/mediapipe/face_mesh.py.

The head-turn ratio is computed client-side in camera.js and POSTed to
/metrics as `head`. See ai/calculations/attention.is_attentive() for the
server-side threshold check. No server-side head-pose code existed in the
original app.py; this module is a structural placeholder only.
"""
