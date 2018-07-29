FROM ubuntu:14.04

WORKDIR /root

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y
RUN mkdir /var/cloudbackups
RUN mkdir /var/cloudbackups/workdir
RUN mkdir /var/cloudbackups/archives
VOLUME /var/cloudbackups/workdir
VOLUME /var/cloudbackups/archives
VOLUME /etc/cloudbackup

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  cron \
  curl \
  build-essential \
  unzip \
  vim \
  git

# Install Python

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python \
  python-setuptools \
  python-dev \
  python-pip

# Install Node.js

RUN curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs

# Install Ruby

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
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

# Install LastPass CLI

WORKDIR /usr/local/src
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
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
RUN /root/.rbenv/shims/gem install 'imap-backup'
VOLUME /root/.imap-backup

# Install Geeknote

WORKDIR /usr/local/src
RUN git clone https://github.com/jeffkowalski/geeknote.git
WORKDIR /usr/local/src/geeknote
RUN python setup.py install
RUN pip install --upgrade .
RUN mkdir /var/cloudbackups/workdir/evernote
VOLUME /root/.geeknote

# Install RClone

WORKDIR /usr/local/src
RUN curl -O https://downloads.rclone.org/v1.42/rclone-v1.42-linux-amd64.zip
RUN unzip rclone-v1.42-linux-amd64.zip
WORKDIR /usr/local/src/rclone-v1.42-linux-amd64
RUN cp rclone /usr/bin/
RUN chmod +x /usr/bin/rclone
VOLUME /root/.config/rclone

# Install GooBook

RUN pip install goobook
ADD goobookrc /root/.goobookrc

# Install Todoist Backup

RUN npm install -g todoist-backup

# Install GitHub Backup

RUN npm install -g github-backup
RUN mkdir /var/cloudbackups/workdir/github

# Closeout

COPY scripts /scripts

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY interface /usr/src/app
RUN npm install
CMD ["node", "index.js"]
