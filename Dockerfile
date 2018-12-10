FROM python:3.6-jessie

RUN apt-get update

RUN apt-get update && apt-get install -y \
  cmake

# get samtools
RUN git clone https://github.com/samtools/htslib
RUN git clone https://github.com/samtools/samtools
RUN (cd /samtools; autoheader; autoconf -Wno-syntax; ./configure; make; make install)

# get bam readcount
RUN git clone https://github.com/genome/bam-readcount.git
RUN (mkdir brc-build; cd brc-build; cmake /bam-readcount; make; export PATH=$PATH:/brc-build/bin/)

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD /bin/bash
