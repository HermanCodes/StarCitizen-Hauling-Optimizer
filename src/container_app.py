"""
Container Allocator Application
Main application window and coordination logic
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os

from solver import ContainerSolver
from ui_components import InputGrids, OutputDisplay, ManagementButtons
from dialogs import ItemSelectionDialog
from settings import SettingsManager
from simple_config_dialogs import SimpleConfigDialogs


class ContainerAllocatorApp:
    """Main application class that coordinates all components"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Container Allocator")
        self.root.geometry("1400x900")
        # Initialize settings manager
        self.settings_manager = SettingsManager()
        # Initialize data - start with empty configuration
        self.materials = []
        self.sizes = [1, 2, 4]
        self.locations = []

        # Initialize components
        self.solver = ContainerSolver()
        self.input_grids = None
        self.output_display = None
        self.mgmt_buttons = None
        
        self.build_ui()

    def build_ui(self):
        """Build the main UI structure"""
        # Create menu bar
        self.create_menu()
                # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Management buttons
        self.mgmt_buttons = ManagementButtons(main_frame, self)
        self.mgmt_buttons.pack(fill=tk.X, pady=(0, 10))

        # Input grids container
        input_container = ttk.Frame(main_frame)
        input_container.pack(fill=tk.X, pady=(0, 10))
        
        self.input_grids = InputGrids(input_container, self.materials, self.sizes, self.locations)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        ttk.Button(left_buttons, text="Calculate Allocation", 
                  command=self.calculate, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(left_buttons, text="Clear All", 
                  command=self.clear_inputs).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(left_buttons, text="Load Example", 
                  command=self.load_example).pack(side=tk.LEFT)

        # Right side buttons (Configuration management)
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        ttk.Button(right_buttons, text="Save Config", 
                  command=self.save_configuration).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(right_buttons, text="Load Config", 
                  command=self.load_configuration).pack(side=tk.LEFT)

        # Output display
        self.output_display = OutputDisplay(main_frame)
        self.output_display.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(5, 0))

    def rebuild_grids(self):
        """Rebuild input grids after configuration changes"""
        self.input_grids.rebuild(self.materials, self.sizes, self.locations)

    def set_status(self, message):
        """Update status bar message"""
        self.status_var.set(message)

    # Management methods
    def add_location(self):
        """Add a new location"""
        name = simpledialog.askstring("Add Location", "Enter location name:")
        if name and name.strip():
            name = name.strip()
            if name not in self.locations:
                self.locations.append(name)
                self.rebuild_grids()
                self.set_status(f"Added location: {name}")
            else:
                messagebox.showwarning("Duplicate", f"Location '{name}' already exists!")

    def remove_location(self):
        """Remove an existing location"""
        if len(self.locations) <= 1:
            messagebox.showwarning("Cannot Remove", "At least one location must remain!")
            return
        
        dialog = ItemSelectionDialog(self.root, "Remove Location", self.locations)
        if dialog.result:
            self.locations.remove(dialog.result)
            self.rebuild_grids()
            self.set_status(f"Removed location: {dialog.result}")

    def add_material(self):
        """Add a new material"""
        name = simpledialog.askstring("Add Material", "Enter material name:")
        if name and name.strip():
            name = name.strip()
            if name not in self.materials:
                self.materials.append(name)
                self.rebuild_grids()
                self.set_status(f"Added material: {name}")
            else:
                messagebox.showwarning("Duplicate", f"Material '{name}' already exists!")

    def remove_material(self):
        """Remove an existing material"""
        if len(self.materials) <= 1:
            messagebox.showwarning("Cannot Remove", "At least one material must remain!")
            return
        
        dialog = ItemSelectionDialog(self.root, "Remove Material", self.materials)
        if dialog.result:
            self.materials.remove(dialog.result)
            self.rebuild_grids()
            self.set_status(f"Removed material: {dialog.result}")

    def add_size(self):
        """Add a new container size"""
        while True:
            size_str = simpledialog.askstring("Add Container Size", "Enter container size (SCU):")
            if not size_str:
                return
            
            try:
                size = int(size_str.strip())
                if size <= 0:
                    messagebox.showerror("Invalid Size", "Container size must be a positive integer!")
                    continue
                if size not in self.sizes:
                    self.sizes.append(size)
                    self.sizes.sort()  # Keep sizes sorted
                    self.rebuild_grids()
                    self.set_status(f"Added container size: {size}-SCU")
                    return
                else:
                    messagebox.showwarning("Duplicate", f"Container size {size}-SCU already exists!")
                    continue
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid integer!")

    def remove_size(self):
        """Remove an existing container size"""
        if len(self.sizes) <= 1:
            messagebox.showwarning("Cannot Remove", "At least one container size must remain!")
            return
        
        size_strings = [f"{size}-SCU" for size in self.sizes]
        dialog = ItemSelectionDialog(self.root, "Remove Container Size", size_strings)
        if dialog.result:
            size_to_remove = int(dialog.result.split('-')[0])
            self.sizes.remove(size_to_remove)
            self.rebuild_grids()
            self.set_status(f"Removed container size: {size_to_remove}-SCU")

    # Core functionality methods
    def validate_inputs(self):
        """Validate that inputs are reasonable"""
        req_vars, cont_vars = self.input_grids.get_variables()
        
        # Check if configuration is complete
        if not self.materials:
            messagebox.showwarning("Configuration Error", "Please add at least one material before calculating.")
            return False
        
        if not self.locations:
            messagebox.showwarning("Configuration Error", "Please add at least one location before calculating.")
            return False
        
        # Check if any requirements are set
        total_requirements = sum(var.get() for var in req_vars.values())
        if total_requirements == 0:
            messagebox.showwarning("Input Error", "Please enter at least one location requirement.")
            return False

        # Check if any containers are available
        total_containers = sum(var.get() for var in cont_vars.values())
        if total_containers == 0:
            messagebox.showwarning("Input Error", "Please enter at least one available container.")
            return False

        return True

    def calculate(self):
        """Perform the optimization calculation"""
        if not self.validate_inputs():
            return

        self.set_status("Calculating...")
        self.root.update()

        try:
            # Get input data
            req_vars, cont_vars = self.input_grids.get_variables()
            requirements = {
                loc: {mat: req_vars[(loc, mat)].get() for mat in self.materials} 
                for loc in self.locations
            }
            available = {
                mat: {size: cont_vars[(mat, size)].get() for size in self.sizes} 
                for mat in self.materials
            }

            # Solve the problem
            result = self.solver.solve(requirements, available, self.locations, self.materials, self.sizes)

            # Display results
            if result['success']:
                self.output_display.show_solution(result, requirements, available, 
                                                self.locations, self.materials, self.sizes)
                self.set_status("Solution found successfully")
            else:
                self.output_display.show_no_solution(requirements, available, 
                                                   self.materials, self.locations, self.sizes)
                self.set_status("No solution found")

        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred during calculation:\n{str(e)}")
            self.set_status("Error occurred")

    def clear_inputs(self):
        """Clear all input fields"""
        self.input_grids.clear_all()
        self.output_display.clear()
        self.set_status("Inputs cleared")

    def load_example(self):
        """Load example data for testing with current configuration"""
        # Check if we have a basic configuration
        if not self.materials or not self.locations:
            messagebox.showinfo("Configuration Required", 
                              "Please add materials and locations first before loading example data.\n\n"
                              "Suggested setup:\n"
                              "• Materials: Titanium, Aluminum, Carbon\n"
                              "• Locations: Sakura Sun, NB Int, Greycat Stanton")
            return
        
        example_data = {
            'requirements': {
                ("Sakura Sun", "Titanium"): 10,
                ("Sakura Sun", "Aluminum"): 15,
                ("Sakura Sun", "Carbon"): 8,
                ("NB Int", "Titanium"): 6,
                ("NB Int", "Aluminum"): 12,
                ("NB Int", "Carbon"): 4,
                ("Greycat Stanton", "Titanium"): 8,
                ("Greycat Stanton", "Aluminum"): 10,
                ("Greycat Stanton", "Carbon"): 6,
            },
            'availability': {
                ("Titanium", 1): 5,
                ("Titanium", 2): 8,
                ("Titanium", 4): 3,
                ("Aluminum", 1): 10,
                ("Aluminum", 2): 12,
                ("Aluminum", 4): 5,
                ("Carbon", 1): 6,
                ("Carbon", 2): 4,
                ("Carbon", 4): 2,
            }
        }

        self.input_grids.load_example_data(example_data, self.locations, self.materials, self.sizes)
        self.set_status("Example data loaded (compatible items only)")

    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Configuration", command=self.save_configuration)
        file_menu.add_command(label="Load Configuration", command=self.load_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Configuration Folder", command=self.show_settings)
        settings_menu.add_separator()
        settings_menu.add_command(label="Setup Config Folder", command=self.setup_config_folder)

    def show_settings(self):
        """Show the settings dialog"""
        self.settings_manager.show_settings_dialog(self.root)
    
    def setup_config_folder(self):
        """Setup configuration folder"""
        self.settings_manager.setup_config_folder(self.root)

    # Configuration management methods
    def save_configuration(self):
        """Save current configuration to JSON file"""
        try:
            # Get current input values
            req_vars, cont_vars = self.input_grids.get_variables()
            
            # Build configuration data
            config_data = {
                "metadata": {
                    "version": "1.0",
                    "description": "Container Allocator Configuration"
                },
                "configuration": {
                    "materials": self.materials.copy(),
                    "sizes": self.sizes.copy(),
                    "locations": self.locations.copy()
                },
                "requirements": {
                    f"{loc}|{mat}": req_vars[(loc, mat)].get()
                    for loc in self.locations
                    for mat in self.materials
                },
                "availability": {
                    f"{mat}|{size}": cont_vars[(mat, size)].get()
                    for mat in self.materials
                    for size in self.sizes
                }
            }
            
            # Check if config folder is set up
            config_folder = self.settings_manager.get_config_folder()
            if not config_folder:
                messagebox.showinfo("Setup Required", "Please set up a configuration folder first.\nGo to Settings -> Setup Config Folder")
                return
            
            # Get filename using simple dialog
            filename = SimpleConfigDialogs.save_config_dialog(self.root, self.settings_manager)
            if not filename:
                return
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                
                self.set_status(f"Configuration saved: {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Configuration saved successfully!\n\nFile: {os.path.basename(filename)}")
                
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save configuration:\n{str(e)}")
            self.set_status("Failed to save configuration")

    def load_configuration(self):
        """Load configuration from JSON file"""
        try:
            # Check if config folder is set up
            config_folder = self.settings_manager.get_config_folder()
            if not config_folder:
                messagebox.showinfo("Setup Required", "Please set up a configuration folder first.\nGo to Settings -> Setup Config Folder")
                return
            
            # Get filename using simple dialog
            filename = SimpleConfigDialogs.load_config_dialog(self.root, self.settings_manager)
            if not filename:
                return
                
            with open(filename, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Validate configuration structure
            if not self._validate_config_structure(config_data):
                messagebox.showerror("Invalid File", 
                                   "The selected file is not a valid configuration file.")
                return
            
            # Ask user to confirm loading (will overwrite current data)
            if not messagebox.askyesno("Confirm Load", 
                                     "Loading this configuration will replace all current settings and data.\n\n"
                                     "Do you want to continue?"):
                return
            
            # Load configuration
            config = config_data["configuration"]
            self.materials = config["materials"]
            self.sizes = config["sizes"]  
            self.locations = config["locations"]
            
            # Rebuild grids with new configuration
            self.rebuild_grids()
            
            # Load saved data
            req_vars, cont_vars = self.input_grids.get_variables()
            
            # Load requirements
            for key, value in config_data.get("requirements", {}).items():
                if "|" in key:
                    loc, mat = key.split("|", 1)
                    if (loc, mat) in req_vars:
                        req_vars[(loc, mat)].set(value)
            
            # Load availability
            for key, value in config_data.get("availability", {}).items():
                if "|" in key:
                    mat, size_str = key.split("|", 1)
                    try:
                        size = int(size_str)
                        if (mat, size) in cont_vars:
                            cont_vars[(mat, size)].set(value)
                    except ValueError:
                        continue
            
            # Clear output and update status
            self.output_display.clear()
            self.set_status(f"Configuration loaded: {os.path.basename(filename)}")
            messagebox.showinfo("Success", f"Configuration loaded successfully!\n\n"
                              f"Materials: {len(self.materials)}\n"
                              f"Locations: {len(self.locations)}\n"
                              f"Container Sizes: {len(self.sizes)}")
                              
        except json.JSONDecodeError:
            messagebox.showerror("File Error", "The selected file is not a valid JSON file.")
        except FileNotFoundError:
            messagebox.showerror("File Error", "The selected file could not be found.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load configuration:\n{str(e)}")
            self.set_status("Failed to load configuration")

    def _validate_config_structure(self, config_data):
        """Validate that the config file has the expected structure"""
        try:
            # Check required top-level keys
            if not isinstance(config_data, dict):
                return False
                
            config = config_data.get("configuration", {})
            if not isinstance(config, dict):
                return False
            
            # Check required configuration keys
            required_keys = ["materials", "sizes", "locations"]
            for key in required_keys:
                if key not in config:
                    return False
                if not isinstance(config[key], list):
                    return False
                if len(config[key]) == 0:
                    return False
            
            # Validate sizes are integers
            for size in config["sizes"]:
                if not isinstance(size, int) or size <= 0:
                    return False
            
            return True
            
        except Exception:
            return False
