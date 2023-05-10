from io import StringIO
import contextlib
import sys

def run_script(script):
    # Redirect stdout
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    
    # Execute script
    with contextlib.redirect_stderr(redirected_output):
        try:
            exec(str(script))
        except Exception as e:
            print(e)
    
    # Restore stdout and return output
    sys.stdout = old_stdout
    return redirected_output.getvalue()
