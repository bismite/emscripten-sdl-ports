# Copyright 2014 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os

TAG = 'release-2.6.3'
HASH = 'f8759721702f81d147e15b54d0d9e6ef5cc8d6d15951f9d69fb88f9ce8f0ac3b4f3de4410fc0dea4c708af5b302bb5e1d1300e306369861fde8e95b7c9e98436'

deps = ['sdl2']
variants = {
  'sdl2_image_jpg':  {'SDL2_IMAGE_FORMATS': ["jpg"]},
  'sdl2_image_png': {'SDL2_IMAGE_FORMATS': ["png"]},
}


def needed(settings):
  return settings.USE_SDL_IMAGE == 2


def get_lib_name(settings):
  settings.SDL2_IMAGE_FORMATS.sort()
  formats = '-'.join(settings.SDL2_IMAGE_FORMATS)

  libname = 'libSDL2_image'
  if formats != '':
    libname += '_' + formats
  return libname + '.a'


def get(ports, settings, shared):
  sdl_build = os.path.join(ports.get_build_dir(), 'sdl2')
  assert os.path.exists(sdl_build), 'You must use SDL2 to use SDL2_image'
  ports.fetch_project('sdl2_image', f'https://github.com/libsdl-org/SDL_image/archive/refs/tags/{TAG}.zip', sha512hash=HASH)
  libname = get_lib_name(settings)

  def create(final):
    src_dir = os.path.join(ports.get_dir(), 'sdl2_image', 'SDL_image-' + TAG)
    ports.install_headers(src_dir, target='SDL2')
    srcs = '''IMG.c IMG_avif.c IMG_bmp.c IMG_gif.c IMG_jpg.c IMG_jxl.c IMG_lbm.c IMG_pcx.c IMG_png.c IMG_pnm.c IMG_qoi.c IMG_stb.c IMG_svg.c IMG_tga.c
              IMG_tif.c IMG_xcf.c IMG_xpm.c IMG_xv.c IMG_webp.c IMG_ImageIO.m'''.split()

    defs = ['-O2', '-sUSE_SDL=2', '-Wno-format-security']

    for fmt in settings.SDL2_IMAGE_FORMATS:
      defs.append('-DLOAD_' + fmt.upper())

    defs += ['-DUSE_STBIMAGE']

    ports.build_port(src_dir, final, 'sdl2_image', flags=defs, srcs=srcs)

  return [shared.cache.get_lib(libname, create, what='port')]


def clear(ports, settings, shared):
  shared.cache.erase_lib(get_lib_name(settings))


def process_dependencies(settings):
  settings.USE_SDL = 2

def process_args(ports):
  return []


def show():
  return 'SDL2_image (USE_SDL_IMAGE=2; zlib license)'
