# DRB File Metadata Addon

The _DRB file metadata addon_ allows to retrieve metadata for nodes provided by
the _**file driver**_.

Here the metadata list provided by this addon:

| name             | description                                        |
|:-----------------|:---------------------------------------------------|
| name             | filename                                           |
| size             | file size                                          |
| type             | file kind [REGULAR, DIRECTORY, LINK, SOCKET, ... ] |
| creationTime     | last update metadata or creation time in second    |
| modificationTime | last modification time in second                   |
| lastAccessTime   | last access time in second                         |
| owner            | file owner id                                      |
| group            | file group id                                      |
| nkink            | number of link attached to this file               |
| inode            | inode number or file index                         |
