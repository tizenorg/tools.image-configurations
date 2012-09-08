%define baseline SLP-2.0
Summary:	Create kickstart files for Tizen images
Name:		image-configurations
Version:	1
Release:	4
License:	GPLv2
Group:		System/Base
URL:		http://www.tizen.org
Source:		image-configurations-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:  kickstarter >= 0.8

%description
Create Configuration files to build Tizen images 

%prep
%setup -q

%build

%if "%{_project}" == "SLP:Build"
find . -name 'configurations*.yaml' -type f -exec sed -i -e "s#@SRNAME@#Build#g" {} \;
%else if "%{_project}" == "SLP:Main"
find . -name 'configurations*.yaml' -type f -exec sed -i -e "s#@SRNAME@#Main#g" {} \;
%else
find . -name 'configurations*.yaml' -type f -exec sed -i -e "s#@SRNAME@#Rel#g" {} \;
%endif

%if "%{_repository}" == "webkit"
kickstarter -c configurations-webkit.yaml -r repos.yaml -i image-configs.xml
%else
kickstarter -c configurations.yaml -r repos.yaml -i image-configs.xml
%endif

%install

mkdir -p %{buildroot}/usr/share/image-configurations

cp %{baseline}/*.ks %{buildroot}/usr/share/image-configurations
cp image-configs.xml %{buildroot}/usr/share/image-configurations

%files
%dir %_datadir/image-configurations
%_datadir/image-configurations/*.ks
%_datadir/image-configurations/image-configs.xml
