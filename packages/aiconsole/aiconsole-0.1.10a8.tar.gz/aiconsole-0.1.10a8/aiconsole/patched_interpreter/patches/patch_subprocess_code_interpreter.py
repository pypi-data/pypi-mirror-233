"""

Added proces.pool check to fix hanging

"""

from ..code_interpreters.subprocess_code_interpreter import SubprocessCodeInterpreter
import queue
import time
import traceback


def run(self, code):
    retry_count = 0
    max_retries = 3

    # Setup
    try:
        code = self.preprocess_code(code)
        if not self.process:
            self.start_process()
    except:
        yield {"output": traceback.format_exc()}
        return

    while retry_count <= max_retries:
        if self.debug_mode:
            print(f"Running code:\n{code}\n---")

        self.done.clear()

        try:
            self.process.stdin.write(code + "\n")
            self.process.stdin.flush()
            break
        except:
            if retry_count != 0:
                # For UX, I like to hide this if it happens once. Obviously feels better to not see errors
                # Most of the time it doesn't matter, but we should figure out why it happens frequently with:
                # applescript
                yield {"output": traceback.format_exc()}
                yield {"output": f"Retrying... ({retry_count}/{max_retries})"}
                yield {"output": "Restarting process."}

            self.start_process()

            retry_count += 1
            if retry_count > max_retries:
                yield {"output": "Maximum retries reached. Could not execute code."}
                return

    while True:
        if not self.output_queue.empty():
            yield self.output_queue.get()
        else:
            time.sleep(0.1)
        try:
            output = self.output_queue.get(
                timeout=0.3)  # Waits for 0.3 seconds
            yield output
        except queue.Empty:
            # AIConsole Fix: Added proces.pool check to fix hanging
            if self.done.is_set() or (self.process and self.process.poll() is not None):
                # Try to yank 3 more times from it... maybe there's something in there...
                # (I don't know if this actually helps. Maybe we just need to yank 1 more time)

                for _ in range(3):
                    if not self.output_queue.empty():
                        yield self.output_queue.get()
                    time.sleep(0.2)
                break


SubprocessCodeInterpreter.run = run
