# nanodb-tool
Python script allowing exports from nano's LMDB database.

[LMDB](http://www.lmdb.tech/doc/) is currently used by [nano](https://github.com/nanocurrency/raiblocks) as the kv store for it's distributed, trust-less data model.

Nano provides an RPC interface that allows for similar functionality to this script, however it is slow and unreliable.

LMDB allows for multiple concurrent readers but only a single writer. As this tool is for exporting blocks, the lmdb environment is opened read-only. This means the tool can be run against the database while the node is running.

This script uses [py-lmdb](https://github.com/dw/py-lmdb) and hopes to eventually emulate the design of the included 'tool.py'.

**NOTE:** You must symlink your data.ldb to data.mdb in your RaiBlocks directory for this script to work (e.g. `ln -s data.ldb data.mdb`).

## Dependencies

```
$ pip install lmdb
```

## Example Usage

* Print the number of records in all dbs:
```
$ nanodb-tool -e /path/to/RaiBlocks/ -r
```

* List databases in nano lmdb env:
```
$ nanodb-tool -e /path/to/RaiBlocks/ -l
```

* Dump key:value blobs from all dbs in the env:
```
$ nanodb-tool -e /path/to/RaiBlocks/ -v
```

* Dump *decoded* key values from all supported dbs:
```
$ nanodb-tool -e . -d
```

## TODO

 * increase decode support
 * implement 'command arg' command line interface (e.g. `nanodb-tool pub send` or `nanodb decode open`) ala lmdb tool.py
 * figure out how to fix filthy decode output formats
 * publish blocks to kafka (db = topic)
 * learn python


