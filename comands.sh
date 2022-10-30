#!/bin/bash
dir=$(ls bot/db/migrations/versions)
if [ -z "$dir" ]
then
empty=true
else
empty false
fi

if [ $empty ]
then
echo $(alembic revision --autogenerate -m "Innit" && alembic upgrade head && cd bot && ls && python server.py)