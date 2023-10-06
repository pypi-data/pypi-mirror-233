##  Thư viện kiểm tra file type.

### Cài đặt:

```bash
 $ pip3 install m-filetype
 ```

Link chữ ký: https://en.wikipedia.org/wiki/List_of_file_signatures

### Sử dụng
```python
from mobio.sdks.filetype.file import File
from mobio.sdks.filetype.common import ExtensionImage

File.check_filetype_by_file_extensions(
    file_binary=file, # Check filetype của định dạng file binary.Mặc định None
    file_path=file_path, # Check filetype của path file
    extensions=[ExtensionImage.PNG] # Danh sách extension cần check.
)

```

#### Lấy extensions support
- Extension Image:
```python
from mobio.sdks.filetype.common import ExtensionImage
ExtensionImage.LIST_EXTENSION_SUPPORTED
```
- Extension Document:
```python
from mobio.sdks.filetype.common import ExtensionDocument
ExtensionDocument.LIST_EXTENSION_SUPPORTED
```
- Extension Audio:
```python
from mobio.sdks.filetype.common import ExtensionAudio
ExtensionAudio.LIST_EXTENSION_SUPPORTED
```