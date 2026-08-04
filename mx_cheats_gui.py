import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

CONFIG_FILE = "mx_cheats_config.json"

# Default config
DEFAULT_CONFIG = {
    "roll_resistance_multiplier": 0.5,
    "power_multiplier": 2.0,
    "grip_multiplier": 1.2,
    "no_crash_enabled": True
}

class MXCheatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MX Simulator Cheats Config")
        self.root.geometry("500x550")
        self.root.resizable(False, False)
        
        # Set window style
        self.root.configure(bg="#1e1e1e")
        
        # Load config
        self.config = self.load_config()
        
        # Create GUI
        self.create_widgets()
        
    def load_config(self):
        """Load config from JSON file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except:
                return DEFAULT_CONFIG.copy()
        return DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Save config to JSON file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
            messagebox.showinfo("Success", "✓ Config saved successfully!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config:\n{e}")
            return False
    
    def create_widgets(self):
        """Create GUI elements"""
        
        # Title
        title = tk.Label(
            self.root,
            text="MX SIMULATOR CHEATS",
            font=("Arial", 18, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        title.pack(pady=15)
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Roll Resistance
        self.create_slider_control(
            main_frame,
            "Roll Resistance",
            "roll_resistance_multiplier",
            0.1, 1.0, 0.1,
            row=0
        )
        
        # Power/Speed
        self.create_slider_control(
            main_frame,
            "Power/Speed Boost",
            "power_multiplier",
            1.0, 2.0, 0.1,
            row=1
        )
        
        # Grip
        self.create_slider_control(
            main_frame,
            "Grip Boost",
            "grip_multiplier",
            1.0, 2.0, 0.1,
            row=2
        )
        
        # No Crash Toggle
        self.create_checkbox_control(
            main_frame,
            "No Crash Protection",
            "no_crash_enabled",
            row=3
        )
        
        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=4, column=0, columnspan=3, sticky="ew", pady=20)
        
        # Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Save Button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Config",
            command=self.on_save,
            bg="#00aa00",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            height=2
        )
        save_btn.pack(side="left", padx=5)
        
        # Reset Button
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Reset Defaults",
            command=self.on_reset,
            bg="#ff6600",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            height=2
        )
        reset_btn.pack(side="left", padx=5)
        
        # Export Button
        export_btn = tk.Button(
            button_frame,
            text="📤 Export to Lua",
            command=self.on_export,
            bg="#0066ff",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            height=2
        )
        export_btn.pack(side="left", padx=5)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 9),
            bg="#1e1e1e",
            fg="#ffff00"
        )
        self.status_label.pack(pady=10)
    
    def create_slider_control(self, parent, label, key, min_val, max_val, step, row):
        """Create a slider control"""
        
        # Label
        label_widget = tk.Label(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        label_widget.grid(row=row, column=0, sticky="w", pady=10)
        
        # Value display
        self.value_labels = getattr(self, 'value_labels', {})
        self.value_labels[key] = tk.Label(
            parent,
            text=f"{self.config[key]:.1f}",
            font=("Arial", 11, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.value_labels[key].grid(row=row, column=2, sticky="e", padx=10)
        
        # Slider
        slider = tk.Scale(
            parent,
            from_=min_val,
            to=max_val,
            resolution=step,
            orient="horizontal",
            bg="#333333",
            fg="#00ff00",
            troughcolor="#555555",
            activebackground="#00ff00",
            length=200,
            command=lambda v: self.on_slider_change(key, float(v))
        )
        slider.set(self.config[key])
        slider.grid(row=row, column=1, sticky="ew", padx=10)
        
        parent.columnconfigure(1, weight=1)
    
    def create_checkbox_control(self, parent, label, key, row):
        """Create a checkbox control"""
        
        label_widget = tk.Label(
            parent,
            text=label,
            font=("Arial", 11, "bold"),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        label_widget.grid(row=row, column=0, sticky="w", pady=10)
        
        # Checkbox
        self.checkbox_vars = getattr(self, 'checkbox_vars', {})
        self.checkbox_vars[key] = tk.BooleanVar(value=self.config[key])
        
        checkbox = tk.Checkbutton(
            parent,
            variable=self.checkbox_vars[key],
            bg="#1e1e1e",
            fg="#00ff00",
            activebackground="#1e1e1e",
            activeforeground="#00ff00",
            selectcolor="#1e1e1e",
            font=("Arial", 11),
            command=lambda: self.on_checkbox_change(key)
        )
        checkbox.grid(row=row, column=1, sticky="w", padx=10)
    
    def on_slider_change(self, key, value):
        """Handle slider change"""
        self.config[key] = round(value, 1)
        self.value_labels[key].config(text=f"{self.config[key]:.1f}")
    
    def on_checkbox_change(self, key):
        """Handle checkbox change"""
        self.config[key] = self.checkbox_vars[key].get()
    
    def on_save(self):
        """Save config"""
        if self.save_config():
            self.status_label.config(text="✓ Config saved successfully!", fg="#00ff00")
    
    def on_reset(self):
        """Reset to defaults"""
        if messagebox.askyesno("Confirm", "Reset all values to defaults?"):
            self.config = DEFAULT_CONFIG.copy()
            self.refresh_ui()
            self.save_config()
            self.status_label.config(text="✓ Reset to defaults", fg="#00ff00")
    
    def refresh_ui(self):
        """Refresh UI with current config values"""
        for key, label in self.value_labels.items():
            label.config(text=f"{self.config[key]:.1f}")
        
        for key, var in self.checkbox_vars.items():
            var.set(self.config[key])
    
    def on_export(self):
        """Export to Lua file"""
        lua_content = self.generate_lua()
        try:
            with open('cheats.lua', 'w') as f:
                f.write(lua_content)
            messagebox.showinfo("Success", "✓ Successfully exported to cheats.lua!")
            self.status_label.config(text="✓ Exported to cheats.lua", fg="#00ff00")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export:\n{e}")
            self.status_label.config(text="✗ Export failed", fg="#ff0000")
    
    def generate_lua(self):
        """Generate Lua cheat code"""
        return f"""-- MX Simulator Cheats Mod
-- Auto-generated from config manager

-- Configuration
local ROLL_RESISTANCE_MULTIPLIER = {self.config['roll_resistance_multiplier']}  -- 0.1 - 1.0
local POWER_MULTIPLIER = {self.config['power_multiplier']}      -- 1.0 - 2.0
local GRIP_MULTIPLIER = {self.config['grip_multiplier']}       -- 1.0 - 2.0
local NO_CRASH_ENABLED = {str(self.config['no_crash_enabled']).lower()}       -- true/false

-- Cheat States
local cheats = {{
    rollResistance = false,
    power = false,
    grip = false,
    noCrash = {str(self.config['no_crash_enabled']).lower()}
}}

-- Hotkeys
local TOGGLE_ROLL_RESISTANCE = 282  -- F1
local TOGGLE_POWER = 283            -- F2
local TOGGLE_GRIP = 284             -- F3
local TOGGLE_NO_CRASH = 285         -- F4

-- Input detection
function update(dt)
    -- Check for F1 (Roll Resistance toggle)
    if isKeyPressed(TOGGLE_ROLL_RESISTANCE) then
        cheats.rollResistance = not cheats.rollResistance
        print("[MX Cheats] Roll Resistance: " .. (cheats.rollResistance and "ON" or "OFF"))
    end
    
    -- Check for F2 (Power toggle)
    if isKeyPressed(TOGGLE_POWER) then
        cheats.power = not cheats.power
        print("[MX Cheats] Power Boost: " .. (cheats.power and "ON" or "OFF"))
    end
    
    -- Check for F3 (Grip toggle)
    if isKeyPressed(TOGGLE_GRIP) then
        cheats.grip = not cheats.grip
        print("[MX Cheats] Grip Boost: " .. (cheats.grip and "ON" or "OFF"))
    end
    
    -- Check for F4 (No Crash toggle)
    if isKeyPressed(TOGGLE_NO_CRASH) then
        cheats.noCrash = not cheats.noCrash
        print("[MX Cheats] No Crash: " .. (cheats.noCrash and "ON" or "OFF"))
    end
    
    -- Apply cheats
    applyRollResistanceCheat(dt)
    applyPowerCheat(dt)
    applyGripCheat(dt)
    applyNoCrashCheat(dt)
end

-- Roll Resistance Cheat
function applyRollResistanceCheat(dt)
    if not cheats.rollResistance then return end
    
    local bike = getBike()
    if bike then
        bike.rollResistance = bike.rollResistance * ROLL_RESISTANCE_MULTIPLIER
    end
end

-- Power Boost Cheat
function applyPowerCheat(dt)
    if not cheats.power then return end
    
    local bike = getBike()
    if bike then
        -- Increase engine power
        bike.enginePower = bike.enginePower * POWER_MULTIPLIER
        
        -- Increase velocity
        if bike.velocity then
            bike.velocity = bike.velocity * (1 + (POWER_MULTIPLIER - 1) * 0.75)
        end
        
        -- Increase top speed
        if bike.maxSpeed then
            bike.maxSpeed = bike.maxSpeed * POWER_MULTIPLIER
        end
    end
end

-- Grip Boost Cheat
function applyGripCheat(dt)
    if not cheats.grip then return end
    
    local bike = getBike()
    if bike then
        -- Increase tire grip
        if bike.tires then
            bike.tires.grip = bike.tires.grip * GRIP_MULTIPLIER
            bike.tires.traction = bike.tires.traction * GRIP_MULTIPLIER
        end
        
        -- Improve handling
        bike.handling = bike.handling * GRIP_MULTIPLIER
    end
end

-- No Crash Cheat
function applyNoCrashCheat(dt)
    if not cheats.noCrash then return end
    
    local bike = getBike()
    if bike then
        -- Prevent crash/damage
        if bike.crashed then
            bike.crashed = false
        end
        
        -- Keep bike upright
        if bike.rotation then
            -- Gradually correct rotation to upright
            bike.rotation = bike.rotation * 0.95
        end
        
        -- Prevent health loss
        if bike.health then
            bike.health = 100
        end
        
        -- Disable crash state
        if bike.isCrashed then
            bike.isCrashed = false
        end
    end
end

-- Helper function to get bike object
function getBike()
    if game and game.player and game.player.bike then
        return game.player.bike
    end
    return nil
end

-- Helper function to detect key press
function isKeyPressed(keyCode)
    if input and input.isKeyPressed then
        return input.isKeyPressed(keyCode)
    end
    return false
end

-- Initialize
print("[MX Cheats] Mod loaded!")
print("[MX Cheats] F1 = Roll Resistance | F2 = Power | F3 = Grip | F4 = No Crash")
"""

def main():
    root = tk.Tk()
    app = MXCheatsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
