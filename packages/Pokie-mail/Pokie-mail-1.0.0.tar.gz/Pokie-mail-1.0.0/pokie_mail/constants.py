# Version
POKIE_MAIL_VERSION = ["1", "0", "0"]


def get_version():
    return ".".join(POKIE_MAIL_VERSION)


# Service names

SVC_MESSAGE_QUEUE = "sv_pokie_mail_msg_queue"
SVC_MESSAGE_TEMPLATE = "sv_pokie_mail_msg_template"

# MessageQueueRecord status
STATUS_DRAFT = "D"  # not committed to database yet
STATUS_QUEUED = "Q"
STATUS_LOCKED = "L"
STATUS_FAILED = "F"
STATUS_SENT = "S"

VALID_STATUS = [
    STATUS_QUEUED,
    STATUS_LOCKED,
    STATUS_FAILED,
    STATUS_SENT,
]

# communication channels

CHANNEL_SMTP = 0
