import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog


class SettingsManager:
    """Manages application settings including configuration folder location"""
    
    def __init__(self):
        self.settings_file = Path.home() / ".container_allocator_settings.json"
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create default settings"""
        default_settings = {
            "config_folder": None,
            "last_config": None
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to handle new settings
                    default_settings.update(settings)
                    return default_settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return default_settings
        
        return default_settings
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_config_folder(self):
        """Get the configured folder for saving/loading configurations"""
        return self.settings.get("config_folder")
    
    def set_config_folder(self, folder_path):
        """Set the configuration folder"""
        self.settings["config_folder"] = str(folder_path) if folder_path else None
        return self.save_settings()
    
    def get_last_config(self):
        """Get the last used configuration file"""
        return self.settings.get("last_config")
    
    def set_last_config(self, config_path):
        """Set the last used configuration file"""
        self.settings["last_config"] = str(config_path) if config_path else None
        return self.save_settings()
    
    def setup_config_folder(self, parent_window):
        """Interactive setup of configuration folder"""
        result = messagebox.askyesno(
            "Configuration Folder Setup",
            "Would you like to set up a folder for storing your container configurations?\n\n"
            "This will make it easier to save and load your setups.",
            parent=parent_window
        )
        
        if not result:
            return False
        
        # Ask user to select or create a folder
        folder_path = filedialog.askdirectory(
            title="Select or Create Configuration Folder",
            parent=parent_window
        )
        
        if not folder_path:
            return False
        
        # Ensure the folder exists
        try:
            os.makedirs(folder_path, exist_ok=True)
            self.set_config_folder(folder_path)
            
            messagebox.showinfo(
                "Setup Complete",
                f"Configuration folder set to:\n{folder_path}\n\n"
                "You can change this later in the Settings menu.",
                parent=parent_window
            )
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Setup Error",
                f"Could not create/access folder:\n{e}",
                parent=parent_window
            )
            return False
    
    def show_settings_dialog(self, parent_window):
        """Show settings configuration dialog"""
        dialog = SettingsDialog(parent_window, self)
        return dialog.result


class SettingsDialog:
    """Dialog for configuring application settings"""
    
    def __init__(self, parent, settings_manager):
        self.parent = parent
        self.settings_manager = settings_manager
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Create the settings dialog widgets"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Container Allocator Settings", 
                              font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Configuration folder section
        config_frame = tk.LabelFrame(main_frame, text="Configuration Folder", padx=10, pady=10)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        current_folder = self.settings_manager.get_config_folder()
        if current_folder:
            folder_text = f"Current: {current_folder}"
        else:
            folder_text = "No folder configured"
        
        self.folder_label = tk.Label(config_frame, text=folder_text, wraplength=400, justify=tk.LEFT)
        self.folder_label.pack(anchor=tk.W, pady=(0, 10))
        
        button_frame = tk.Frame(config_frame)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Change Folder", 
                 command=self.change_folder).pack(side=tk.LEFT, padx=(0, 10))
        
        if current_folder:
            tk.Button(button_frame, text="Clear Folder", 
                     command=self.clear_folder).pack(side=tk.LEFT)
        
        # Info section
        info_frame = tk.LabelFrame(main_frame, text="Information", padx=10, pady=10)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        info_text = (
            "• Configuration folder: Where your saved configurations are stored\n"
            "• When set, Save/Load will use a simple dialog instead of file browser\n"
            "• Settings are automatically saved between sessions"
        )
        
        tk.Label(info_frame, text=info_text, justify=tk.LEFT, wraplength=400).pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Close", command=self.close_dialog).pack(side=tk.RIGHT)
    
    def change_folder(self):
        """Change the configuration folder"""
        folder_path = filedialog.askdirectory(
            title="Select Configuration Folder",
            initialdir=self.settings_manager.get_config_folder(),
            parent=self.dialog
        )
        
        if folder_path:
            try:
                os.makedirs(folder_path, exist_ok=True)
                self.settings_manager.set_config_folder(folder_path)
                self.folder_label.config(text=f"Current: {folder_path}")
                self.result = "changed"
                
                messagebox.showinfo(
                    "Folder Updated",
                    f"Configuration folder updated to:\n{folder_path}",
                    parent=self.dialog
                )
                
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Could not set folder:\n{e}",
                    parent=self.dialog
                )
    
    def clear_folder(self):
        """Clear the configuration folder setting"""
        result = messagebox.askyesno(
            "Clear Folder",
            "Are you sure you want to clear the configuration folder?\n\n"
            "Save/Load will use the file browser again.",
            parent=self.dialog
        )
        
        if result:
            self.settings_manager.set_config_folder(None)
            self.folder_label.config(text="No folder configured")
            self.result = "cleared"
    
    def close_dialog(self):
        """Close the settings dialog"""
        self.dialog.destroy()
