import hashlib as _hashlib
import string
from typing import Callable as _Callable

def Hash(filePath: str, hashFunc=_hashlib.sha256()) -> str:
    from simpleworkspace.types.byte import ByteEnum
    Read(filePath, lambda x: hashFunc.update(x), readSize=ByteEnum.MegaByte.value * 1, getBytes=True)
    return hashFunc.hexdigest()

def Read(filePath: str, callback: _Callable[[str | bytes], None] = None, readSize=-1, readLimit=-1, getBytes=False) -> (str | bytes | None):
    """
    :callback:
        the callback is triggered each time a file is read with the readSize, 
        callback recieves one parameter as bytes or str depending on getBytes param
    :readSize: amount of bytes to read at each callback, default of -1 reads all at once
    :ReadLimit: Max amount of bytes to read, default -1 reads until end of file
    :getBytes: specifies if the data returned is in string or bytes format
    :Returns
        if no callback is used, the filecontent will be returned\n
        otherwise None
    """
    from io import BytesIO, StringIO


    if (readSize == -1 and readLimit >= 0) or (readLimit < readSize and readLimit >= 0):
        readSize = readLimit

    content = BytesIO() if getBytes else StringIO()
    openMode = "rb" if getBytes else "r"
    totalRead = 0
    with open(filePath, openMode, newline=None) as fp:
        while True:
            if readLimit != -1 and totalRead >= readLimit:
                break
            data = fp.read(readSize)
            totalRead += readSize
            
            if not data:
                break

            if callback is None:
                content.write(data)
            else:
                callback(data)

    if callback is None:
        return content.getvalue()
    return None


    
def Create(filepath: str, data: bytes | str = None):
    if type(data) is str:
        data = data.encode()
    with open(filepath, "wb") as file:
        if data is not None:
            file.write(data)

def Append(filepath: str, data: bytes | str):
    if type(data) is bytes:
        pass  # all good
    elif type(data) is str:
        data = data.encode()
    else:
        raise Exception("Only bytes or string can be used to append to file")
    with open(filepath, "ab") as file:
        file.write(data)


def CleanInvalidNameChars(filename:str, allowedCharset = string.ascii_letters + string.digits + " .-_"):
    return ''.join(c for c in filename if c in allowedCharset)



