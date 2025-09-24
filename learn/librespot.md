# Librespot

As a bonus, you can install librespot for playing Spotify content from the Raspberry Pi.
Of course, this can also be achieved through bluetooth, but the playback quality over bluetooth can be lacking especially with several devices connected simultaneously.

Start by installing the package manager [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html).
```bash
curl https://sh.rustup.rs -sSf | sh
```

Install librespot with the JACK backend.
```bash
cd ~/.cargo/bin/
./cargo install librespot --features jackaudio-backend
sudo cp librespot /usr/bin/
```
You need to specify where to store credentials and temporary data.
The wrapper script saves these in `~/microtonOS/tmp/`.
Note that git is set to ignore anything saved in the tmp directory apart from the `.gitignore` file.
You may have to repeat these steps if there is an update to spotify.