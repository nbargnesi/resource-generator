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
JENA = [JENA_CORE, JENA_ARQ, JENA_TDB]
ST4 = 'org.antlr:ST4:jar:4.0.8'
LOG4J = ['org.apache.logging.log4j:log4j-1.2-api:jar:2.4.1', 'log4j:log4j:jar:1.2.17']

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

  compile.with JENA, LOG4J, ST4
end

# vim:ts=2:sw=2
