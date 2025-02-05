# Librespot

As a bonus, you can install librespot for playing Spotify content from the Raspberry Pi.
Of course, this can also be achieved through bluetooth, but the playback quality over bluetooth can be lacking especially with several devices connected simultaneously.

Start by installing the package manager [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html).
```bash
curl https://sh.rustup.rs -sSf | sh
```

Install librespot with the JACK backend.
```bash
cargo install librespot --features jackaudio-backend
```

Create a directory for storing the credentials from the Spotify account.
Note that git will not track this directory.
Then run the wrapper script.
The terminal should provide you with a link to a webpage to register your credentials.
```bash
mkdir /home/pi/microtonOS/config/.librespot
/home/pi/.venv/bin/python3 /home/pi/microtonOS/src/wrappers/librespot.py
```