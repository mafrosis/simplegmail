import base64
import os
from typing import Optional

from googleapiclient import discovery


from gmsa.exceptions import AttachmentSaveError


class Attachment:
    '''
    The Attachment class for attachments to emails in your Gmail mailbox.
    '''
    def __init__(self, service: discovery.Resource, user_id: str, msg_id: str,
                 att_id: str, filename: str, filetype: str, data: Optional[bytes]=None):
        '''
        Args:
            service: The Gmail service object.
            user_id: The username of the account the message belongs to.
            msg_id: The id of message the attachment belongs to.
            att_id: The id of the attachment.
            filename: The filename associated with the attachment.
            filetype: The mime type of the file.
            data: The raw data of the file. Default None.
        '''
        self.service = service
        self.user_id = user_id
        self.msg_id = msg_id
        self.id = att_id
        self.filename = filename
        self.filetype = filetype
        self.data = data


    def save(self, filepath: Optional[str]=None, overwrite: bool=False):
        '''
        Saves the attachment. Downloads file data if not downloaded.

        Args:
            filepath: where to save the attachment. Default uses the filename stored.
            overwrite: whether to overwrite existing files. Default False.
        '''
        # Use filename from MIME if not specified
        if filepath is None:
            filepath = self.filename

        if not overwrite and os.path.exists(filepath):
            raise FileExistsError(
                f'Cannot overwrite file "{filepath}". Use overwrite=True if '
                'you would like to overwrite the file.'
            )

        def download() -> bytes:
            res = self.service.users().messages().attachments().get(
                userId=self.user_id, messageId=self.msg_id, id=self.id
            ).execute()

            return base64.urlsafe_b64decode(res['data'])

        if not self.data:
            self.data = download()

        try:
            with open(filepath, 'wb') as f:
                f.write(self.data)
        except (FileNotFoundError, PermissionError, OSError, IOError) as e:
            raise AttachmentSaveError(str(e)) from e
