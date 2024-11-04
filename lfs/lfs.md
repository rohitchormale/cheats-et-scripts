# LFS

## Steps

- [Check host system requirements](#check-host-system-requirements)
- [Make required partitions](#make-required-partitions)
- [Download required packages](#download-required-packages)
- [Compile temporary tools]()
- [Build necessary tools for constructing final lfs]()
- [Compile and install all packages one by one]()
- [Set up boot script]()
- [Install kernel]()



## Check host system requirements


### Hardware

- 4 core cpu
- 8 GB ram


### Software

- run [`version-check.sh`](version-check.sh)


## Make required partitions

### Layouts

#### Regular layout

- root (20G)
- swap same as ram (below 4G double of ram)
- GRUB bios partition (1 MB with label `BIOS Boot`)

#### Special layout

- `/boot` for kernel (200-500MB)
- `/boot/efi` for systems with UEFI (512MB)
- `/root`
- `/home` to share access across multiple distros (10-30GB)
- `/usr` binaries required for system to run. `/bin`, `/lib` and `sbin` simlinks to `/usr`
- `/opt` for large packages like KDE, Texlive (5-10G)
- `/tmp` will use `tmpfs` (optional)
- `/usr/src` store and share BLFS source files across distros (10-50G)

### Tools
- `cfdisk`
- `fdisk` to manage partitions for EFI based systems

    ```
    # list partitions
    fdisk -l

    # create partition
    fdisk <diskname>
    fdisk /dev/nvme0n2

    # install ext4 file system on lfs partition
    mkfs -v -t ext4 /dev/<xxx>

    # initialize swap partition
    mkswap /dev/<yyy>

    ```


- `gdisk` to manager partitions for GPT based systems


### Additional notes

- BIOS loads  a bootloader from `BIOS Boot` loader partition
- At boot time, the boot loader loads the kernel and the `initramfs` image into memory and starts the kernel. The kernel checks for the presence of the `initramfs` and if found, mounts it as `/` and runs `/init`a. The init program is typically a shell script. Note that the boot process takes longer, possibly significantly longer, if an initramfs is used.
- [initramfs](https://wiki.unbuntu.com/Initramfs)
- [file vs streams](https://stackoverflow.com/a/20937904)


## Additional setup

- set environment variables in ~/.bashrc
    - `export LFS=/mnt/lfs`
- set environment variables in /root/.bashrc
    - `export LFS=/mnt/lfs`
- mount new partition and create required dirs

    ```
    # mount lfs for regular layout
    mkdir -pv $LFS
    mkdir -v -t ext4 /dev/<xx> $LFS

    # mount lfs for special layout
    mkdir -pv $LFS
    mount -v -t ext4 /dev/<xxx> $LFS

    mkdir -v $LFS/home
    mount -v -t ext4 /dev/<yyy> $LFS/home

    mkdir -v $LFS/root
    mount -v -t ext4 /dev/<yyy> $LFS/root

    mkdir -v $LFS/boot
    mount -v -t ext4 /dev/<yyy> $LFS/boot

    mkdir -v $LFS/usr
    mount -v -t ext4 /dev/<yyy> $LFS/usr

    mkdir -v $LFS/opt
    mount -v -t ext4 /dev/<yyy> $LFS/opt

    mkdir -v $LFS/tmp
    mount -v -t ext4 /dev/<yyy> $LFS/tmp

    mkdir -v $LFS/usr/src
    mount -v -t ext4 /dev/<yyy> $LFS/usr/src

    ```

- add fstab entry  to remount partition on boot automatically

    ```
    /dev/<xxx>  /mnt/lfs ext4   defaults      1     1

    # for special layout add entries for all additional partitions similar to above
    ```

- enable swap

    ```
    /sbin/swapon -v /dev/<zzz>
    ```


## Download required packages


    mkdir -v $LFS/sources
    chmod -v a+wt $LFS/sources

    # download packages
    wget --input-file=wget-list-sysv --continue --directory-prefix=$LFS/sources

    # verify packages
    pushd $LFS/sources
      md5sum -c md5sums
    popd

    # https://www.linuxfromscratch.org/lfs/view/stable/wget-list-sysv
    # https://www.linuxfromscratch.org/lfs/view/stable/md5sums

    # If the packages and patches are downloaded as a non-root user, these files will be owned by the user. The file system records the owner by its UID, and the UID of a normal user in the host distro is not assigned in LFS. So the files will be left owned by an unnamed UID in the final LFS system. If you won't assign the same UID for your user in the LFS system, change the owners of these files to root now to avoid this issue:


    chown root:root $LFS/sources/*


## Create a required directory layout

Run as root


    mkdir -pv $LFS/{etc,var} $LFS/usr/{bin,lib,sbin}

    for i in bin lib sbin; do
      ln -sv usr/$i $LFS/$i
    done

    case $(uname -m) in
      x86_64) mkdir -pv $LFS/lib64 ;;
    esac

## Create a required user


    groupadd lfs
    useradd -s /bin/bash -g lfs -m -k /dev/null lfs

    # `-k` avoids copying skeleton files from `/etc/skel` by changing group location to special null device

    passwd lfs

    chown -v lfs $LFS/{usr{,/*},lib,var,etc,bin,sbin,tools}
    case $(uname -m) in
      x86_64) chown -v lfs $LFS/lib64 ;;
    esac

    su - lfs

    `-` tells su to start login shell


## Setup an environment

    su - lfs


    cat > ~/.bash_profile << "EOF"
    exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
    EOF


    cat > ~/.bashrc << "EOF"
    set +h
    umask 022
    LFS=/mnt/lfs
    LC_ALL=POSIX
    LFS_TGT=$(uname -m)-lfs-linux-gnu
    PATH=/usr/bin
    if [ ! -L /bin ]; then PATH=/bin:$PATH; fi
    PATH=$LFS/tools/bin:$PATH
    CONFIG_SITE=$LFS/usr/share/config.site
    export LFS LC_ALL LFS_TGT PATH CONFIG_SITE
    EOF


    [ ! -e /etc/bash.bashrc ] || mv -v /etc/bash.bashrc /etc/bash.bashrc.NOUSE


    cat >> ~/.bashrc << "EOF"
    export MAKEFLAGS=-j$(nproc)
    EOF


    source ~/.bash_profile
