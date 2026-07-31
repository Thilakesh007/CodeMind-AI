"""Eye-tracking (EAR) placeholder — mirrors ai/mediapipe/face_mesh.py.

The eye-aspect-ratio (EAR) calculation in the original app runs client-side
in JavaScript (frontend/static/js/camera.js, function onResults). The
resulting `ear` value is POSTed to /metrics, where the server applies the
threshold check in ai/calculations/attention.is_attentive().

No server-side eye-tracking code existed in app.py to move; this module is a
structural placeholder only.
"""
