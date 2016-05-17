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
JENA_BASE = 'org.apache.jena:jena-base:jar:3.1.0'
JENA_CORE = 'org.apache.jena:jena-core:jar:3.1.0'
JENA_ARQ = 'org.apache.jena:jena-arq:jar:3.1.0'
JENA_TDB = 'org.apache.jena:jena-tdb:jar:3.1.0'
JENA_IRI = 'org.apache.jena:jena-iri:jar:3.1.0'
JENA_GUAVA = 'org.apache.jena:jena-shaded-guava:jar:3.1.0'
XERCES = 'xerces:xercesImpl:jar:2.11.0'
XML = 'xml-apis:xml-apis:jar:1.4.01'
JENA_DEPS = [XERCES, XML, JENA_GUAVA]
JENA = [JENA_BASE, JENA_CORE, JENA_ARQ, JENA_TDB, JENA_IRI, JENA_DEPS]

LOG4J = 'log4j:log4j:jar:1.2.17'
LOG4J_12_API = 'org.apache.logging.log4j:log4j-1.2-api:jar:2.4.1'
LOG4J_API = 'org.apache.logging.log4j:log4j-api:jar:2.4.1'
LOG4J_CORE = 'org.apache.logging.log4j:log4j-core:jar:2.4.1'
SLF4J_API = 'org.slf4j:slf4j-api:jar:1.7.13'
SLF4J_NOP = 'org.slf4j:slf4j-nop:jar:1.7.13'
LOGGING = [LOG4J, LOG4J_12_API, LOG4J_API, LOG4J_CORE, SLF4J_API, SLF4J_NOP]

ST4 = 'org.antlr:ST4:jar:4.0.8'
TROVE = 'net.sf.trove4j:trove4j:jar:3.0.3'
COMMONS_LANG = 'org.apache.commons:commons-lang3:jar:3.4'
ANTLR = 'org.antlr:antlr4-runtime:jar:4.5.3'
REGGIE_DEPS = [ST4, TROVE, COMMONS_LANG, ANTLR]

DEPS = [JENA, LOGGING, REGGIE_DEPS]
artifacts(DEPS).each(&:invoke)

# Project layout
layout = Layout.new
layout[:source, :main, :java] = 'src'
layout[:source, :test, :java] = 'test'
layout[:source, :main, :resources] = 'resources'
layout[:source, :test, :resources] = 'test'
layout[:target, :main, :classes] = 'build'

def create_lib
  puts 'Pulling dependencies into lib/.'
  FileUtils.rm_rf 'lib'
  FileUtils.mkdir_p 'lib'
  artifacts(DEPS).each { |x|
    FileUtils.cp x.to_s, 'lib'
  }
end

def have_libs
  return false unless File.directory? 'lib'
  libtime = File::Stat.new('lib')
  btime = File::Stat.new(__FILE__)
  if libtime.ctime < btime.ctime
    puts 'Dependencies out-of-date.'
    return false
  end
  return true
end

create_lib unless have_libs
LIB_JARS = *Dir.glob(File.join('lib', '**', '*.jar'))

define 'bel-resource-generator', :layout => layout do
  project.version = VERSION_NUMBER
  project.group = GROUP
  run.using :main=>'org.openbel.reggie.rdf.generate.namespaces.Main'
  compile.with LIB_JARS

  package do
    Dir.glob(File.join('lib', '**', '*.jar')).each { |x|
      puts x
      unzip(x)
    }
  end
end
# vim:ts=2:sw=2
