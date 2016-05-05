%{?scl:%scl_package jline2}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

# Exclude generation of osgi() style provides, since they are not
# SCL-namespaced and may conflict with base RHEL packages.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1045447
%global __provides_exclude ^osgi(.*)$

Name:             %{?scl_prefix}jline2
Version:          2.10
# Release should be higher than el6 builds. Use convention
# 60.X where X is an increasing int. 60 for rhel-6. We use
# 70.X for rhel-7. For some reason we cannot rely on the
# dist tag.
Release:          70.5%{?dist}
Summary:          JLine is a Java library for handling console input
Group:            Development/Libraries
License:          BSD and ASL 2.0
URL:              https://github.com/jline/jline2

# git clone git://github.com/jline/jline2.git
# cd jline2/ && git archive --format=tar --prefix=jline-2.10/ jline-2.10 | xz > jline-2.10.tar.xz
Source0:          jline-%{version}.tar.xz

BuildArch:        noarch

BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    %{?scl_prefix_maven}maven-compiler-plugin
BuildRequires:    %{?scl_prefix_maven}maven-jar-plugin
BuildRequires:    %{?scl_prefix_maven}maven-surefire-plugin
BuildRequires:    %{?scl_prefix_maven}maven-install-plugin
BuildRequires:    %{?scl_prefix_java_common}junit
BuildRequires:    %{?scl_prefix_java_common}jansi
BuildRequires:    %{?scl_prefix_maven}fusesource-pom
BuildRequires:    %{?scl_prefix_maven}maven-surefire-provider-junit

%{?scl:Requires: %scl_runtime}

%description
JLine is a Java library for handling console input. It is similar
in functionality to BSD editline and GNU readline. People familiar
with the readline/editline capabilities for modern shells (such as
bash and tcsh) will find most of the command editing features of
JLine to be familiar. 

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
%{?scl:Requires: %scl_runtime}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n jline-%{version}

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_xpath_remove "pom:build/pom:pluginManagement/pom:plugins/pom:plugin[pom:artifactId = 'maven-site-plugin']"

# Do not import non-existing internal package
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Import-Package"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions" "<Import-Package>javax.swing;resolution:=optional,!org.fusesource.jansi.internal</Import-Package>"

# Let maven bundle plugin figure out the exports.
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Export-Package"
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc CHANGELOG.md README.md LICENSE.txt
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Wed Mar 30 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.5
- Own jline2 pom directory.
- Resolves: RHBZ#1317970

* Wed Jan 27 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.4
- Rebuild for RHSCL 2.2.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.3
- Use java common's libs as BR.

* Thu Dec 18 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.2
- Use maven30 collection for building.
- Use java common's requires/provides generators.

* Mon Jun 23 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.0.18-70.1
- Add requires for thermostat1-runtime package.

* Mon Jan 27 2014 Severin Gehwolf <sgehwolf@redhat.com> - 2.10-13
- Own scl-ized jline2 directory in javadir.
- Resolves: RHBZ#1057169

* Fri Dec 20 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-12
- Don't generate osgi() style provides.
- Resolves: RHBZ#1045447.

* Wed Nov 27 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-11
- Properly enable SCL.

* Wed Nov 06 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-10
- Use xmvn to install to proper SCL-ized location.

* Tue Sep 24 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-9
- Bump release for rebuild.

* Wed Aug 28 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-8
- SCL-ize package.

* Fri Apr 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-7
- Remove unneeded animal-sniffer BR.

* Tue Mar 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-6
- Fix OSGi metadata. Don't export packages which aren't in this
  package. Fixes RHBZ#920756.

* Mon Mar 11 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-5
- Provide %{_javadir}/%{name}.jar symlink. Fix RHBZ#919640.

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-4
- Install versioned JAR and POM
- Add missing BR: animal-sniffer
- Resolves: rhbz#911559

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.10-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-2
- Do not import non-existing org.fusesource.jansi.internal package

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-1
- Upstream release 2.10
- Removed patches, using pom macros now

* Fri Oct 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.5-7
- Fix OSGi Import-Package header so as to not import non existing
  org.fusesource.jansi.internal package.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-4
- jline.console.ConsoleReader.back should be protected instead of private [rhbz#751208]

* Wed Sep 21 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-3
- Updated license
- Removed unnecessary add_to_maven_depmap

* Thu Sep 08 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-2
- Cleaned spec

* Tue May 31 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-1
- Initial packaging
