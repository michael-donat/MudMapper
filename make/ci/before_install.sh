#!/bin/bash
curl -O http://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.10.1/PyQt-x11-gpl-4.10.1.tar.gz?r=http%3A%2F%2Fwww.riverbankcomputing.co.uk%2Fsoftware%2Fpyqt%2Fdownload&ts=1368089507&use_mirror=garr
tar -xvf PyQt-x11-gpl-4.10.1.gz
cd PyQt-x11-gpl-4.10.1
python configure.py --confirm-license
make -j 4
sudo make install