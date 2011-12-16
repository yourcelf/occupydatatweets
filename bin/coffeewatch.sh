while true ; do sleep 1 ; inotifywait static/js/*.coffee ; coffee -c static/js/ ; done
