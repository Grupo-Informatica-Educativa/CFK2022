#!/usr/bin/env bash
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_xlsx.py
cd ~/docker-compose/streamlit/CFK2022
git add .
git commit -m "Actualización"
git push origin master
