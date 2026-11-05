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
# A versionless jar plugin is removed, and the bundle plugin's manifest is
# not produced. jnr-parent's surefire toolchain runs even when tests are skipped.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(
	r"\s*<manifestFile>.*?</manifestFile>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = text.replace(
	"<artifactId>maven-jar-plugin</artifactId>",
	"<artifactId>maven-jar-plugin</artifactId>\n        <version>3.3.0</version>",
	1,
)
text = text.replace(
	"<build>",
	"""<build>
    <pluginManagement>
      <plugins>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <configuration combine.self="override"/>
        </plugin>
      </plugins>
    </pluginManagement>""",
	1,
)
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
