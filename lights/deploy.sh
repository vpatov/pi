scp -r ./* vas@pi99:/home/vas/proj/lights
ssh -t vas@pi99 "sudo systemctl restart lights"
