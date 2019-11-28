patch -p0 < patch-1.patch
cd node_modules/pouch-vue/
npm i rollup-plugin-commonjs
npm i rollup-plugin-node-resolve
npm i rollup-plugin-json
npm i rollup-plugin-buble
npm i rollup-plugin-replace
rollup -c
