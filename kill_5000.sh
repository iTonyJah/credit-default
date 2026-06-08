#!/bin/bash
echo "Killing process on port 5000..."
fuser -k 5000/tcp 2>/dev/null || true
sleep 1
echo "Port 5000 is free"
