import logging
import platform
import shutil
from pathlib import Path
from tempfile import (
    SpooledTemporaryFile,
    NamedTemporaryFile,
    _TemporaryFileWrapper,
)

from .dir_setting import DirSetting

_isWindows = platform.system() == "Windows"

logger = logging.getLogger(__name__)


class SpooledNamedTemporaryFile(SpooledTemporaryFile):
    """Temporary file wrapper, specialized to switch from BytesIO
    or StringIO to a real file when it exceeds a certain size or
    when a fileno or name is needed.
    """

    def __init__(self, *args, **kwargs):
        kwargs["dir"] = kwargs.pop("dir", DirSetting.tmpDirPath)
        SpooledTemporaryFile.__init__(self, *args, **kwargs)

    def rollover(self):
        if self._rolled:
            return
        file = self._file
        self._file = NamedTemporaryFile(**self._TemporaryFileArgs)
        del self._TemporaryFileArgs

        self._file.write(file.getvalue())
        self._file.seek(file.tell(), 0)

        self._rolled = True

    @property
    def name(self):
        """Name

        Trying to access "name" will cause the file to roll over
        """
        self.rollover()
        return self._file.name

    @property
    def delete(self):
        """Delete

        Fill the file be automatically deleted

        (Causes rollover)
        """
        self.rollover()
        if hasattr(self._file, "_closer"):
            return self._file._closer.delete
        return self._file.delete

    @delete.setter
    def delete(self, value):
        """Delete Setter

        Sets if the file will automatically be deleted by NamedTemporayFile

        (Causes rollover)
        """
        if _isWindows:
            raise Exception(
                "Windows NamedTemporaryFile files can not have delete unset. "
                "You will have to read the data and write it to your own file."
            )
        self.rollover()
        if hasattr(self._file, "_closer"):
            self._file._closer.delete = value
        else:
            self._file.delete = value

    @property
    def namedTemporaryFile(self) -> _TemporaryFileWrapper:
        """Named Temporary File

        Trying to access this property causes a rollover if required
        """
        self.rollover()
        return self._file

    def moveToPath(self, path: Path):
        if _isWindows:
            logger.debug(
                "We're copying this file as we can't prevent"
                "windows deleting the temporary file."
                "Expect double the space required."
            )
            # On windows, when a temporary file is opened with
            # NamedTemporaryFile, it sets the os.O_TEMPORARY flag
            # there is no way to tell it to not
            with open(path, "wb") as nf:
                data = self.read(10 * 1024 * 1024)
                while data:
                    nf.write(data)
                    data = self.read(10 * 1024 * 1024)
        else:
            self.delete = False
            shutil.move(self.name, path)
