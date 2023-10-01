
from logging import Logger
from logging import getLogger

from oglio.IDFactory import IDFactory


class BaseXml:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._idFactory: IDFactory = IDFactory()

