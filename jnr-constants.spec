Name:		jnr-constants
Version:	0.11.4
Release:	2
Summary:	Java constants for POSIX and platform values
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/jnr/jnr-constants
Source0:	https://github.com/jnr/jnr-constants/archive/refs/tags/jnr-constants-%{version}.tar.gz
# Gradle 9.9.1 strictly pins 0.10.4. The tag archive has no prebuilt jars.
Source1:	https://github.com/jnr/jnr-constants/archive/refs/tags/jnr-constants-0.10.4.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	jnr-parent
BuildSystem:	maven

%description
Platform and POSIX constants used by the jnr libraries. %{version} stays
the default jar. Gradle 9.9.1 strictly pins 0.10.4, so that jar is
installed beside it.

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
%setup -q -T -D -a 1 -n jnr-constants-jnr-constants-%{version}
find jnr-constants-jnr-constants-0.10.4 \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete

%build -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
mkdir -p jnr0104/classes
find jnr-constants-jnr-constants-0.10.4/src/main/java -name '*.java' > jnr0104/sources.list
test -s jnr0104/sources.list
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-d jnr0104/classes @jnr0104/sources.list
"$JAVA_HOME/bin/jar" cf jnr0104/jnr-constants.jar -C jnr0104/classes .
cat > jnr0104/jnr-constants.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.github.jnr</groupId>
  <artifactId>jnr-constants</artifactId>
  <version>0.10.4</version>
  <name>jnr-constants</name>
  <description>A set of platform constants (e.g. errno values)</description>
  <url>https://github.com/jnr/jnr-constants</url>
  <licenses>
    <license>
      <name>The Apache Software License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF

%install -p
sysjar install --buildroot %{buildroot} \
	--artifact jnr0104/jnr-constants.pom:jnr0104/jnr-constants.jar \
	--file-name jnr-constants-0.10.4 \
	--filelist .mfiles0104
# %{version} owns jnr-constants.sysjar. 0.10.4 keeps a second index file.
/bin/mv %{buildroot}/usr/share/sysjar/index/com.github.jnr/jnr-constants.sysjar \
	%{buildroot}/usr/share/sysjar/index/com.github.jnr/jnr-constants-0.10.4.sysjar
sed -i 's|/usr/share/sysjar/index/com.github.jnr/jnr-constants\.sysjar|/usr/share/sysjar/index/com.github.jnr/jnr-constants-0.10.4.sysjar|' .mfiles0104

%install -a
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles0104

%check -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > JnrSmoke.java << 'EOF'
import jnr.constants.platform.Errno;
public class JnrSmoke {
	public static void main(String[] args) {
		int v = Errno.ENOENT.intValue();
		if (v != 2 || Errno.ENOENT.longValue() != 2L || !Errno.ENOENT.defined()) {
			throw new AssertionError("enoent=" + v);
		}
		System.out.println(args[0] + " " + v);
	}
}
EOF
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/jnr-constants.jar -d . JnrSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/jnr-constants.jar:." JnrSmoke jnr0114_ok > check0114.log
cat check0114.log
grep -F -q 'jnr0114_ok 2' check0114.log
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/jnr-constants-0.10.4.jar -d . JnrSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/jnr-constants-0.10.4.jar:." JnrSmoke jnr0104_ok > check0104.log
cat check0104.log
grep -F -q 'jnr0104_ok 2' check0104.log

%files -f .mfiles
%doc LICENSE README.md
