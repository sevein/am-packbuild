%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


#
# Packages
#

Name: archivematica
Version: %{rpmversion}
Release: %{rpmrelease}
Summary: Archivematica digital preservation system
Group: Application/System
License: AGPLv3
Source0: %{git_repo}
BuildRequires: git, gcc, openldap-devel, openssl-devel, python36-virtualenv, python36-pip, mariadb-devel, libxslt-devel, python36-devel, python36-distutils-extra, python36-setuptools, libffi-devel, openssl-devel, gcc-c++, postgresql-devel, nodejs
Requires: python36-devel
AutoReq: No
AutoProv: No
%description
Archivematica is a web- and standards-based, open-source application which allows your institution to preserve long-term access to trustworthy, authentic and reliable digital content.

%package common
Summary: Archivematica common libraries
Requires: archivematica, shadow-utils
%description common
Common files and libraries for Archivematica.

%package mcp-server
Requires: archivematica, archivematica-common
Summary: Archivematica MCP server
AutoReq: No
AutoProv: No

%description mcp-server
Archivematica MCP server.

%package mcp-client
Summary: Archivematica MCP client
Requires: archivematica, archivematica-common
Requires: bzip2
Requires: tesseract
Requires: tree
Requires: p7zip
Requires: p7zip-plugins
Requires: pbzip2
Requires: ImageMagick
Requires: ghostscript
Requires: perl-Image-ExifTool
Requires: inkscape
Requires: clamav-data
Requires: clamav-update
Requires: clamav-filesystem
Requires: clamav
Requires: clamav-devel
Requires: clamav-lib
Requires: clamd
Requires: libvpx
Requires: libraw1394
Requires: libpst
Requires: openjpeg
Requires: mediainfo
Requires: mediaconch
Requires: md5deep
Requires: uuid
# Packages from Archivematica repo
Requires: siegfried
Requires: fits
Requires: atool
Requires: jhove
# Packages from https://forensics.cert.org/
Requires: bulk_extractor
Requires: sleuthkit
Requires: libewf
# Packages from Nux repo
Requires: ffmpeg
Requires: ufraw

AutoReq: No
AutoProv: No
%description mcp-client
Archivematica MCP client.

%package dashboard
Summary: Archivematica dashboard
Requires: archivematica, nginx, policycoreutils-python, gettext
AutoReq: No
AutoProv: No
%description dashboard
Archivematica dashboard with Nginx + gunicorn.

#
# Files
#

# Archivematica
%files
/usr/share/archivematica/virtualenvs/archivematica/

# Common
%files common
/usr/lib/archivematica/archivematicaCommon/
/var/archivematica/sharedDirectory/

# MCPServer
%files mcp-server
/usr/lib/archivematica/MCPServer/
/usr/lib/systemd/system/archivematica-mcp-server.service
%config(noreplace) /etc/sysconfig/archivematica-mcp-server
%config(noreplace) /etc/archivematica/serverConfig.conf
%config(noreplace) /etc/archivematica/serverConfig.logging.json

# MCPClient
%files mcp-client
/usr/lib/archivematica/MCPClient/
/usr/lib/systemd/system/archivematica-mcp-client.service
%config(noreplace) /etc/sysconfig/archivematica-mcp-client
%config(noreplace) /etc/archivematica/clientConfig.conf
%config(noreplace) /etc/archivematica/clientConfig.logging.json

# Dashboard
%files dashboard
/usr/share/archivematica/dashboard/
/usr/lib/systemd/system/archivematica-dashboard.service
%config(noreplace) /etc/sysconfig/archivematica-dashboard
%config(noreplace) /etc/nginx/conf.d/archivematica-dashboard.conf
%config(noreplace) /etc/archivematica/dashboard.gunicorn-config.py
%config(noreplace) /etc/archivematica/dashboard.logging.json

#
# Preparations
#

%prep
rm -rf /usr/share/python/archivematica*
rm -rf /usr/lib/archivematica
rm -rf %{_sourcedir}/*
rm -rf %{buildroot}/*
mkdir -p %{buildroot}/%{install_dir}

git clone \
  --quiet \
  --branch %{_branch} \
  --depth 1 \
  --single-branch \
    %{git_repo} \
    %{_sourcedir}/%{name}

#
# Install
#

%install
mkdir -p \
  %{buildroot}/etc/archivematica/ \
  %{buildroot}/usr/lib/archivematica/MCPServer \
  %{buildroot}/usr/lib/archivematica/MCPClient \
  %{buildroot}/usr/lib/archivematica/archivematicaCommon \
  %{buildroot}/usr/share/archivematica/virtualenvs/archivematica \
  %{buildroot}/usr/share/archivematica/dashboard \
  %{buildroot}/var/archivematica/sharedDirectory \
  %{buildroot}/etc/sysconfig \
  %{buildroot}/usr/lib/systemd/system \
  %{buildroot}/etc/nginx/conf.d

# Archivematica virtual environment
virtualenv-3.6 /usr/share/archivematica/virtualenvs/archivematica
/usr/share/archivematica/virtualenvs/archivematica/bin/pip install --upgrade pip
/usr/share/archivematica/virtualenvs/archivematica/bin/pip install -r %{_sourcedir}/%{name}/requirements-py3.txt
virtualenv-3.6 --relocatable /usr/share/archivematica/virtualenvs/archivematica
cp -rf /usr/share/archivematica/virtualenvs/archivematica/* %{buildroot}/usr/share/archivematica/virtualenvs/archivematica/

# Common
cp -rf %{_sourcedir}/%{name}/src/archivematicaCommon/lib/* %{buildroot}/usr/lib/archivematica/archivematicaCommon/

# MCPServer
cp -rf %{_sourcedir}/%{name}/src/MCPServer/lib/* %{buildroot}/usr/lib/archivematica/MCPServer/
cp %{_sourcedir}/%{name}/src/MCPServer/install/serverConfig.logging.json %{buildroot}/etc/archivematica/serverConfig.logging.json
cp %{_sourcedir}/%{name}/src/MCPServer/install/serverConfig.conf %{buildroot}/etc/archivematica/serverConfig.conf
cp %{_etcdir}/archivematica-mcp-server.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-server.service
cp %{_etcdir}/archivematica-mcp-server.env %{buildroot}/etc/sysconfig/archivematica-mcp-server

# MCPClient
cp -rf %{_sourcedir}/%{name}/src/MCPClient/lib/* %{buildroot}/usr/lib/archivematica/MCPClient
cp %{_sourcedir}/%{name}/src/MCPClient/install/clientConfig.logging.json %{buildroot}/etc/archivematica/clientConfig.logging.json
cp %{_sourcedir}/%{name}/src/MCPClient/install/clientConfig.conf %{buildroot}/etc/archivematica/clientConfig.conf
cp %{_etcdir}/archivematica-mcp-client.service %{buildroot}/usr/lib/systemd/system/archivematica-mcp-client.service
cp %{_etcdir}/archivematica-mcp-client.env %{buildroot}/etc/sysconfig/archivematica-mcp-client

# Dashboard
cp %{_sourcedir}/%{name}/src/dashboard/install/dashboard.gunicorn-config.py %{buildroot}/etc/archivematica/dashboard.gunicorn-config.py
cp %{_sourcedir}/%{name}/src/dashboard/install/dashboard.logging.json %{buildroot}/etc/archivematica/dashboard.logging.json
cp %{_etcdir}/archivematica-dashboard.service %{buildroot}/usr/lib/systemd/system/archivematica-dashboard.service
cp %{_etcdir}/archivematica-dashboard.env %{buildroot}/etc/sysconfig/archivematica-dashboard
cp %{_etcdir}/dashboard.nginx %{buildroot}/etc/nginx/conf.d/archivematica-dashboard.conf

cd %{_sourcedir}/%{name}/src/dashboard/frontend/ && npm install --unsafe-perm
find %{_sourcedir}/%{name}/src/dashboard/ | grep static
cp -rf %{_sourcedir}/%{name}/src/dashboard/src/* %{buildroot}/usr/share/archivematica/dashboard/

#
# Clean up build directory
#

%clean
rm -rf %{buildroot}

#
# Post install scripts
#

%post common

# Create archivematica user and group
getent group archivematica >/dev/null || groupadd -f -g 333 -r archivematica
if ! getent passwd archivematica >/dev/null ; then
  if ! getent passwd 333 >/dev/null ; then
    useradd -r -u 333 -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
    else
    useradd -r -g archivematica -d /var/lib/archivematica/ -s /sbin/nologin -c "Archivematica system account" -m archivematica
  fi
fi

# Configure permissions of shared directory
chown -R archivematica:archivematica /var/archivematica/sharedDirectory

# MCPServer
%post mcp-server
mkdir -p /var/log/archivematica/MCPServer
chown -R archivematica:archivematica /var/log/archivematica/MCPServer
systemctl daemon-reload

# MCPClient
%post mcp-client
mkdir -p /var/log/archivematica/MCPClient
chown -R archivematica:archivematica /var/log/archivematica/MCPClient
systemctl daemon-reload

# Dashboard
%post dashboard
mkdir -p /var/log/archivematica/dashboard

# Create Django key
KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)
sed -i "s/CHANGE_ME_WITH_A_SECRET_KEY/\"$KEY\"/g" /etc/sysconfig/archivematica-dashboard
# Update SELinux policy
if [ x$(semanage port -l | grep http_port_t | grep 7400 | wc -l) == x0 ]; then
  semanage port -a -t http_port_t -p tcp 7400
fi


#
# Posttrans install script
#

%posttrans dashboard
# Update old virtual environment paths in configuration files
sed -i "s/\/usr\/share\/archivematica\/virtualenvs\/archivematica-\(dashboard\|mcp-server\|mcp-client\)\//\/usr\/share\/archivematica\/virtualenvs\/archivematica\//g" \
  /etc/sysconfig/archivematica-mcp-server \
  /etc/sysconfig/archivematica-mcp-client \
  /etc/sysconfig/archivematica-dashboard \
  /usr/lib/systemd/system/archivematica-mcp-server.service \
  /usr/lib/systemd/system/archivematica-mcp-client.service \
  /usr/lib/systemd/system/archivematica-dashboard.service
systemctl daemon-reload
# Run django collectstatic and compilemessages.
# These tasks need to be run after postun script on upgrades
# because the old virtualenv files need to be removed from the old package.
# https://github.com/archivematica/Issues/issues/1312
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#ordering
mkdir -p /usr/share/archivematica/dashboard/static
bash -c " \
  set -a -e -x
  source /etc/sysconfig/archivematica-dashboard \
    || (echo 'Environment file not found'; exit 1)
  cd /usr/share/archivematica/dashboard
  /usr/share/archivematica/virtualenvs/archivematica/bin/python3.6 manage.py collectstatic --noinput --clear
  /usr/share/archivematica/virtualenvs/archivematica/bin/python3.6 manage.py compilemessages
";
chown -R archivematica:archivematica /var/log/archivematica/dashboard
systemctl daemon-reload
