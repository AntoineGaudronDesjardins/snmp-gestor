FROM ubuntu:22.10

# Install the snmp agent
RUN apt-get update && \
    apt-get install -y snmpd snmp-mibs-downloader openssh-server rsyslog sudo vim net-tools
RUN rm /usr/share/snmp/mibs/ietf/SNMPv2-PDU

# Load configuration files and custom scripts
COPY ./conf/*.conf /etc/snmp/
COPY ./scripts/ /usr/local/bin/
RUN chmod -R a+x /usr/local/bin/

# Create user to test ssh session
RUN useradd -ms /bin/bash bob
RUN echo 'bob:bobpassword' | chpasswd
RUN usermod -aG sudo bob
RUN mkdir -p /home/bob/.ssh/
COPY id_ed25519.pub /home/bob/.ssh/authorized_keys
RUN chown -R bob:bob /home/bob/.ssh && \
    chmod 0700 /home/bob/.ssh && \
    chmod 0600 /home/bob/.ssh/authorized_keys

EXPOSE 161-162/udp
EXPOSE 22

COPY boot.sh /bin/boot.sh
RUN chmod a+x /bin/boot.sh
CMD ["/bin/boot.sh"]