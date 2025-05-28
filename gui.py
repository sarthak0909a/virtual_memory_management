import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from fifo import FIFOPageReplacement
from lru import LRUPageReplacement
from optimal import OptimalPageReplacement
from comparison_chart import plot_comparison


class StepByStepWindow(tk.Toplevel):
    def __init__(self, master, ref_str, frames, log):
        super().__init__(master)
        self.title("Step-by-Step Simulation")
        self.geometry("700x500")

        self.ref_str = ref_str
        self.frames = frames
        self.log = log
        self.current_step = 0
        self.auto_playing = False

        self.label_step = tk.Label(self, text="")
        self.label_step.pack(pady=5)

        self.label_page = tk.Label(self, text="", font=("Arial", 16))
        self.label_page.pack(pady=5)

        self.label_status = tk.Label(self, text="", font=("Arial", 14))
        self.label_status.pack(pady=5)

        cols = [f"Frame {i+1}" for i in range(frames)]
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=1)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=80)
        self.tree.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.btn_prev = tk.Button(btn_frame, text="Previous", command=self.prev_step)
        self.btn_prev.grid(row=0, column=0, padx=5)

        self.btn_next = tk.Button(btn_frame, text="Next", command=self.next_step)
        self.btn_next.grid(row=0, column=1, padx=5)

        self.btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset_steps)
        self.btn_reset.grid(row=0, column=2, padx=5)

        self.btn_auto = tk.Button(btn_frame, text="Auto Play", command=self.auto_play)
        self.btn_auto.grid(row=0, column=3, padx=5)

        self.btn_stop = tk.Button(btn_frame, text="Stop", command=self.stop_auto_play)
        self.btn_stop.grid(row=0, column=4, padx=5)
        self.btn_stop.config(state=tk.DISABLED)

        self.btn_1 = tk.Button(btn_frame, text="+1", command=lambda: self.step_forward(1))
        self.btn_1.grid(row=1, column=0, padx=5)

        self.btn_2 = tk.Button(btn_frame, text="+2", command=lambda: self.step_forward(2))
        self.btn_2.grid(row=1, column=1, padx=5)

        self.btn_5 = tk.Button(btn_frame, text="+5", command=lambda: self.step_forward(5))
        self.btn_5.grid(row=1, column=2, padx=5)

        self.update_step()

    def update_step(self):
        if self.current_step < 0:
            self.current_step = 0
        if self.current_step >= len(self.log):
            self.current_step = len(self.log) - 1

        entry = self.log[self.current_step]

        # Determine status
        if "Hit:" in entry:
            status = "Hit"
        elif "Miss:" in entry:
            status = "Miss"
        else:
            status = "N/A"

        # Extract page number
        try:
            if "Hit:" in entry:
                page = int(entry.split("Hit:")[1].split("|")[0].strip())
            elif "Miss:" in entry:
                page = int(entry.split("Miss:")[1].split("|")[0].strip())
            else:
                page = "?"
        except Exception:
            page = "?"

        # Extract memory/frame content
        try:
            mem_str = entry.split("Memory:")[1].strip()
            frames_content = mem_str.strip("[]").split(",")
            frames_content = [f.strip() if f.strip() else "-" for f in frames_content]
            while len(frames_content) < self.frames:
                frames_content.append("-")
        except Exception:
            frames_content = ["-"] * self.frames

        # Update GUI elements
        self.label_step.config(text=f"Step {self.current_step + 1} of {len(self.log)}")
        self.label_page.config(text=f"Accessed Page: {page}")
        self.label_status.config(text=f"Status: {status}")

        for i in self.tree.get_children():
            self.tree.delete(i)
        self.tree.insert("", "end", values=frames_content)

        self.btn_prev.config(state=tk.NORMAL if self.current_step > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_step < len(self.log) - 1 else tk.DISABLED)

    def next_step(self):
        if self.current_step < len(self.log) - 1:
            self.current_step += 1
            self.update_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()

    def reset_steps(self):
        self.stop_auto_play()
        self.current_step = 0
        self.update_step()

    def step_forward(self, n):
        self.stop_auto_play()
        self.current_step = min(self.current_step + n, len(self.log) - 1)
        self.update_step()

    def auto_play(self):
        if self.auto_playing:
            return
        self.auto_playing = True
        self.btn_auto.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)

        def step():
            if not self.auto_playing:
                return
            if self.current_step < len(self.log) - 1:
                self.current_step += 1
                self.update_step()
                self.auto_after_id = self.after(800, step)
            else:
                self.stop_auto_play()

        step()

    def stop_auto_play(self):
        self.auto_playing = False
        self.btn_auto.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        if hasattr(self, 'auto_after_id'):
            self.after_cancel(self.auto_after_id)


def recommend_best_policy(reference_string, num_frames):
    results = {}

    fifo = FIFOPageReplacement(num_frames)
    fifo_faults, fifo_hits = fifo.run(reference_string, simulate_only=True)
    results["FIFO"] = {'faults': fifo_faults, 'hits': fifo_hits}

    lru = LRUPageReplacement(num_frames)
    lru_faults, lru_hits = lru.run(reference_string, simulate_only=True)
    results["LRU"] = {'faults': lru_faults, 'hits': lru_hits}

    optimal = OptimalPageReplacement(num_frames)
    optimal_faults, optimal_hits = optimal.run(reference_string, simulate_only=True)
    results["Optimal"] = {'faults': optimal_faults, 'hits': optimal_hits}

    best = min(results, key=lambda k: results[k]['faults'])
    return best, results


def show_results_table(results):
    table_window = tk.Toplevel()
    table_window.title("Comparison Table: Page Faults and Hits")
    table_window.geometry("500x300")

    columns = ("Algorithm", "Page Faults", "Page Hits")
    tree = ttk.Treeview(table_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=150)

    for algo, data in results.items():
        tree.insert("", tk.END, values=(algo, data['faults'], data['hits']))

    tree.pack(expand=True, fill='both')

    scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")


def simulate():
    try:
        frames = int(entry_frames.get())
        max_virt_mem = int(entry_max_virtual.get())
        ref_str = list(map(int, entry_ref.get().strip().split()))
        algo = combo_algo.get()

        if algo not in ["FIFO", "LRU", "Optimal"]:
            raise ValueError("Select a valid algorithm")

        if len(ref_str) > max_virt_mem:
            messagebox.showwarning(
                "Virtual Memory Limit Exceeded",
                f"Reference string truncated to maximum virtual memory limit of {max_virt_mem} pages."
            )
            ref_str = ref_str[:max_virt_mem]

        if algo == "FIFO":
            obj = FIFOPageReplacement(frames)
        elif algo == "LRU":
            obj = LRUPageReplacement(frames)
        elif algo == "Optimal":
            obj = OptimalPageReplacement(frames)

        log, faults, hits = obj.run(ref_str, simulate_only=False)
        best_algo, all_results = recommend_best_policy(ref_str, frames)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Algorithm: {algo}\n\n")
        result_text.insert(tk.END, "\n".join(log))
        result_text.insert(tk.END, f"\n\nPage Faults: {faults}, Page Hits: {hits}")
        result_text.insert(tk.END, f"\n\nRecommended: {best_algo} (fewest faults: {all_results[best_algo]['faults']})")

        plot_comparison(all_results)
        show_results_table(all_results)

        StepByStepWindow(app, ref_str, frames, log)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_trace_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            selected_type = access_type.get()
            reference_string = []
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 2:
                        op, page = parts[0], int(parts[1])
                        if selected_type == "All" or op == selected_type:
                            reference_string.append(page)
            if reference_string:
                entry_ref.delete(0, tk.END)
                entry_ref.insert(0, " ".join(map(str, reference_string)))
                messagebox.showinfo("Success", f"Loaded {len(reference_string)} references from file.")
            else:
                messagebox.showwarning("No Data", f"No entries found for access type '{selected_type}' in the file.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load trace file: {str(e)}")


# GUI Setup
app = tk.Tk()
app.title("Page Replacement Simulator")
app.geometry("750x750")

tk.Label(app, text="Number of Frames:").pack()
entry_frames = tk.Entry(app)
entry_frames.pack()

tk.Label(app, text="Maximum Virtual Memory Size (max pages):").pack()
entry_max_virtual = tk.Entry(app)
entry_max_virtual.insert(0, "1000")
entry_max_virtual.pack()

tk.Label(app, text="Reference String (space-separated):").pack()
entry_ref = tk.Entry(app, width=70)
entry_ref.pack()

access_type = tk.StringVar(value="All")
tk.Label(app, text="Filter Access Type:").pack()
ttk.Combobox(app, textvariable=access_type, values=["All", "R", "I"]).pack()

tk.Button(app, text="Load Reference String from Trace File", command=load_trace_file).pack(pady=5)

tk.Label(app, text="Choose Algorithm:").pack()
combo_algo = ttk.Combobox(app, values=["FIFO", "LRU", "Optimal"])
combo_algo.pack()

tk.Button(app, text="Simulate", command=simulate).pack(pady=10)

result_text = tk.Text(app, height=25, width=80)
result_text.pack()

app.mainloop()
