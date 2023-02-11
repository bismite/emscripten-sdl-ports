#!/bin/bash

EMDIR=`which emcc`
EMDIR=`dirname "${EMDIR}"`
# echo ${EMDIR}

PORTS_DIR="${EMDIR}/tools/ports/"
# echo ${PORTS_DIR}
# ls -l ${PORTS_DIR}/sdl2.py ${PORTS_DIR}/sdl2_image.py ${PORTS_DIR}/sdl2_mixer.py

echo "copy to ${PORTS_DIR}"
cp sdl2_image.py sdl2_mixer.py sdl2.py "${PORTS_DIR}"
# ls -l ${PORTS_DIR}/sdl2.py ${PORTS_DIR}/sdl2_image.py ${PORTS_DIR}/sdl2_mixer.py
