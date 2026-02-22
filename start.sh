#!/bin/bash
echo ">>> starting Telegram bot..."
python3 bot_interface.py & 
echo ">>> starting Flask..."
python3 main.py