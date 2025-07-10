import subprocess

def run_stage(script_name, args=None):
    cmd = ["python", script_name]
    if args:
        cmd.extend(args)
    print(f"Запускаем: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Ошибки:", result.stderr)

def main():
    run_stage("Yolo_obr.py")   # Этап 2
    run_stage("SeemPy.py")     # Этап 3
    run_stage("Ready.py")      # Этап 4
    run_stage("bert_on.py")    # Этап 6

if __name__ == "__main__":
    main()
