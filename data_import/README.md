# HOW TO RUN
- From project root:

```
python -m data_import <command>
```

- From data_import package root:

```
./bootstrap.py <command>
```

# EXAMPLE USAGE:
- **Important Note** The xlsx should disable password for importing to work normally.
- Convert XLSX to pickle:
```
./bootstrap.py xlsx-to-pickle
```

- In case there are changes in xlsx, remove XLSX pickle:
```
./bootstrap.py rm-xlsx-pickle
```

- Generate MasterData pickle:
```
./bootstrap.py generate-master
```

- Truncate database tables:
```
./bootstrap.py truncate-db
```

- Load to Database
```
./bootstrap.py insert-db --customer=1 --forest=1
```

# FLOW:
- `XLSX -> pickle -> importer + converter -> intermediate pickle -> DbImporter -> DB`
