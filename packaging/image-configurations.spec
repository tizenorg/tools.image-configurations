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
  %endif
  %if "%{_repository}" == "target"
    kickstarter -c configurations_m_target.yaml -r repos.yaml -i image-configs.xml
  %endif
  %if "%{_repository}" == "target-Z130H"
    kickstarter -c configurations_m_target-Z130H.yaml -r repos.yaml -i image-configs.xml
  %endif
  %if "%{_repository}" == "target-TM1"
    kickstarter -c configurations_m_target-TM1.yaml -r repos.yaml -i image-configs.xml
  %endif
%endif

%if "%{?tizen_profile_name}" == "wearable"
  %if "%{_repository}" == "emulator"
    kickstarter -c configurations_w_emulator.yaml -r repos.yaml -i image-configs.xml
  %else
    kickstarter -c configurations_w_target.yaml -r repos.yaml -i image-configs.xml
  %endif
%endif

%if "%{?tizen_profile_name}" == "tv"
  %if "%{_repository}" == "emulator"
    kickstarter -c configurations_t_emulator.yaml -r repos.yaml -i image-configs.xml
  %else
    kickstarter -c configurations_t_target.yaml -r repos.yaml -i image-configs.xml
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
