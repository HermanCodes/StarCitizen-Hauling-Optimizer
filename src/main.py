import tkinter as tk
from container_app import ContainerAllocatorApp

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = ContainerAllocatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()