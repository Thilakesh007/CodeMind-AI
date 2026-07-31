"""High-level engagement detection placeholder.

In the original app.py, "detection" is really: client-side FaceMesh (JS)
produces ear/mar/head values -> POST /metrics -> server-side threshold
checks (ai/calculations/attention.py) + score aggregation
(backend/services/engagement_service.py, attention_service.py). There is no
separate server-side detector object; this module exists only to match the
target architecture's folder layout and to document where such a component
would live if detection moved server-side in the future.
"""
