#!/bin/bash

mkdir -p build

# emcc --clear-ports

emcc -Wall -std=c11 -O2 test.c -o build/test.html \
  -sUSE_SDL=2 \
  -sUSE_SDL_IMAGE=2 -sSDL2_IMAGE_FORMATS='["png","jpg"]' \
  -sUSE_SDL_MIXER=2 -sSDL2_MIXER_FORMATS='["mp3","ogg"]' \
  -sMAX_WEBGL_VERSION=2 \
  -sWASM=1 -sALLOW_MEMORY_GROWTH=1 --preload-file assets@assets
