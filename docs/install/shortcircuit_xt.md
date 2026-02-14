# Shortcircuit still does not work

Dependencies
```bash
sudo apt install libgtkmm-3.0-dev
```

The repo is [here](https://github.com/surge-synthesizer/shortcircuit-xt?tab=readme-ov-file)
```bash
git clone <this repo or your fork>
cd shortcircuit-xt
git submodule update --init --recursive
cmake -Bignore/build -DCMAKE_BUILD_TYPE=Release
cmake --build ignore/build --config Release --target shortcircuit-products
```

The errors:
- "x86intrin.h" does not exist
- "cpuid.h" does not exist