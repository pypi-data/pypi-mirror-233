import logging
logger = logging.getLogger(__name__)

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dd8.utils.smtp_ import Gmail

if __name__ == '__main__':    
    from_ = 'yuanqing87@gmail.com'
    key = os.getenv('GMAIL_SECRET')

    subject = 'test'
    body = 'test'

    client = Gmail()
    mailitem = client.create_email('yuanqing87@gmail.com', '', '', subject, body, [r'E:\Program Files\Dropbox\Yuan Qing\Work\Projects\Libraries\3. Python\dd8\data\ftx_data.csv'])
    client.send_email(from_, key, mailitem )
