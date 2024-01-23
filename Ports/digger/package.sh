#!/usr/bin/env -S bash ../.port_include.sh
port='digger'
version='b72f36a224d670a0ac1eeba11bc944c8bc835066'
useconfigure='true'
files=(
    "https://github.com/sobomax/digger/archive/${version}.tar.gz#864efaa38c90cf11dcda096f4dac89c0225b33696bafb6b8006a7da2614a33a5"
)
configopts=(
    '-DCMAKE_BUILD_TYPE=release'
    "-DCMAKE_TOOLCHAIN_FILE=${SERENITY_BUILD_DIR}/CMakeToolchain.txt"
)
depends=(
    'SDL2'
    'zlib'
)

launcher_name='Digger Reloaded'
launcher_category='Games'
launcher_command='/usr/local/bin/digger'

configure() {
    run cmake "${configopts[@]}" .
}

install() {
    run /usr/bin/install -Dm755 digger "${SERENITY_INSTALL_ROOT}/usr/local/bin/digger"
}
