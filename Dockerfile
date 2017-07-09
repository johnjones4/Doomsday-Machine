FROM ubuntu:14.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN mkdir /var/cloudbackups
RUN mkdir /var/cloudbackups/workdir
RUN mkdir /var/cloudbackups/archives
ADD backup.sh /usr/bin/backup.sh
ADD startup.sh /usr/bin/startup.sh
ADD crontab /etc/crontab
ADD supervisor.conf /etc/supervisor/conf.d/backup.conf
VOLUME /var/cloudbackups/workdir
VOLUME /var/cloudbackups/archives
RUN touch /var/log/backup.log

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  cron \
  curl \
  supervisor \
  build-essential \
  unzip \
  vim

# Install LastPass CLI

WORKDIR /usr/local/src

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git \
  openssl \
  libcurl4-openssl-dev \
  libxml2 \
  libssl-dev \
  libxml2-dev \
  pinentry-curses \
  xclip \
  cmake \
  build-essential \
  pkg-config

RUN git clone https://github.com/lastpass/lastpass-cli.git

WORKDIR /usr/local/src/lastpass-cli

RUN make
RUN make install

VOLUME /root/.lpass

# Install IMAP Backup

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git-core \
  curl \
  zlib1g-dev \
  build-essential \
  libssl-dev \
  libreadline-dev \
  libyaml-dev \
  libsqlite3-dev \
  sqlite3 \
  libxml2-dev \
  libxslt1-dev \
  libcurl4-openssl-dev \
  python-software-properties \
  libffi-dev

RUN git clone https://github.com/sstephenson/rbenv.git .rbenv
RUN echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(rbenv init -)"' >> ~/.bashrc
RUN git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
RUN echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
RUN /root/.rbenv/bin/rbenv install -v 2.4.1
RUN /root/.rbenv/bin/rbenv global 2.4.1

RUN /root/.rbenv/shims/gem install 'imap-backup'

VOLUME /root/.imap-backup

# Install Geeknote

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python \
  python-setuptools
WORKDIR /usr/local/src
RUN git clone https://github.com/VitaliyRodnenko/geeknote.git
WORKDIR /usr/local/src/geeknote
RUN python setup.py install
RUN mkdir /var/cloudbackups/workdir/evernote

VOLUME /root/.geeknote

# Install RClone

WORKDIR /usr/local/src

RUN curl -O https://downloads.rclone.org/rclone-v1.36-linux-amd64.zip
RUN unzip rclone-v1.36-linux-amd64.zip
WORKDIR /usr/local/src/rclone-v1.36-linux-amd64
RUN cp rclone /usr/bin/
RUN chmod +x /usr/bin/rclone

VOLUME /root/.config/rclone

# Install GooBook

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python \
  python-dev \
  python-pip

RUN pip install goobook

ADD goobookrc /root/.goobookrc

VOLUME /root/goobook

# Closeout

WORKDIR /root
CMD ["/usr/bin/startup.sh"]
