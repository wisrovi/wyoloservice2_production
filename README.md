# wyoloservice2_production

This project contains the following components:

- **workers**: Service for executing tasks.
- **control_server**: Central management server for datasets and model configurations.

## Setup

Refer to the individual directories for specific setup instructions.


# ports

23432 -> front (react)
23433 -> ui_invoker
23434 -> ui_manager
23435 -> Mlflow
23436 -> postgress
23437 -> redis
23438 -> redis-commander
23439 -> minIO_back
23440 -> minIO_front
23441 -> Flower
23442 -> api for front (react)
23443 -> optuna dashboard
23444 -> gradio for api

23448 -> FTP browser
23449 -> samba dataset



## punto de montaje que usa los executor que levanta el invoker

sudo mount -t cifs //192.168.10.252/datasets /mnt/nas_dataset/ -o username=wisrovi,password=wyoloservice,port=23449,file_mode=0777,dir_mode=0777,iocharset=utf8

otra forma seria montarlo en local y compartir los datos al contenedor

volumes:
      - /mnt/nas_dataset:/wyolo/control_server/datasets
