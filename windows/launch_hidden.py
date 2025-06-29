"""
Silent launcher stub for WebUI Assistant.
Starts the bundled EXE; splash UI handles visibility.
"""
import subprocess, sys, os

def main():
	exe_path = sys.executable if getattr(sys,'frozen',False) else os.path.join(os.path.dirname(__file__),'WebUI_Assistant.exe')
	subprocess.Popen([exe_path])

if __name__ == '__main__':
	main()
