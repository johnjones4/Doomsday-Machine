import imaplib
from imaplib import IMAP4, IMAP4_SSL, Time2Internaldate
import os
import os.path as path
from doomsdaymachine.sync_map import SyncMap
import time
from datetime import date, timedelta
from doomsdaymachine.util import format_filename

imaplib._MAXLINE = 1000000

def execute_imap(logger, config, job):
    syncer = SyncMap(job)
    if job["options"]["ssl"]:
        imap = IMAP4_SSL(job["options"]["host"], port=job["options"]["port"])
    else:
        imap = IMAP4(job["options"]["host"], port=job["options"]["port"])
    if job["options"]["tls"]:
        imap.starttls()
    imap.login(job["options"]["username"], job["options"]["password"])
    for mailbox in job["options"]["mailboxes"]:
        logger.info(f"Downloading {mailbox}")
        mbox_folder = path.join(job["output_folder"], format_filename(mailbox))
        if not path.isdir(mbox_folder):
            os.mkdir(mbox_folder)
        imap.select(mailbox)
        since_timestamp = syncer.get_last_modified(mailbox)
        if since_timestamp == 0:
            logger.debug("Doing deep search of mailbox")
            downloaded = None
            start = date.today()
            end = start - timedelta(days=30)
            while downloaded != 0:    
                logger.debug(f"Searching {str(start)} to {str(end)}")
                criteria = f"(BEFORE {start.strftime('%d-%b-%Y')}) (SINCE {end.strftime('%d-%b-%Y')})"
                downloaded = search_mail(logger, imap, mbox_folder, criteria)
                start = end
                end = start - timedelta(days=30)
        else:
            since = date.fromtimestamp(since_timestamp)
            logger.debug(f"Searching since {str(since)}")
            criteria = "(SINCE " + since.strftime("%d-%b-%Y") + ")"
            search_mail(logger, imap, mbox_folder, criteria)
        syncer.set_last_modified(mailbox, time.time())
        syncer.save()
    syncer.close()

def search_mail(logger, imap, mbox_folder, criteria):
    downloaded = 0
    tmp, data = imap.search(None, criteria)
    for num in data[0].split():
        downloaded += 1
        logger.debug(f"Getting message {num.decode('utf-8')}")
        tmp, mdata = imap.fetch(num, "(RFC822)")
        msg_file_path = path.join(mbox_folder, f"{num.decode('utf-8')}.msg")
        with open(msg_file_path, "wb") as msg_file:
            logger.debug(f"Saving {num.decode('utf-8')}")
            msg_file.write(mdata[0][1])
            #TODO attachment
    return downloaded
