import os as _os

class PathInfo:
    """
    Notes
    * all backslashes are replaced with forward ones for compability 

    """
    from functools import cached_property as _cached_property

    def __init__(self, filepath:str) -> None:
        self._path = filepath.replace("\\", "/")

    @_cached_property
    def IsDirectory(self) -> bool:
        return _os.path.isdir(self.Path)
    
    @_cached_property
    def IsFile(self) -> bool:
        return _os.path.isfile(self.Path)
    
    @_cached_property
    def IsSymlink(self) -> bool:
        return _os.path.islink(self.Path)
    
    @_cached_property
    def Exists(self) -> bool:
        return _os.path.exists(self.Path)
    
    def Join(self, *otherPaths:str):
        return self.__class__(_os.path.join(self.Path, *otherPaths))

    @_cached_property
    def Stats(self, follow_symlinks=True):
        return _os.stat(self.Path, follow_symlinks=follow_symlinks)

    @property
    def Path(self) -> str:
        '''the input path, example case: a/b/test.exe -> a/b/test.exe'''
        return self._path
    
    @_cached_property
    def AbsolutePath(self) -> str:
        '''converts the input path to an absolute path, example case: a/b/test.exe -> c:/a/b/test.exe'''
        return _os.path.realpath(self.Path).replace("\\", "/")

    @_cached_property
    def Tail(self) -> str:
        '''Retrieves everything before filename, example case: a/b/test.exe -> a/b'''

        tail, head = self._HeadTail
        return tail

    @_cached_property
    def Head(self) -> str:
        '''Retrieves everything after last slash which would be the filename or directory, example case: a/b/test.exe -> test.exe'''

        tail,head = self._HeadTail
        return head
    
    @_cached_property
    def Filename(self) -> str:
        '''retrieves filename without extension, example case: a/b/test.exe -> test'''

        filename = self._FilenameSplit[0]
        return filename
    
    @_cached_property
    def FileExtension(self):
        '''retrieves fileextension without the dot, example case: a/b/test.exe -> exe'''

        if(len(self._FilenameSplit) == 2):
            return self._FilenameSplit[1]
        return ""
    
    @property
    def Parent(self) -> 'PathInfo':
        return PathInfo(self.Tail)

    @_cached_property
    def _HeadTail(self) -> tuple[str,str]:
        return _os.path.split(self.Path)
    
    @_cached_property
    def _FilenameSplit(self) -> str:
        return self.Head.rsplit(".", 1)
    
    @property
    def __str__(self) -> str:
        return self.Path

    def __truediv__(self, otherPath:str):
        return self.Join(otherPath)

def FindEmptySpot(filepath: str):
    pathInfo = PathInfo(filepath)
    TmpPath = filepath
    i = 1
    while _os.path.exists(TmpPath) == True:
        TmpPath = f"{pathInfo.Tail}{pathInfo.Filename}_{i}{pathInfo.FileExtension}"
        i += 1
    return TmpPath

def GetAppdataPath(appName=None, companyName=None):
    """
    Retrieves roaming Appdata folder.\n
    no arguments        -> %appdata%/\n
    appName only        -> %appdata%/appname\n
    appname and company -> %appdata%/appname/companyName\n
    """
    from simpleworkspace.types.os import OperatingSystemEnum
    

    currentOS = OperatingSystemEnum.GetCurrentOS()
    if currentOS == OperatingSystemEnum.Windows:
        pathBuilder = _os.getenv('APPDATA')
    elif currentOS == OperatingSystemEnum.MacOS:
        pathBuilder = _os.path.expanduser('~/Library/Application Support/')
    else:
        pathBuilder = _os.getenv('XDG_DATA_HOME', _os.path.expanduser("~/.local/share"))

    if(companyName is not None):
        pathBuilder = _os.path.join(pathBuilder, companyName)
    if(appName is not None):
        pathBuilder = _os.path.join(pathBuilder, appName)
    return pathBuilder
    
