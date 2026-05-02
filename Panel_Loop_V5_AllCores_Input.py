import os, time, threading, subprocess, tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import messagebox

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
GAMELOOP_PATHS = [
r"C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe",
r"C:\Program Files\TxGameAssistant\ui\AppMarket.exe",
r"C:\Program Files\TxGameAssistant\AndroidEmulatorEx.exe",
r"C:\Program Files\GameLoop\Launcher.exe",
r"D:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe",
r"D:\TxGameAssistant\AppMarket\AppMarket.exe"]
PROCESSES=["AndroidEmulatorEx","AndroidEmulator","aow_exe","AppMarket","ProjectTitan","AndroidRender"]
SAFE_JUNK=["XboxGameBar","GameBar","Widgets","OneDrive","YourPhone","PhoneExperienceHost"]

def run_ps(cmd, timeout=25):
    try:
        subprocess.run(["powershell","-NoProfile","-ExecutionPolicy","Bypass","-WindowStyle","Hidden","-Command",cmd],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout, creationflags=CREATE_NO_WINDOW)
        return True
    except:
        return False

def find_gameloop():
    for p in GAMELOOP_PATHS:
        if Path(p).exists(): return p
    return None

def gameloop_running():
    try:
        out=subprocess.check_output(["tasklist"],creationflags=CREATE_NO_WINDOW,stderr=subprocess.DEVNULL).decode(errors="ignore")
        return any(x+".exe" in out for x in ["AndroidEmulatorEx","aow_exe","AppMarket"])
    except:
        return False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PANEL LOOP V5 ALL CORES + INPUT")
        self.geometry("900x620")
        self.configure(bg="#07090d")
        self.running=False
        self.loop_seconds=5
        self.mask=65534
        self.core_text="CPU 1-15"
        self.build_ui()
        self.log("V5 All Cores + Input loaded.")
        self.log("Best flow: PRE-GAME CLEAN → MOUSE & KEYBOARD BOOST → SMART START.")

    def build_ui(self):
        header=tk.Frame(self,bg="#07090d",height=115); header.pack(fill="x")
        tk.Label(header,text="PANEL LOOP V5 ALL CORES + INPUT",fg="#00ffd5",bg="#07090d",font=("Consolas",24,"bold")).place(x=20,y=18)
        self.engine_label=tk.Label(header,text="ENGINE: OFF",fg="#ffdf5d",bg="#07090d",font=("Consolas",13,"bold")); self.engine_label.place(x=700,y=45)
        tk.Frame(self,bg="#00ffd5",height=2).pack(fill="x")
        body=tk.Frame(self,bg="#07090d"); body.pack(fill="both",expand=True,padx=15,pady=15)
        left=tk.Frame(body,bg="#07090d",width=290); left.pack(side="left",fill="y")
        self.btn(left,"🚀 SMART START","#31ff47",self.smart_start)
        self.btn(left,"🔥 ALL CORES MODE","#00ffd5",self.all_cores_mode)
        self.btn(left,"⌨ MOUSE & KEYBOARD BOOST","#9b5cff",self.input_boost)
        self.btn(left,"🧼 PRE-GAME CLEAN","#ffdf5d",self.pre_game_clean)
        self.btn(left,"🎮 START GAMELOOP","#4aa3ff",self.start_gameloop)
        self.btn(left,"🔁 RE-APPLY NOW","#ffdf5d",self.apply_stability)
        self.btn(left,"🛑 STOP ENGINE","#ff4d6d",self.stop_engine)
        self.btn(left,"↩ RESTORE DEFAULTS","#aaaaaa",self.restore_defaults)
        right=tk.Frame(body,bg="#07090d"); right.pack(side="left",fill="both",expand=True,padx=(15,0))
        self.info=tk.Label(right,text="",fg="white",bg="#101217",font=("Consolas",12),justify="left",relief="solid",bd=1,padx=14,pady=12)
        self.info.pack(fill="x",pady=(0,12))
        self.log_box=tk.Text(right,bg="black",fg="#31ff47",insertbackground="#31ff47",font=("Consolas",10),relief="flat")
        self.log_box.pack(fill="both",expand=True)
        self.update_info()

    def btn(self,parent,text,color,cmd):
        tk.Button(parent,text=text,command=cmd,bg="#15191f",fg=color,activebackground="#232a33",activeforeground=color,relief="flat",anchor="w",padx=16,pady=12,font=("Consolas",10,"bold")).pack(fill="x",pady=5)

    def update_info(self):
        self.info.config(text=f"CPU MODE: {self.core_text}\nAFFINITY MASK: {self.mask}\nENGINE: {'ON' if self.running else 'OFF'}\nLOOP: every {self.loop_seconds}s\nGPU Preference: High Performance")

    def log(self,msg):
        self.log_box.insert("end",f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see("end")

    def power_mode(self):
        run_ps("powercfg /S SCHEME_MIN")
        self.log("Power plan set to High Performance.")

    def gpu_preference(self):
        for exe in dict.fromkeys(GAMELOOP_PATHS):
            run_ps(f"New-Item -Path 'HKCU:\\Software\\Microsoft\\DirectX\\UserGpuPreferences' -Force | Out-Null; New-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\DirectX\\UserGpuPreferences' -Name '{exe}' -Value 'GpuPreference=2;' -PropertyType String -Force | Out-Null")
        self.log("GPU preference set to High Performance.")

    def apply_stability(self):
        names=",".join([f"'{p}'" for p in PROCESSES])
        run_ps(f"$names=@({names}); foreach($n in $names){{ Get-Process -Name $n -ErrorAction SilentlyContinue | ForEach-Object {{ try {{ if($_.ProcessName -ne 'adb'){{$_.PriorityClass='High'}} }} catch {{}}; try {{ if($_.ProcessName -ne 'QMEmulatorService'){{$_.ProcessorAffinity={self.mask}}} }} catch {{}} }} }}")
        self.log(f"Applied High priority + {self.core_text}.")
        self.update_info()

    def all_cores_mode(self):
        self.mask=65534
        self.core_text="CPU 1-15"
        self.apply_stability()
        self.log("All Cores Mode active. CPU 0 stays free for Windows.")

    def input_boost(self):
        ps=r"""Set-ItemProperty -Path 'HKCU:\Control Panel\Keyboard' -Name 'KeyboardDelay' -Value 0
Set-ItemProperty -Path 'HKCU:\Control Panel\Keyboard' -Name 'KeyboardSpeed' -Value 31
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseSpeed' -Value 0
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseThreshold1' -Value 0
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseThreshold2' -Value 0
New-Item -Path 'HKCU:\Software\Microsoft\GameBar' -Force | Out-Null
New-ItemProperty -Path 'HKCU:\Software\Microsoft\GameBar' -Name 'AllowAutoGameMode' -Value 1 -PropertyType DWORD -Force | Out-Null"""
        run_ps(ps)
        self.log("Mouse & Keyboard Boost applied: acceleration OFF, fast keyboard, Game Mode ON.")

    def pre_game_clean(self):
        self.log("Pre-game clean started.")
        names=",".join([f"'{p}'" for p in SAFE_JUNK])
        run_ps(f"$names=@({names}); foreach($n in $names){{ Get-Process -Name $n -ErrorAction SilentlyContinue | ForEach-Object {{ try {{ Stop-Process -Id $_.Id -Force }} catch {{}} }} }}")
        run_ps("ipconfig /flushdns")
        self.log("Pre-game clean complete. DNS flushed and safe junk closed.")

    def engine_loop(self):
        while self.running:
            if gameloop_running():
                self.apply_stability()
            time.sleep(self.loop_seconds)

    def start_engine(self):
        if self.running:
            self.log("Engine already running."); return
        self.running=True
        self.engine_label.config(text="ENGINE: ON",fg="#31ff47")
        self.power_mode(); self.gpu_preference(); self.input_boost(); self.apply_stability()
        threading.Thread(target=self.engine_loop,daemon=True).start()
        self.log("Engine started. Keep tool open while playing.")
        self.update_info()

    def start_gameloop(self):
        path=find_gameloop()
        if not path:
            messagebox.showwarning("GameLoop not found","GameLoop was not found in default paths.")
            self.log("GameLoop not found.")
            return
        subprocess.Popen([path],creationflags=CREATE_NO_WINDOW)
        self.log(f"GameLoop started: {path}")
        self.after(6000,self.apply_stability)
        self.after(12000,self.apply_stability)
        self.after(22000,self.apply_stability)

    def smart_start(self):
        self.log("Smart Start running...")
        self.start_engine()
        self.start_gameloop()
        self.log("Smart Start complete.")

    def stop_engine(self):
        self.running=False
        self.engine_label.config(text="ENGINE: OFF",fg="#ffdf5d")
        self.log("Engine stopped.")
        self.update_info()

    def restore_defaults(self):
        if not messagebox.askyesno("Restore Defaults","Restore keyboard/mouse/power defaults?"): return
        self.stop_engine()
        ps=r"""Set-ItemProperty -Path 'HKCU:\Control Panel\Keyboard' -Name 'KeyboardDelay' -Value 1
Set-ItemProperty -Path 'HKCU:\Control Panel\Keyboard' -Name 'KeyboardSpeed' -Value 15
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseSpeed' -Value 1
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseThreshold1' -Value 6
Set-ItemProperty -Path 'HKCU:\Control Panel\Mouse' -Name 'MouseThreshold2' -Value 10
powercfg /S SCHEME_BALANCED"""
        run_ps(ps)
        self.log("Defaults restored. Restart recommended.")

if __name__=="__main__":
    App().mainloop()
