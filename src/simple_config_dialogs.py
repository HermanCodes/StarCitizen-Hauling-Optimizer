import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
from pathlib import Path


class SimpleConfigDialogs:
    """Simplified configuration dialogs - text input for save, list for load"""
    
    @staticmethod
    def save_config_dialog(parent, settings_manager):
        """Simple text input dialog for saving configuration"""
        config_folder = settings_manager.get_config_folder()
        if not config_folder:
            return None
            
        # Simple text input for filename
        name = simpledialog.askstring(
            "Save Configuration",
            "Enter configuration name:",
            parent=parent
        )
        
        if not name:
            return None
            
        # Remove .json extension if user added it
        if name.lower().endswith('.json'):
            name = name[:-5]
        
        config_path = Path(config_folder) / f"{name}.json"
        
        # Check if file exists
        if config_path.exists():
            result = messagebox.askyesno(
                "Overwrite Configuration",
                f"Configuration '{name}' already exists.\nDo you want to overwrite it?",
                parent=parent
            )
            if not result:
                return None
        
        settings_manager.set_last_config(config_path)
        return config_path
    
    @staticmethod
    def load_config_dialog(parent, settings_manager):
        """Simple list dialog for loading configuration"""
        config_folder = settings_manager.get_config_folder()
        if not config_folder:
            return None
            
        config_folder_path = Path(config_folder)
        if not config_folder_path.exists():
            messagebox.showerror(
                "Folder Error",
                f"Configuration folder does not exist:\n{config_folder}",
                parent=parent
            )
            return None
        
        # Get all .json files
        json_files = list(config_folder_path.glob("*.json"))
        if not json_files:
            messagebox.showinfo(
                "No Configurations",
                "No saved configurations found in the folder.",
                parent=parent
            )
            return None
        
        # Sort by modification time (newest first)
        json_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Create simple selection dialog
        dialog = SimpleLoadDialog(parent, json_files, settings_manager)
        return dialog.result


class SimpleLoadDialog:
    """Simple dialog for selecting a configuration to load"""
    
    def __init__(self, parent, json_files, settings_manager):
        self.parent = parent
        self.json_files = json_files
        self.settings_manager = settings_manager
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Load Configuration")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 100,
            parent.winfo_rooty() + 100
        ))
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Create the dialog widgets"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Select Configuration to Load:", 
                              font=("Arial", 12, "bold"))
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # List frame with scrollbar
        list_frame = tk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.config_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.config_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.config_listbox.yview)
        
        # Populate list
        for json_file in self.json_files:
            # Display name without .json extension
            display_name = json_file.stem
            
            # Add modification time
            mtime = json_file.stat().st_mtime
            import datetime
            mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%m/%d %H:%M")
            
            self.config_listbox.insert(tk.END, f"{display_name} ({mod_time})")
        
        # Select first item by default
        if self.json_files:
            self.config_listbox.selection_set(0)
        
        # Double-click to load
        self.config_listbox.bind("<Double-Button-1>", lambda e: self.load_selected())
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Load", command=self.load_selected, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT)
        tk.Button(button_frame, text="Delete", command=self.delete_selected, 
                 bg="#f44336", fg="white").pack(side=tk.LEFT)
    
    def load_selected(self):
        """Load the selected configuration"""
        selection = self.config_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a configuration to load.", parent=self.dialog)
            return
        
        selected_file = self.json_files[selection[0]]
        if not selected_file.exists():
            messagebox.showerror("Error", "Selected configuration file does not exist.", parent=self.dialog)
            return
        
        self.result = selected_file
        self.settings_manager.set_last_config(selected_file)
        self.dialog.destroy()
    
    def delete_selected(self):
        """Delete the selected configuration"""
        selection = self.config_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a configuration to delete.", parent=self.dialog)
            return
        
        selected_file = self.json_files[selection[0]]
        
        result = messagebox.askyesno(
            "Delete Configuration",
            f"Are you sure you want to delete '{selected_file.stem}'?\nThis cannot be undone.",
            parent=self.dialog
        )
        
        if result:
            try:
                selected_file.unlink()
                # Remove from list
                index = selection[0]
                self.config_listbox.delete(index)
                self.json_files.pop(index)
                
                messagebox.showinfo("Deleted", f"Configuration '{selected_file.stem}' deleted.", parent=self.dialog)
                
                # Close dialog if no more files
                if not self.json_files:
                    messagebox.showinfo("No Configurations", "No more configurations available.", parent=self.dialog)
                    self.cancel()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete configuration:\n{e}", parent=self.dialog)
    
    def cancel(self):
        """Cancel the dialog"""
        self.result = None
        self.dialog.destroy()
