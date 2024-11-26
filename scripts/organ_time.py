import subprocess
import time
from utils import handle_terminations
cmd = ['/usr/bin/setBfree']
done = 'All systems go. press CTRL-C, or send SIGINT or SIGHUP to terminate'
process = subprocess.Popen(
	cmd,
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT,
)
handle_terminations(process)
start = time.perf_counter_ns()
for line in iter(process.stdout.readline, b''):
	if done in line.decode() or time.perf_counter_ns() - start > 5e9:
		break
print('DONE: Organ took', (time.perf_counter_ns() - start)/1e9, 'seconds to load')
process.stdin = None
process.stdout = None
process.terminate()
