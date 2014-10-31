from api.APISettings import CHARSET
import sys
import logging

reload(sys)
sys.setdefaultencoding(CHARSET)

log = logging.getLogger(__name__)
