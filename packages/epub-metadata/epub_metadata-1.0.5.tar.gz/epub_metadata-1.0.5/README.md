# epub-metadata
Get metadata from the Epub file.

# Install
```bash
pip install epub-metadata
```

# Example

```python
import epub_metadata
epub = epub_metadata.epub('tests/Alices Adventures in Wonderland.epub')
```

show all metadata from the Epub file

```python
print(epub.metadata)
# return all metadata from the Epub file
{
    'version': '2.0', 
    'title': "Alice's Adventures in Wonderland", 
    'creator': 'Lewis Carroll', 
    'date': '1865-07-04', 
    'cover': '/9j/4AAQSkZJRgABAQE...', 
    'cover_type': 'image/jpeg', 
    'description': '', 
    'publisher': 'D. Appleton and Co', 
    'identifier': 'eb2934ae-bb1a-4652-bce7-9f78fc5ca496'
}
```

only show the epub metadata
```python
print(epub.metadata.title)
# only print the title
Alice's Adventures in Wonderland
```