FROM google/cloud-sdk:latest
RUN apt update && \
      apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl
ADD manage-startup-script.sh /
RUN chmod 755 /manage-startup-script.sh
CMD /manage-startup-script.sh
