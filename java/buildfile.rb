# Build settings
settings = Buildr.settings.build
# Build options
options = Buildr.options

# Disables testing (i.e., defer to a build server)
# options.test = false

# Convenient tasks
# buildr cp -> buildr clean package
task :cp => [:clean, :package]
# buildr p -> buildr package
task :p  => [:package]
# buildr c -> buildr clean
task :c  => [:clean]

# Version number for this release
VERSION_NUMBER = '0.1'
# Group identifier for your projects
GROUP = 'org.openbel.reggie'

# Maven 2.0 remote repositories
repositories.remote << 'http://repo1.maven.org/maven2'
repositories.remote << 'http://www.ibiblio.org/maven2'

# Dependencies
JENA_CORE = 'org.apache.jena:jena-core:jar:3.0.0'
JENA_ARQ = 'org.apache.jena:jena-arq:jar:3.0.0'
JENA_TDB = 'org.apache.jena:jena-tdb:jar:3.0.0'
JENA_BASE = 'org.apache.jena:jena-base:jar:3.0.0'
JENA = [JENA_BASE, JENA_CORE, JENA_ARQ, JENA_TDB, 'xerces:xercesImpl:jar:2.11.0', 'xml-apis:xml-apis:jar:1.4.01', 'org.apache.jena:jena-shaded-guava:jar:3.0.0', 'org.apache.jena:jena-iri:jar:3.0.0']
ST4 = 'org.antlr:ST4:jar:4.0.8'
LOG4J = ['org.apache.logging.log4j:log4j-1.2-api:jar:2.4.1', 'log4j:log4j:jar:1.2.17', 'org.apache.logging.log4j:log4j-core:jar:2.4.1', 'org.apache.logging.log4j:log4j-api:jar:2.4.1', 'org.slf4j:slf4j-api:jar:1.7.13']
TROVE = 'net.sf.trove4j:trove4j:jar:3.0.3'
COMMONS_LANG = 'org.apache.commons:commons-lang3:jar:3.3.2'
ANTLR = 'org.antlr:antlr-runtime:jar:3.5.1'

# Project layout
layout = Layout.new
layout[:source, :main, :java] = 'src'
layout[:source, :test, :java] = 'test'
layout[:source, :main, :resources] = 'resources'
layout[:source, :test, :resources] = 'test'
layout[:target, :main, :classes] = 'build'

define 'bel-resource-generator', :layout => layout do
  project.version = VERSION_NUMBER
  project.group = GROUP
  package :jar

  run.using :main=>'org.openbel.reggie.rdf.generate.namespaces.Main'

  compile.with JENA, LOG4J, ST4, TROVE, COMMONS_LANG, ANTLR

end

# vim:ts=2:sw=2
