"""
UI Components for Container Allocator
Reusable UI component classes
"""

import tkinter as tk
from tkinter import ttk
from tabulate import tabulate
from pulp import value


class ManagementButtons(ttk.LabelFrame):
    """Management buttons for adding/removing locations, materials, and sizes"""
    
    def __init__(self, parent, app):
        super().__init__(parent, text="Manage Configuration")
        self.app = app
        self.build_ui()
    
    def build_ui(self):
        """Build the management button interface"""
        # Main container for horizontal layout
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.X, padx=10, pady=10)
        
        # Configure columns to be equal width
        main_container.columnconfigure(0, weight=1, uniform="column")
        main_container.columnconfigure(1, weight=1, uniform="column")
        main_container.columnconfigure(2, weight=1, uniform="column")
        
        # Location management
        loc_frame = ttk.Frame(main_container)
        loc_frame.grid(row=0, column=0, padx=10, sticky="ew")
        
        ttk.Label(loc_frame, text="Locations", 
                 font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 5))
        
        loc_buttons = ttk.Frame(loc_frame)
        loc_buttons.pack()
        
        ttk.Button(loc_buttons, text="−", width=3,
                  command=self.app.remove_location).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(loc_buttons, text="+", width=3,
                  command=self.app.add_location).pack(side=tk.LEFT)
        
        # Material management
        mat_frame = ttk.Frame(main_container)
        mat_frame.grid(row=0, column=1, padx=10, sticky="ew")
        
        ttk.Label(mat_frame, text="Materials", 
                 font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 5))
        
        mat_buttons = ttk.Frame(mat_frame)
        mat_buttons.pack()
        
        ttk.Button(mat_buttons, text="−", width=3,
                  command=self.app.remove_material).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(mat_buttons, text="+", width=3,
                  command=self.app.add_material).pack(side=tk.LEFT)
        
        # Size management
        size_frame = ttk.Frame(main_container)
        size_frame.grid(row=0, column=2, padx=10, sticky="ew")
        
        ttk.Label(size_frame, text="Container Sizes", 
                 font=('TkDefaultFont', 10, 'bold')).pack(pady=(0, 5))
        
        size_buttons = ttk.Frame(size_frame)
        size_buttons.pack()
        
        ttk.Button(size_buttons, text="−", width=3,
                  command=self.app.remove_size).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(size_buttons, text="+", width=3,
                  command=self.app.add_size).pack(side=tk.LEFT)


class InputGrids:
    """Input grids for requirements and container availability"""
    
    def __init__(self, parent, materials, sizes, locations):
        self.parent = parent
        self.req_vars = {}
        self.cont_vars = {}
        self.req_frame = None
        self.cont_frame = None
        
        self.build_grids(materials, sizes, locations)
    
    def build_grids(self, materials, sizes, locations):
        """Build or rebuild the input grids"""
        # Clear existing frames
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Location Requirements
        self.req_frame = ttk.LabelFrame(self.parent, text="Location Requirements (SCU needed)")
        self.req_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Check if we have materials and locations to display
        if not materials or not locations:
            # Show helpful message when no materials or locations are configured
            message_frame = ttk.Frame(self.req_frame)
            message_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
            
            if not materials and not locations:
                message = "Add materials and locations using the buttons above to get started."
            elif not materials:
                message = "Add materials using the '+' button above to configure requirements."
            else:  # not locations
                message = "Add locations using the '+' button above to configure requirements."
            
            ttk.Label(message_frame, text=message, 
                     font=('TkDefaultFont', 10), 
                     foreground='gray',
                     anchor='center').pack(expand=True)
            self.req_vars = {}
        else:
            # Requirements header
            ttk.Label(self.req_frame, text="Location", 
                     font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            for j, mat in enumerate(materials):
                ttk.Label(self.req_frame, text=mat, 
                         font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=j+1, padx=5, pady=5)

            # Requirements grid
            new_req_vars = {}
            for i, loc in enumerate(locations):
                ttk.Label(self.req_frame, text=loc).grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
                for j, mat in enumerate(materials):
                    # Preserve existing values if they exist
                    old_value = self.req_vars.get((loc, mat), tk.IntVar(value=0)).get()
                    var = tk.IntVar(value=old_value)
                    entry = ttk.Entry(self.req_frame, width=8, textvariable=var, justify='center')
                    entry.grid(row=i+1, column=j+1, padx=5, pady=2)
                    new_req_vars[(loc, mat)] = var
            
            self.req_vars = new_req_vars

        # Container Availability
        self.cont_frame = ttk.LabelFrame(self.parent, text="Container Availability")
        self.cont_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Check if we have materials to display
        if not materials:
            # Show helpful message when no materials are configured
            message_frame = ttk.Frame(self.cont_frame)
            message_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
            
            ttk.Label(message_frame, text="Add materials using the '+' button above to configure container availability.", 
                     font=('TkDefaultFont', 10), 
                     foreground='gray',
                     anchor='center').pack(expand=True)
            self.cont_vars = {}
        else:
            # Container header
            ttk.Label(self.cont_frame, text="Size", 
                     font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            for j, mat in enumerate(materials):
                ttk.Label(self.cont_frame, text=mat, 
                         font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=j+1, padx=5, pady=5)

            # Container grid
            new_cont_vars = {}
            for i, size in enumerate(sizes):
                ttk.Label(self.cont_frame, text=f"{size}-SCU").grid(row=i+1, column=0, padx=5, pady=2, sticky="w")
                for j, mat in enumerate(materials):
                    # Preserve existing values if they exist
                    old_value = self.cont_vars.get((mat, size), tk.IntVar(value=0)).get()
                    var = tk.IntVar(value=old_value)
                    entry = ttk.Entry(self.cont_frame, width=8, textvariable=var, justify='center')
                    entry.grid(row=i+1, column=j+1, padx=5, pady=2)
                    new_cont_vars[(mat, size)] = var
            
            self.cont_vars = new_cont_vars
    
    def rebuild(self, materials, sizes, locations):
        """Rebuild grids with new configuration"""
        self.build_grids(materials, sizes, locations)
    
    def get_variables(self):
        """Get the current variable dictionaries"""
        return self.req_vars, self.cont_vars
    
    def clear_all(self):
        """Clear all input fields"""
        for var in self.req_vars.values():
            var.set(0)
        for var in self.cont_vars.values():
            var.set(0)
    
    def load_example_data(self, example_data, locations, materials, sizes):
        """Load example data into the grids"""
        # Load requirements
        for (loc, mat), val in example_data['requirements'].items():
            if loc in locations and mat in materials and (loc, mat) in self.req_vars:
                self.req_vars[(loc, mat)].set(val)
        
        # Load availability
        for (mat, size), val in example_data['availability'].items():
            if mat in materials and size in sizes and (mat, size) in self.cont_vars:
                self.cont_vars[(mat, size)].set(val)


class OutputDisplay(ttk.LabelFrame):
    """Output display area with scrollable text"""
    
    def __init__(self, parent):
        super().__init__(parent, text="Allocation Results")
        self.output = None
        self.build_ui()
    
    def build_ui(self):
        """Build the output display interface"""
        # Text widget with scrollbars
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.output = tk.Text(text_frame, height=15, font=('Consolas', 10), wrap=tk.NONE)
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.output.xview)
        
        self.output.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.output.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
    
    def clear(self):
        """Clear the output display"""
        self.output.delete(1.0, tk.END)
    
    def show_solution(self, result, requirements, available, locations, materials, sizes):
        """Display the optimal solution"""
        self.clear()
        x = result['variables']
        
        self.output.insert(tk.END, "✅ OPTIMAL ALLOCATION FOUND\n")
        self.output.insert(tk.END, "=" * 60 + "\n\n")

        # Main allocation table
        headers = ["Location", "Material"] + [f"{s}×SCU" for s in sizes] + ["Total SCU"]
        rows = []

        for loc in locations:
            for mat in materials:
                row = [loc, mat]
                total_scu = 0
                
                for size in sizes:
                    container_count = int(value(x[(loc, mat, size)]))
                    # Show count with units for clarity
                    if container_count > 0:
                        row.append(f"{container_count}×")
                    else:
                        row.append("-")
                    total_scu += container_count * size
                
                # Highlight total SCU
                row.append(f"{total_scu} SCU")
                rows.append(row)

        table = tabulate(rows, headers=headers, tablefmt="fancy_grid", numalign="center", stralign="center")
        self.output.insert(tk.END, table)
        
        # Container summary table
        self._show_container_summary(x, materials, sizes, locations)
        
        self.output.insert(tk.END, f"\n📊 SUMMARY:\n")
        self.output.insert(tk.END, f"• Total containers allocated: {result['total_containers']}\n")
        self.output.insert(tk.END, f"• Optimization status: OPTIMAL\n\n")

        # Container utilization summary
        self._show_utilization(x, available, materials, sizes, locations)
    
    def show_no_solution(self, requirements, available, materials, locations, sizes):
        """Display when no solution is found"""
        self.clear()
        self.output.insert(tk.END, "❌ NO FEASIBLE SOLUTION FOUND\n")
        self.output.insert(tk.END, "=" * 40 + "\n\n")
        self.output.insert(tk.END, "Possible reasons:\n")
        self.output.insert(tk.END, "• Insufficient container capacity\n")
        self.output.insert(tk.END, "• Wrong material types available\n")
        self.output.insert(tk.END, "• Check your input values\n\n")
        
        self._show_capacity_analysis(requirements, available, materials, locations, sizes)
    
    def _show_container_summary(self, x, materials, sizes, locations):
        """Show total container usage summary by material and size"""
        self.output.insert(tk.END, "\n📦 CONTAINER USAGE SUMMARY:\n")
        summary_headers = ["Material"] + [f"{s}×SCU" for s in sizes] + ["Total Containers"]
        summary_rows = []

        for mat in materials:
            row = [mat]
            total_containers = 0
            
            for size in sizes:
                # Sum up containers of this size across all locations
                size_total = sum(int(value(x[(loc, mat, size)])) for loc in locations)
                if size_total > 0:
                    row.append(f"{size_total}×")
                else:
                    row.append("-")
                total_containers += size_total
            
            # Add total containers for this material
            if total_containers > 0:
                row.append(f"{total_containers}×")
                summary_rows.append(row)
        
        # Only show the table if there are containers being used
        if summary_rows:
            summary_table = tabulate(summary_rows, headers=summary_headers, tablefmt="fancy_grid", numalign="center")
            self.output.insert(tk.END, summary_table)
    
    def _show_utilization(self, x, available, materials, sizes, locations):
        """Show container utilization details"""
        self.output.insert(tk.END, "\n📦 CONTAINER UTILIZATION:\n")
        util_headers = ["Material", "Size", "Available", "Used", "Remaining", "Usage %"]
        util_rows = []

        for mat in materials:
            for size in sizes:
                available_count = available[mat][size]
                used_count = sum(int(value(x[(loc, mat, size)])) for loc in locations)
                remaining = available_count - used_count
                
                # Only show rows where containers are available
                if available_count > 0:
                    percent_used = f"{(used_count/available_count*100):.0f}%"
                    
                    # Color-code the usage percentage
                    if used_count == available_count:
                        usage_display = f"{percent_used} (FULL)"
                    elif used_count == 0:
                        usage_display = f"{percent_used} (UNUSED)"
                    else:
                        usage_display = percent_used
                    
                    util_rows.append([
                        mat, 
                        f"{size}×SCU", 
                        f"{available_count}×", 
                        f"{used_count}×", 
                        f"{remaining}×", 
                        usage_display
                    ])

        util_table = tabulate(util_rows, headers=util_headers, tablefmt="fancy_grid", numalign="center")
        self.output.insert(tk.END, util_table)
    
    def _show_capacity_analysis(self, requirements, available, materials, locations, sizes):
        """Show capacity analysis when no solution exists"""
        self.output.insert(tk.END, "📋 CAPACITY ANALYSIS:\n")
        
        analysis_headers = ["Material", "Required", "Available", "Difference", "Status"]
        analysis_rows = []
        
        for mat in materials:
            total_required = sum(requirements[loc][mat] for loc in locations)
            total_available = sum(available[mat][size] * size for size in sizes)
            difference = total_available - total_required
            
            # Format the difference with + or - sign
            if difference >= 0:
                diff_display = f"+{difference} SCU"
                status = "✅ SUFFICIENT"
            else:
                diff_display = f"{difference} SCU"
                status = "❌ INSUFFICIENT"
            
            analysis_rows.append([
                mat, 
                f"{total_required} SCU", 
                f"{total_available} SCU", 
                diff_display,
                status
            ])
        
        analysis_table = tabulate(analysis_rows, headers=analysis_headers, tablefmt="fancy_grid", numalign="center")
        self.output.insert(tk.END, analysis_table)
