# jonas
Command line tool for transparently running shell commands using docker containers.

## Features
* Automatic volumes detection - scans arguments passed to the invoked commands looking for paths and mounts them. If given path is nonexistent but has an existing ancestor, this ancestor is mounted instead. This allows handling files created by the wrapped command.
* Mapping uid and guid into docker containers

## Example usage
Suppose you want to use `mkdir` command from Alpine linux:
1. Create wrapper script  
```sh
jonasadm -i alpine -c mkdir > mkdir
chmod u+x mkdir
```
2. Run the script with arguments needed by mkdir:
```sh
./mkdir -p ./mydir/subdir
```

`jonas` will detect that `./mydir/subdir` is a nonexistent directoy with existing ancestor `.`.
Thus an alpine linux container will be created with current directory (`.`) mounted in
and command `mkdir -p ./mydir/subdir` will be run inside.


## Help
For full list of possible options see `jonasadm -h`.


## Installation
Clonse the repository and place files `jonas` and `jonasadm` in your PATH
referencing `jonas.py` and `jonasadm.py` respectively.
The Makefile contains helper script placing correct links in `/usr/bin/`:
```sh
sudo make install
```


## Name origin
Reference to biblical Jonas swallowed by a whale.

## License
MIT License, see the [LICENSE](LICENSE) file.
