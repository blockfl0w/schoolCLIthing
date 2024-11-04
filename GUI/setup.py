from cx_Freeze import setup, Executable

setup(
    name="Reportr",
    version="1.0",
    description="Report your teachers lessons!",
    executables=[
        Executable(
            "main.py",
            base="Win32GUI",  # Removes console window
            target_name="Reportr.exe",  # Name of the executable
        )
    ],
    options={
        "build_exe": {
            "packages": ["tkinter", "sv_ttk", "darkdetect", "bcrypt"],
            "include_files": [],
        }
    },
)
