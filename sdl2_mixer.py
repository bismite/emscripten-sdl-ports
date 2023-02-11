# Copyright 2016 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging

TAG = 'release-2.6.3'
HASH = 'ff8482975e927897c2ee934af836874438edeef412cf2c7d883b677708ddbf86cc97a7283b1c74c82574bfc08fb18b48e7faae08e750c81abc4278865b7f1c99'

deps = ['sdl2']
variants = {
  'sdl2_mixer_mp3': {'SDL2_MIXER_FORMATS': ["mp3"]},
  'sdl2_mixer_none': {'SDL2_MIXER_FORMATS': []},
}


def needed(settings):
  return settings.USE_SDL_MIXER == 2


def get_lib_name(settings):
  settings.SDL2_MIXER_FORMATS.sort()
  formats = '-'.join(settings.SDL2_MIXER_FORMATS)

  libname = 'libSDL2_mixer'
  if formats != '':
    libname += '_' + formats
  libname += '.a'

  return libname


def get(ports, settings, shared):
  sdl_build = os.path.join(ports.get_build_dir(), 'sdl2')
  assert os.path.exists(sdl_build), 'You must use SDL2 to use SDL2_mixer'
  ports.fetch_project('sdl2_mixer', f'https://github.com/libsdl-org/SDL_mixer/archive/refs/tags/{TAG}.zip', sha512hash=HASH)
  libname = get_lib_name(settings)

  def create(final):
    logging.info('building port: sdl2_mixer')

    source_path = os.path.join(ports.get_dir(), 'sdl2_mixer', 'SDL_mixer-' + TAG)
    src_path = os.path.join(source_path, 'src')
    include_path = os.path.join(source_path, 'include')
    ports.install_headers(include_path, target='SDL2')

    flags = [
      '-sUSE_SDL=2',
      '-O2',
      '-DMUSIC_WAV',
    ]

    if "ogg" in settings.SDL2_MIXER_FORMATS:
      flags += [
        '-DMUSIC_OGG',
        '-DOGG_USE_STB',
      ]

    if "mp3" in settings.SDL2_MIXER_FORMATS:
      flags += [
        '-DMUSIC_MP3_DRMP3',
      ]

    srcs = []
    src_c = 'effect_position.c effect_stereoreverse.c effects_internal.c mixer.c music.c utils.c'.split()
    for i in src_c:
      srcs += [os.path.join(src_path,i)]

    src_codecs_c = '''load_aiff.c mp3utils.c music_drflac.c music_flac.c music_modplug.c music_nativemidi.c music_ogg_stb.c music_timidity.c music_xmp.c
    load_voc.c music_cmd.c music_drmp3.c music_fluidsynth.c music_mpg123.c music_ogg.c music_opus.c music_wav.c'''.split()
    for i in src_codecs_c:
      srcs += [os.path.join(src_path,"codecs",i)]

    includes = [
      src_path,
      os.path.join(src_path, 'codecs'),
    ]

    build_dir = ports.clear_project_build('sdl2_mixer')

    ports.build_port(
      source_path,
      final,
      build_dir,
      includes=includes,
      flags=flags,
      srcs=srcs
    )

  return [shared.cache.get_lib(libname, create, what='port')]


def clear(ports, settings, shared):
  shared.cache.erase_lib(get_lib_name(settings))


def process_dependencies(settings):
  settings.USE_SDL = 2

def process_args(ports):
  return []


def show():
  return 'SDL2_mixer (USE_SDL_MIXER=2; zlib license)'
