Name:		jnr-constants
Version:	0.11.4
Release:	1
Summary:	Java constants for POSIX and platform values
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/jnr/jnr-constants
Source0:	https://github.com/jnr/jnr-constants/archive/refs/tags/jnr-constants-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	jnr-parent
BuildSystem:	maven

%description
Platform and POSIX constants used by the jnr libraries.

%prep
%setup -q -n jnr-constants-jnr-constants-%{version}
# jnr-parent configures surefire with a JDK toolchain. No toolchain is installed,
# and that check runs even when tests are skipped.
python - <<'PY'
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
plugin = """      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration combine.self="override"/>
      </plugin>
"""
marker = "</plugins>"
text = text[:text.rfind(marker)] + plugin + text[text.rfind(marker):]
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
