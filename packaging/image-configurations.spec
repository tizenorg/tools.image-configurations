%define baseline tizen-0.0
Summary:	Create kickstart files for Tizen images
Name:		image-configurations
Version:	6
Release:	1
License:	GPLv2
Group:		System/Base
URL:		http://www.tizen.org
Source:		image-configurations-%{version}.tar.bz2
Source1001: packaging/image-configurations.manifest 

BuildArch:	noarch
BuildRequires:  kickstarter >= 0.8

%description
Create Configuration files to build Tizen images 

%prep
%setup -q

%build
cp %{SOURCE1001} .
kickstarter -c configurations.yaml -r repos.yaml -i image-configs.xml

%install

mkdir -p %{buildroot}/usr/share/image-configurations
cp %{baseline}/*.ks %{buildroot}/usr/share/image-configurations
cp image-configs.xml %{buildroot}/usr/share/image-configurations

%files
%manifest image-configurations.manifest
%dir %_datadir/image-configurations
%_datadir/image-configurations/*.ks
%_datadir/image-configurations/image-configs.xml
