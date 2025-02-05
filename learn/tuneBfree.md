# tuneBfree
It is also possible to build a CLAP plugin.
```bash
sudo apt-get install libcairo2-dev
cd ~/microtonOS/third_party/tuneBfree/src
cmake -B build -D CLAP_GUI=true
cmake --build build
sudo cp build/tuneBfree.clap /usr/lib/clap
```