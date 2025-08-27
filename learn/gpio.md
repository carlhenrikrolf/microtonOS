For sytemd to work
```bash
sudo apt install rgpiod
```
Maybe that was not necessary, what solved it was to set a working directory in the systemctl file---a working directory where the user pi has write privileges.
```.service
WorkingDirectory=/home/pi/microtonOS/
```