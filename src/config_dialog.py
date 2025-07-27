import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
from pathlib import Path


class ConfigDialog:
    """Dialog for saving and loading configurations with simplified UI"""
    
    def __init__(self, parent, settings_manager, mode="load"):
        self.parent = parent
        self.settings_manager = settings_manager
        self.mode = mode  # "load" or "save"
        self.result = None
        self.selected_config = None
        
        config_folder = settings_manager.get_config_folder()
        if not config_folder:
            messagebox.showerror(
                "No Configuration Folder",
                "Please set up a configuration folder in Settings first.",
                parent=parent
            )
            return
        
        self.config_folder = Path(config_folder)
        if not self.config_folder.exists():
            try:
                self.config_folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror(
                    "Folder Error",
                    f"Could not access configuration folder:\n{e}",
                    parent=parent
                )
                return
        
        self.create_dialog()
    
    def create_dialog(self):
        """Create the configuration dialog"""
        self.dialog = tk.Toplevel(self.parent)
        title = "Save Configuration" if self.mode == "save" else "Load Configuration"
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        self.refresh_config_list()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Create the dialog widgets"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_text = "Save Configuration As:" if self.mode == "save" else "Load Configuration:"
        title_label = tk.Label(main_frame, text=title_text, font=("Arial", 12, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Configuration list
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Listbox with scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.config_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.config_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.config_listbox.yview)
        
        # Bind double-click for load mode
        if self.mode == "load":
            self.config_listbox.bind("<Double-Button-1>", lambda e: self.load_config())
        else:
            self.config_listbox.bind("<Double-Button-1>", lambda e: self.select_for_overwrite())
        
        # Name entry for save mode
        if self.mode == "save":
            name_frame = tk.Frame(main_frame)
            name_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(name_frame, text="Configuration Name:").pack(anchor=tk.W)
            self.name_entry = tk.Entry(name_frame, font=("Arial", 10))
            self.name_entry.pack(fill=tk.X, pady=(5, 0))
            self.name_entry.focus()
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        if self.mode == "save":
            tk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.RIGHT, padx=(10, 0))
        else:
            tk.Button(button_frame, text="Load", command=self.load_config).pack(side=tk.RIGHT, padx=(10, 0))
            tk.Button(button_frame, text="Delete", command=self.delete_config).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(button_frame, text="Refresh", command=self.refresh_config_list).pack(side=tk.LEFT)
    
    def refresh_config_list(self):
        """Refresh the list of available configurations"""
        self.config_listbox.delete(0, tk.END)
        
        try:
            # Get all .json files in the config folder
            json_files = list(self.config_folder.glob("*.json"))
            json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)  # Sort by modification time
            
            for json_file in json_files:
                # Display name without .json extension
                display_name = json_file.stem
                
                # Add modification time
                mtime = json_file.stat().st_mtime
                import datetime
                mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
                
                self.config_listbox.insert(tk.END, f"{display_name} ({mod_time})")
            
            if not json_files:
                self.config_listbox.insert(tk.END, "No configurations found")
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not read configuration folder:\n{e}",
                parent=self.dialog
            )
    
    def get_selected_config_path(self):
        """Get the path of the selected configuration"""
        selection = self.config_listbox.curselection()
        if not selection:
            return None
        
        selected_text = self.config_listbox.get(selection[0])
        if selected_text == "No configurations found":
            return None
        
        # Extract the name (before the timestamp in parentheses)
        config_name = selected_text.split(" (")[0]
        return self.config_folder / f"{config_name}.json"
    
    def select_for_overwrite(self):
        """Select a configuration name for overwriting in save mode"""
        if self.mode != "save":
            return
        
        config_path = self.get_selected_config_path()
        if config_path:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, config_path.stem)
    
    def save_config(self):
        """Save the configuration"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a configuration name.", parent=self.dialog)
            return
        
        # Remove .json extension if user added it
        if name.lower().endswith('.json'):
            name = name[:-5]
        
        config_path = self.config_folder / f"{name}.json"
        
        # Check if file exists
        if config_path.exists():
            result = messagebox.askyesno(
                "Overwrite Configuration",
                f"Configuration '{name}' already exists.\nDo you want to overwrite it?",
                parent=self.dialog
            )
            if not result:
                return
        
        self.result = config_path
        self.settings_manager.set_last_config(config_path)
        self.dialog.destroy()
    
    def load_config(self):
        """Load the selected configuration"""
        config_path = self.get_selected_config_path()
        if not config_path:
            messagebox.showerror("Error", "Please select a configuration to load.", parent=self.dialog)
            return
        
        if not config_path.exists():
            messagebox.showerror("Error", "Selected configuration file does not exist.", parent=self.dialog)
            self.refresh_config_list()
            return
        
        self.result = config_path
        self.settings_manager.set_last_config(config_path)
        self.dialog.destroy()
    
    def delete_config(self):
        """Delete the selected configuration"""
        config_path = self.get_selected_config_path()
        if not config_path:
            messagebox.showerror("Error", "Please select a configuration to delete.", parent=self.dialog)
            return
        
        result = messagebox.askyesno(
            "Delete Configuration",
            f"Are you sure you want to delete '{config_path.stem}'?\nThis cannot be undone.",
            parent=self.dialog
        )
        
        if result:
            try:
                config_path.unlink()
                self.refresh_config_list()
                messagebox.showinfo("Deleted", f"Configuration '{config_path.stem}' deleted.", parent=self.dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete configuration:\n{e}", parent=self.dialog)
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()
