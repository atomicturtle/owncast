# Owncast project RPM packaging repo

Currently building for Fedora 40, and Rocky 9 (aarch64, x86_64)


# Installation

## Rocky 9

wget -q -O - https://updates.atomicorp.com/installers/atomic |sudo bash

sudo dnf -y install epel-release

sudo crb enable

sudo dnf install owncast


## Fedora 40

wget -q -O - https://updates.atomicorp.com/installers/atomic |sudo bash


sudo dnf install owncast

