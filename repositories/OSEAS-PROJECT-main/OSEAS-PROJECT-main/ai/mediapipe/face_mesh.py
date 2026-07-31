"""MediaPipe FaceMesh integration point.

NOTE ON SCOPE: in the original app.py, MediaPipe FaceMesh runs entirely in
the browser (JavaScript, loaded from the MediaPipe CDN) — there was no
server-side Python MediaPipe code to move. The real landmark-detection and
EAR/MAR/head-turn math lives in:
    frontend/static/js/camera.js   (FaceMesh setup + onResults callback)

This module is a placeholder for a future server-side MediaPipe pipeline
(e.g. if frame images are ever POSTed to the backend for processing instead
of computed client-side) so the target architecture has a home for it
without inventing new server-side behavior that the original app didn't have.
"""


def landmarks_supported_server_side() -> bool:
    """Indicates server-side MediaPipe processing is not implemented.

    Landmark extraction currently happens client-side; see camera.js.
    """
    return False
