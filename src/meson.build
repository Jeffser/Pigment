pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'pigment'
gnome = import('gnome')

blueprints = files(
  'ui/preferences.blp',
  'ui/shortcuts.blp',
  'ui/window.blp'
)

blueprints = custom_target('blueprints',
  input: blueprints,
  output: '.',
  command: [
    find_program('blueprint-compiler', version: '>= 0.18.0'),
    'batch-compile',
    '@OUTPUT@',
    '@CURRENT_SOURCE_DIR@',
    '@INPUT@'
  ],
)

gnome.compile_resources(
  'pigment',
  'pigment.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
  source_dir: meson.current_source_dir(),
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'pigment.in',
  output: 'pigment',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

pigment_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'widgets.py'
]

install_data(pigment_sources, install_dir: moduledir)
