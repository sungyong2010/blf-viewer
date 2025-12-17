'''
python -m PyInstaller --onefile --noconsole --name="BLF_Viewer" blf-viewer.py
'''
import can
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

# 파일 선택 대화상자 열기
root = tk.Tk()
root.withdraw()  # 메인 윈도우 숨기기

log_file = filedialog.askopenfilename(
    title="BLF 파일 선택 - by shaun.hong@lge.com",
    filetypes=[("BLF files", "*.blf"), ("All files", "*")]
)

if not log_file:
    messagebox.showinfo("알림", "파일이 선택되지 않았습니다.")
    exit()

# 진행 상황 창 생성
progress_window = tk.Toplevel(root)
progress_window.title("BLF 파일 변환 중...")
progress_window.geometry("400x150")
progress_window.resizable(False, False)

# 중앙에 위치
progress_window.update_idletasks()
x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
progress_window.geometry(f"400x150+{x}+{y}")

# 레이블
label = tk.Label(progress_window, text=f"파일 변환 중...\n{log_file}", wraplength=380)
label.pack(pady=20)

# 진행률 표시
progress_label = tk.Label(progress_window, text="0 메시지 처리됨")
progress_label.pack(pady=5)

# 진행바
progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=350)
progress_bar.pack(pady=10)
progress_bar.start(10)

progress_window.update()

# 출력 파일명 생성 (확장자를 .log로 변경)
output_file = os.path.splitext(log_file)[0] + ".log"

print(f"로그 파일로 저장 중: {output_file}\n")

with can.BLFReader(log_file) as log, open(output_file, 'w', encoding='utf-8') as f:
    # 헤더 작성
    header = f"{'Time':<15} {'Channel':<10} {'ID':<10} {'Type':<15} {'Dir':<5} {'DLC':<5} {'Data':<50}"
    f.write(header + "\n")
    f.write("-" * 110 + "\n")
    
    start_time = None  # 첫 메시지의 시간을 저장
    msg_count = 0
    
    for msg in log:
        msg_count += 1
        
        # 100개마다 진행 상황 업데이트
        if msg_count % 100 == 0:
            progress_label.config(text=f"{msg_count} 메시지 처리됨")
            progress_window.update()
        # 첫 메시지의 시간을 기준으로 설정
        if start_time is None:
            start_time = msg.timestamp
        
        # 상대 시간 계산 (시작 시간 기준)
        relative_time = msg.timestamp - start_time
        
        # 시간 포맷 (시:분:초.마이크로초)
        hours = int(relative_time // 3600)
        minutes = int((relative_time % 3600) // 60)
        seconds = relative_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
        
        # 채널 정보
        channel = f"CAN {msg.channel}" if hasattr(msg, 'channel') else "CAN 1"
        
        # ID (16진수)
        id_str = f"{msg.arbitration_id:03X}{'x' if msg.is_extended_id else ''}"
        
        # CAN FD 여부
        frame_type = "CAN FD Frame" if msg.is_fd else "CAN Frame"
        
        # 방향 (Rx/Tx)
        direction = "Tx" if msg.is_rx == False else "Rx"
        
        # DLC (Data Length Code)
        dlc = len(msg.data)
        
        # Data (16진수, 공백으로 구분)
        data_str = ' '.join(f"{b:02X}" for b in msg.data)
        
        # 출력 라인 생성
        line = f"{time_str:<15} {channel:<10} {id_str:<10} {frame_type:<15} {direction:<5} {dlc:<5} {data_str:<50}"
        f.write(line + "\n")

# 진행 창 닫기
progress_window.destroy()

# 완료 커스텀 팝업
def open_log_file():
    try:
        os.startfile(output_file)  # Windows에서 기본 프로그램으로 파일 열기
    except Exception as e:
        messagebox.showerror("오류", f"파일을 열 수 없습니다:\n{e}")

# root는 계속 숨김 상태 유지 (root.deiconify() 제거)

popup = tk.Toplevel(root)
popup.title("완료")
popup.geometry("400x200")
popup.resizable(False, False)

# 중앙에 위치
popup.update_idletasks()
x = (popup.winfo_screenwidth() // 2) - (400 // 2)
y = (popup.winfo_screenheight() // 2) - (200 // 2)
popup.geometry(f"400x200+{x}+{y}")

msg = tk.Label(popup, text=f"변환 완료!\n\n총 {msg_count}개의 메시지 처리됨\n\n저장 위치:\n{output_file}", wraplength=380)
msg.pack(pady=20)

open_btn = tk.Button(popup, text="Open", command=open_log_file, width=10)
open_btn.pack(pady=5)

def close_app():
    popup.destroy()
    root.quit()  # destroy 대신 quit 사용

close_btn = tk.Button(popup, text="닫기", command=close_app, width=10)
close_btn.pack(pady=5)

# popup.transient(root) 제거 - root가 숨겨져 있어서 팝업도 안 보임
popup.grab_set()
popup.focus_force()  # 팝업에 포커스 강제 설정
root.wait_window(popup)

root.destroy()
