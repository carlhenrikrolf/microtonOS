TARGET_PATH="/lib/systemd/system/"
SOURCE_PATH="/home/pi/Scripts/systemd"
for FILE in "$SOURCE_PATH"/*; do
	if [ -f "$FILE" ]; then
		FILENAME=$(basename "$FILE")
		echo "Stop $FILENAME"
		systemctl stop $FILENAME
		echo "Disable $FILENAME"
		systemctl disable $FILENAME
		echo "Copy $FILENAME"
		cp -f "$FILE" "$TARGET_PATH/"
		echo "Enable $FILENAME"
		systemctl enable $FILENAME
		echo "Reload"
		systemctl daemon-reload
		echo "Start $FILENAME"
		systemctl start $FILENAME
	fi
done
echo "Done"
