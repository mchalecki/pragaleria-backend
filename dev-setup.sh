sudo apt-get update && \
sudo apt-get install unzip && \
unzip -P "autorzy w kolejnosci brodologicznej" ./db/init.zip && \
mv ./init.sql ./db