import tkinter as tk
from tkinter import ttk


class ItemSelectionDialog:
    
    def __init__(self, parent, title, items):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._build_ui(items)
        
        # Wait for result
        self.dialog.wait_window()
    
    def _build_ui(self, items):
        """Build the dialog UI"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame, text="Select item to remove:").pack(pady=(0, 10))
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add items to listbox
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Remove", command=self._ok_clicked).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self._cancel_clicked).pack(side=tk.RIGHT)
        
        # Bind double-click to OK
        self.listbox.bind("<Double-Button-1>", lambda e: self._ok_clicked())
    
    def _ok_clicked(self):
        """Handle OK button click"""
        selection = self.listbox.curselection()
        if selection:
            self.result = self.listbox.get(selection[0])
        self.dialog.destroy()
    
    def _cancel_clicked(self):
        """Handle Cancel button click"""
        self.dialog.destroy()