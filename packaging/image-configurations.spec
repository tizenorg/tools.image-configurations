%define baseline tizen-0.0

Summary:	Create kickstart files for Tizen images
Name:		image-configurations
Version:	9
Release:	1
License:	GPLv2
Group:		System/Base
URL:		http://www.tizen.org
Source:		image-configurations-%{version}.tar.gz
Source1001:	packaging/image-configurations.manifest

BuildArch:	noarch
BuildRequires:  kickstarter >= 0.8
BuildRequires:  sed

%description
Create Configuration files to build Tizen images

%prep
%setup -q

%build
cp %{SOURCE1001} .

%if "%{?tizen_profile_name}" == "mobile"
	%if "%{_repository}" == "emulator"
		kickstarter -c configurations_m_emulator.yaml -r repos.yaml -i image-configs.xml
	%else
		kickstarter -c configurations_m_target.yaml -r repos.yaml -i image-configs.xml
	%endif
%else
	%if "%{_repository}" == "emulator"
		kickstarter -c configurations_w_emulator.yaml -r repos.yaml -i image-configs.xml
	%else
		%if "%{_repository}" == "emulator-circle"
			kickstarter -c configurations_w_emulator-circle.yaml -r repos.yaml -i image-configs.xml
		%else
			%if "%{_repository}" == "target-b3"
				kickstarter -c configurations_w_target-b3.yaml -r repos.yaml -i image-configs.xml
			%else
				kickstarter -c configurations_w_target.yaml -r repos.yaml -i image-configs.xml
			%endif
		%endif
	%endif
%endif

%install
mkdir -p %{buildroot}/usr/share/image-configurations

cp %{baseline}/*.ks %{buildroot}/usr/share/image-configurations
cp image-configs.xml %{buildroot}/usr/share/image-configurations

%files
%manifest image-configurations.manifest
%dir %_datadir/image-configurations
%_datadir/image-configurations/*.ks
%_datadir/image-configurations/image-configs.xml
