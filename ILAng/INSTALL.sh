#!/bin/bash
#-------------------------------
# Install all dependent packages
#-------------------------------

if [ -d "/tmp/z3/build" ]; then
	echo "Did you just install?"
	if [ ! -f "/tmp/ILAinstalled" ]; then
		echo "And it was not installed correctly."
	fi
	exit 1
fi

if [ ! -w ~ ]; then
	echo "Error: Unable to write to home directory."
	exit 2
fi

cd packages
PACKDIR=$(pwd)

# ubuntu deb packages
sudo dpkg -i *.deb

# z3
unzip z3-bin-only.zip -d /tmp
cd /tmp/z3/build
sudo make install

# glog
cd ${PACKDIR}
unzip glog-master.zip -d /tmp
cd /tmp/glog-master
mkdir -p build
cd build
cmake ..
make
sudo make install

#yosys
cd ${PACKDIR}
unzip yosys -d ~

#clang+llvm
#tar xzvf clang+llvm-2.9-bin.tar.gz -C ~

#cbmc
#unzip cbmc -d ~

#ila tool Need to change something there!
cd ${PACKDIR}/../
cp -r ILA-Tools ~/
cd ~/ILA-Tools/build
make
# make run_test, we will not do this explicitly
sudo make install
sudo ldconfig
cd ~/ILA-Tools/py-tmpl-synth
bjam
# add environment variable to initial script
export PYTHONPATH=~/ILA-Tools/py-tmpl-synth/bin/gcc-7/debug/cpp11-on:$PYTHONPATH
export ILAROOT=~/ILA-Tools
echo "export PYTHONPATH=~/ILA-Tools/py-tmpl-synth/bin/gcc-7/debug/cpp11-on:$PYTHONPATH" >> ~/.bashrc
echo "export ILAROOT=~/ILA-Tools" >> ~/.bashrc


echo "${ILAROOT}" > /tmp/ILAinstalled

echo
echo "---------------------------"
echo "  Installation Completed.  "
echo "---------------------------"

# return to its original directory
cd ${PACKDIR}/../


