#!/usr/bin/env bash
cd ~/docker-compose/streamlit/CFK2022
git pull origin master

python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_estudiantes.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/add_extrafiles.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_docentes.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_directivos.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_lider.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_plan.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_equipos.py
python3 ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/update_pivot.py

cd ~/mariana
./gdrive sync upload ~/docker-compose/streamlit/CFK2022/data/descargables/ 10-vecqL2rtGRXkZ4H6xkI4DY1Z5wr7fw
./gdrive sync upload ~/docker-compose/streamlit/CFK2022/utils/cleaners/bot/eliminados 1xaulGr1dAuJqx2AwtGRKCcRhm9jQZCUP

cd ~/docker-compose/streamlit/CFK2022
git add .
git commit -m "Actualización"
git push origin master
