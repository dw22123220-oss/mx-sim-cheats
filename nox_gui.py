#!/usr/bin/env python3
"""
NOX.CC Cheat Manager - GUI Version
Graphical cheat configuration tool for MX Simulator
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
import os
from datetime import datetime

CONFIG_FILE = "mx_cheats_config.json"

DEFAULT_CONFIG = {
    "power": 1.00,
    "grip": 1.00,
    "roll_resistance": 1.00,
    "erode": False,
    "cheat_enabled": False,
    "online_safe": False
}

class NOXCheatsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NOX.CC v1.0.0")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Set dark theme
        self.root.configure(bg="#0a0a0a")
        self.bg_color = "#0a0a0a"
        self.fg_color = "#00ff00"
        self.accent_color = "#ff6600"
        
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
            return True
        except:
            return False
    
    def create_widgets(self):
        """Create GUI elements"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1a1a", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_title = tk.Label(
            header_frame,
            text="NOX.CC v1.0.0",
            font=("Courier New", 20, "bold"),
            bg="#1a1a1a",
            fg=self.fg_color
        )
        header_title.pack(anchor="w", padx=20, pady=10)
        
        header_info = tk.Label(
            header_frame,
            text="toggle A  show S  panic D  (60% Keyboard)",
            font=("Courier New", 10),
            bg="#1a1a1a",
            fg=self.fg_color
        )
        header_info.pack(anchor="w", padx=20)
        
        # Status line
        status_frame = tk.Frame(self.root, bg="#1a1a1a", height=60)
        status_frame.pack(fill="x", padx=0, pady=5)
        status_frame.pack_propagate(False)
        
        self.cheat_status = tk.Label(
            status_frame,
            text="cheat OFF",
            font=("Courier New", 12, "bold"),
            bg="#1a1a1a",
            fg="#ff0000"
        )
        self.cheat_status.pack(anchor="w", padx=20, pady=5)
        
        self.game_status = tk.Label(
            status_frame,
            text="game not running",
            font=("Courier New", 11),
            bg="#1a1a1a",
            fg=self.accent_color
        )
        self.game_status.pack(anchor="w", padx=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sliders
        self.create_slider(main_frame, "power", "Power", 1.00, 3.00, 0.05, row=0)
        self.create_slider(main_frame, "grip", "Grip", 1.00, 3.00, 0.05, row=1)
        self.create_slider(main_frame, "roll_resistance", "Roll Resistance", 0.50, 2.00, 0.05, row=2)
        
        # Separator
        sep = tk.Frame(main_frame, bg="#333333", height=2)
        sep.grid(row=3, column=0, columnspan=3, sticky="ew", pady=15)
        
        # Erode toggle
        self.create_toggle(main_frame, "erode", "Erode (100% rut depth)", row=4)
        
        # Separator
        sep2 = tk.Frame(main_frame, bg="#333333", height=2)
        sep2.grid(row=5, column=0, columnspan=3, sticky="ew", pady=15)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Button row 1
        self.create_button(button_frame, "▶ START", self.on_start, "#00aa00", 0, 0)
        self.create_button(button_frame, "⏹ STOP", self.on_stop, "#ff0000", 0, 1)
        self.create_button(button_frame, "💾 SAVE", self.on_save, "#0066ff", 0, 2)
        
        # Button row 2
        self.create_button(button_frame, "🔄 RESET", self.on_reset, self.accent_color, 1, 0)
        self.create_button(button_frame, "📤 EXPORT", self.on_export, "#00aaff", 1, 1)
        self.create_button(button_frame, "❌ PANIC", self.on_panic, "#ff0000", 1, 2)
        
        # F-keys info
        info_frame = tk.Frame(self.root, bg="#1a1a1a", height=80)
        info_frame.pack(fill="x", padx=0, pady=0)
        info_frame.pack_propagate(False)
        
        info_label = tk.Label(
            info_frame,
            text="HOTKEYS: A=Toggle | S=Status | D=Panic | Q=Roll | W=Power | E=Grip | R=Erode",
            font=("Courier New", 9),
            bg="#1a1a1a",
            fg=self.fg_color
        )
        info_label.pack(anchor="w", padx=20, pady=15)
    
    def create_slider(self, parent, key, label, min_val, max_val, step, row):
        """Create a slider control"""
        
        label_widget = tk.Label(
            parent,
            text=label,
            font=("Courier New", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        label_widget.grid(row=row, column=0, sticky="w", pady=8)
        
        # Value display
        if not hasattr(self, 'value_labels'):
            self.value_labels = {}
        
        self.value_labels[key] = tk.Label(
            parent,
            text=f"{self.config[key]:.2f} x",
            font=("Courier New", 11, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
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
            fg=self.fg_color,
            troughcolor="#1a1a1a",
            activebackground=self.fg_color,
            highlightthickness=0,
            length=250,
            command=lambda v: self.on_slider_change(key, float(v))
        )
        slider.set(self.config[key])
        slider.grid(row=row, column=1, sticky="ew", padx=10)
        
        parent.columnconfigure(1, weight=1)
    
    def create_toggle(self, parent, key, label, row):
        """Create a toggle control"""
        
        label_widget = tk.Label(
            parent,
            text=label,
            font=("Courier New", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        label_widget.grid(row=row, column=0, sticky="w", pady=8)
        
        # Toggle value
        if not hasattr(self, 'toggle_vars'):
            self.toggle_vars = {}
        
        self.toggle_vars[key] = tk.BooleanVar(value=self.config[key])
        
        toggle_frame = tk.Frame(parent, bg=self.bg_color)
        toggle_frame.grid(row=row, column=1, columnspan=2, sticky="w", padx=10)
        
        toggle_status = tk.Label(
            toggle_frame,
            text=("ON" if self.config[key] else "OFF"),
            font=("Courier New", 11, "bold"),
            bg=self.bg_color,
            fg=("#00ff00" if self.config[key] else "#ff0000")
        )
        toggle_status.pack(side="left", padx=10)
        
        def on_toggle():
            self.config[key] = self.toggle_vars[key].get()
            toggle_status.config(
                text=("ON" if self.config[key] else "OFF"),
                fg=("#00ff00" if self.config[key] else "#ff0000")
            )
        
        checkbox = tk.Checkbutton(
            toggle_frame,
            variable=self.toggle_vars[key],
            bg=self.bg_color,
            fg=self.fg_color,
            activebackground=self.bg_color,
            activeforeground=self.fg_color,
            selectcolor=self.bg_color,
            highlightthickness=0,
            command=on_toggle
        )
        checkbox.pack(side="left")
    
    def create_button(self, parent, text, command, color, row, col):
        """Create a button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="black",
            font=("Courier New", 9, "bold"),
            width=12,
            height=2,
            relief="solid",
            bd=1
        )
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
    
    def on_slider_change(self, key, value):
        """Handle slider change"""
        self.config[key] = round(value, 2)
        self.value_labels[key].config(text=f"{self.config[key]:.2f} x")
    
    def on_start(self):
        """Start cheats"""
        self.config['cheat_enabled'] = True
        self.update_status()
        messagebox.showinfo("NOX", "✓ Cheats ENABLED")
    
    def on_stop(self):
        """Stop cheats"""
        self.config['cheat_enabled'] = False
        self.update_status()
        messagebox.showinfo("NOX", "✓ Cheats DISABLED")
    
    def on_save(self):
        """Save config"""
        if self.save_config():
            messagebox.showinfo("NOX", "✓ Configuration saved!")
        else:
            messagebox.showerror("NOX", "✗ Failed to save")
    
    def on_reset(self):
        """Reset to defaults"""
        if messagebox.askyesno("NOX", "Reset all values to defaults?"):
            self.config = DEFAULT_CONFIG.copy()
            self.refresh_ui()
            self.save_config()
            messagebox.showinfo("NOX", "✓ Reset to defaults")
    
    def on_export(self):
        """Export to Lua"""
        self.export_lua()
    
    def on_panic(self):
        """Panic - disable all"""
        if messagebox.askyesno("NOX", "PANIC - Disable all cheats?"):
            self.config['cheat_enabled'] = False
            self.config['erode'] = False
            self.update_status()
            messagebox.showwarning("NOX", "✓ PANIC - All cheats disabled!")
    
    def update_status(self):
        """Update status display"""
        if self.config['cheat_enabled']:
            self.cheat_status.config(text="cheat ON", fg="#00ff00")
            self.game_status.config(text="game running", fg="#00ff00")
        else:
            self.cheat_status.config(text="cheat OFF", fg="#ff0000")
            self.game_status.config(text="game not running", fg=self.accent_color)
    
    def refresh_ui(self):
        """Refresh UI"""
        for key, label in self.value_labels.items():
            label.config(text=f"{self.config[key]:.2f} x")
        
        for key, var in self.toggle_vars.items():
            var.set(self.config[key])
        
        self.update_status()
    
    def export_lua(self):
        """Export to Lua cheat file"""
        lua_content = f"""-- MX Simulator Cheats Mod
-- Generated by NOX.CC GUI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Configured for 60% Keyboard (Letter A to toggle)

-- Configuration
local POWER_MULTIPLIER = {self.config['power']}
local GRIP_MULTIPLIER = {self.config['grip']}
local ROLL_RESISTANCE_MULTIPLIER = {self.config['roll_resistance']}
local ERODE_ENABLED = {str(self.config['erode']).lower()}
local CHEAT_ENABLED = {str(self.config['cheat_enabled']).lower()}

-- Cheat States
local cheats = {{
    power = {str(self.config['cheat_enabled']).lower()},
    grip = {str(self.config['cheat_enabled']).lower()},
    rollResistance = {str(self.config['cheat_enabled']).lower()},
    erode = {str(self.config['erode']).lower()}
}}

-- Hotkeys (60% Keyboard Compatible)
local KEY_A = 65              -- Toggle cheat ON/OFF
local KEY_S = 83              -- Show status
local KEY_D = 68              -- Panic disable
local KEY_Q = 81              -- Roll Resistance
local KEY_W = 87              -- Power Boost
local KEY_E = 69              -- Grip Boost
local KEY_R = 82              -- Erode

local lastToggleTime = 0
local debounceDelay = 0.2

function update(dt)
    -- Debounce key presses
    lastToggleTime = lastToggleTime + dt
    
    -- Check hotkeys
    if isKeyPressed(KEY_A) and lastToggleTime > debounceDelay then
        cheats.power = not cheats.power
        cheats.grip = not cheats.grip
        cheats.rollResistance = not cheats.rollResistance
        print("[NOX] Cheat " .. (cheats.power and "ON" or "OFF"))
        lastToggleTime = 0
    end
    
    if isKeyPressed(KEY_D) and lastToggleTime > debounceDelay then
        cheats.power = false
        cheats.grip = false
        cheats.rollResistance = false
        cheats.erode = false
        print("[NOX] PANIC - All cheats disabled!")
        lastToggleTime = 0
    end
    
    -- Apply cheats
    local bike = getBike()
    if bike then
        if cheats.power then
            bike.enginePower = (bike.enginePower or 1.0) * POWER_MULTIPLIER
            if bike.maxSpeed then
                bike.maxSpeed = bike.maxSpeed * POWER_MULTIPLIER
            end
        end
        
        if cheats.grip then
            if bike.tires then
                bike.tires.grip = (bike.tires.grip or 1.0) * GRIP_MULTIPLIER
                bike.tires.traction = (bike.tires.traction or 1.0) * GRIP_MULTIPLIER
            end
        end
        
        if cheats.rollResistance then
            bike.rollResistance = (bike.rollResistance or 1.0) * ROLL_RESISTANCE_MULTIPLIER
        end
        
        if cheats.erode then
            if bike.erosionLevel then
                bike.erosionLevel = 1.0  -- 100% rut depth
            end
        end
    end
end

function getBike()
    if game and game.player and game.player.bike then
        return game.player.bike
    end
    return nil
end

function isKeyPressed(keyCode)
    if input and input.isKeyPressed then
        return input.isKeyPressed(keyCode)
    end
    return false
end

print("[NOX] Cheat mod loaded!")
print("[NOX] 60% KEYBOARD - A=Toggle S=Status D=Panic Q=Roll W=Power E=Grip R=Erode")
"""
        
        try:
            with open('cheats.lua', 'w') as f:
                f.write(lua_content)
            messagebox.showinfo("NOX", "✓ Exported to cheats.lua!\n\n60% Keyboard Configured:\nPress A to toggle cheats!\n\nCopy to your MX Sim mods folder.")
        except Exception as e:
            messagebox.showerror("NOX", f"✗ Export failed: {e}")

def main():
    root = tk.Tk()
    app = NOXCheatsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
