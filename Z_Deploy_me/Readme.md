# Deploy Me!


## Quick - Use my DockerHub Image

* Visit and check the version you want to deploy: <https://hub.docker.com/repository/docker/fossengineer/double_pendulum/general>
* Execute: docker run -p 8501:8501 fossengineer/double_pendulum:your_desired_version
* Go to your browser: localhost:8501
## [Build](https://fossengineer.com/building-docker-container-images/) Me

* Get Docker installed
* Clone this repository
* Execute: docker build -t double_pendulum .
* And then: docker run -p 8501:8501 double_pendulum 
* Go to your browser: localhost:8501