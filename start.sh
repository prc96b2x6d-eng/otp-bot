#!/bin/bash
echo ">>> starting Flask..."
python3 main.py &

sleep 3
echo ">>> starting Telegram bot..."
python3 bot_interface.py