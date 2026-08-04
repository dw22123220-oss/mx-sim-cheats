#!/usr/bin/env python3
"""
NOX.CC Cheat Manager - CLI Version
Terminal-style cheat configuration tool for MX Simulator
"""

import json
import os
import sys
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

class NOXCheats:
    def __init__(self):
        self.config = self.load_config()
        self.running = True
        
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
    
    def display_header(self):
        """Display NOX header"""
        print("\033[92m" + "=" * 70)
        print("NOX.CC v1.0.0".ljust(24) + "toggle A  show S  panic D")
        print("=" * 70 + "\033[0m")
    
    def display_status(self):
        """Display cheat status"""
        status = "\033[91mOFF\033[0m" if not self.config['cheat_enabled'] else "\033[92mON\033[0m"
        online = "\033[92mOFF\033[0m" if not self.config['online_safe'] else "\033[93mON\033[0m"
        
        print(f"\ncheat {status}".ljust(30) + f"online-safe {online}")
        
        if not self.config['cheat_enabled']:
            print("\033[93mgame not running\033[0m")
        else:
            print("\033[92mgame running\033[0m")
        
        print()
    
    def display_values(self):
        """Display current cheat values"""
        print(f"power".ljust(20) + f"{self.config['power']:.2f} x")
        print(f"grip".ljust(20) + f"{self.config['grip']:.2f} x")
        print(f"roll_resistance".ljust(20) + f"{self.config['roll_resistance']:.2f} x")
        
        erode_status = "\033[92mON\033[0m" if self.config['erode'] else "\033[0mOFF\033[0m"
        print(f"erode".ljust(20) + f"{erode_status}".ljust(25) + "(stock erosion - 100% rut depth)")
        print()
    
    def display_help(self):
        """Display help menu"""
        print("\033[92m" + "=" * 70)
        print("COMMANDS:")
        print("=" * 70 + "\033[0m")
        print("  power <value>           Set power multiplier (1.00 - 3.00)")
        print("  grip <value>            Set grip multiplier (1.00 - 3.00)")
        print("  roll <value>            Set roll resistance (0.50 - 2.00)")
        print("  erode                   Toggle erode cheat ON/OFF")
        print("  start                   Start cheats (enable)")
        print("  stop                    Stop cheats (disable)")
        print("  save                    Save configuration")
        print("  reset                   Reset to defaults")
        print("  status                  Show current status")
        print("  keys                    Configure hotkeys")
        print("  export                  Export to Lua cheat file")
        print("  help                    Show this help menu")
        print("  quit                    Exit program")
        print("=" * 70)
        print()
    
    def display_keys(self):
        """Display hotkeys"""
        print("\033[92m" + "=" * 70)
        print("HOTKEYS (60% Keyboard Compatible):")
        print("=" * 70 + "\033[0m")
        print("  A  - Toggle cheat ON/OFF")
        print("  S  - Show status")
        print("  D  - Panic (disable all)")
        print("  Q  - Roll Resistance")
        print("  W  - Power Boost")
        print("  E  - Grip Boost")
        print("  R  - Erode/No Crash")
        print("=" * 70)
        print()
    
    def handle_command(self, command):
        """Handle user command"""
        parts = command.strip().split()
        
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == "power" and len(parts) > 1:
            try:
                value = float(parts[1])
                if 1.00 <= value <= 3.00:
                    self.config['power'] = round(value, 2)
                    print(f"\033[92m✓ Power set to {self.config['power']:.2f} x\033[0m\n")
                else:
                    print("\033[91m✗ Power must be between 1.00 and 3.00\033[0m\n")
            except ValueError:
                print("\033[91m✗ Invalid value\033[0m\n")
        
        elif cmd == "grip" and len(parts) > 1:
            try:
                value = float(parts[1])
                if 1.00 <= value <= 3.00:
                    self.config['grip'] = round(value, 2)
                    print(f"\033[92m✓ Grip set to {self.config['grip']:.2f} x\033[0m\n")
                else:
                    print("\033[91m✗ Grip must be between 1.00 and 3.00\033[0m\n")
            except ValueError:
                print("\033[91m✗ Invalid value\033[0m\n")
        
        elif cmd == "roll" and len(parts) > 1:
            try:
                value = float(parts[1])
                if 0.50 <= value <= 2.00:
                    self.config['roll_resistance'] = round(value, 2)
                    print(f"\033[92m✓ Roll Resistance set to {self.config['roll_resistance']:.2f} x\033[0m\n")
                else:
                    print("\033[91m✗ Roll Resistance must be between 0.50 and 2.00\033[0m\n")
            except ValueError:
                print("\033[91m✗ Invalid value\033[0m\n")
        
        elif cmd == "erode":
            self.config['erode'] = not self.config['erode']
            status = "\033[92mON\033[0m" if self.config['erode'] else "\033[0mOFF\033[0m"
            print(f"\033[92m✓ Erode set to {status}\033[0m\n")
        
        elif cmd == "start":
            self.config['cheat_enabled'] = True
            print("\033[92m✓ Cheats ENABLED\033[0m\n")
        
        elif cmd == "stop":
            self.config['cheat_enabled'] = False
            print("\033[91m✓ Cheats DISABLED\033[0m\n")
        
        elif cmd == "save":
            if self.save_config():
                print("\033[92m✓ Configuration saved!\033[0m\n")
            else:
                print("\033[91m✗ Failed to save configuration\033[0m\n")
        
        elif cmd == "reset":
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()
            print("\033[92m✓ Reset to defaults\033[0m\n")
        
        elif cmd == "status":
            self.display_status()
            self.display_values()
        
        elif cmd == "keys":
            self.display_keys()
        
        elif cmd == "export":
            self.export_lua()
        
        elif cmd == "help":
            self.display_help()
        
        elif cmd == "quit" or cmd == "exit":
            self.running = False
            print("\033[91mTurning cheat off and exiting...\033[0m")
        
        else:
            print("\033[91m✗ Unknown command. Type 'help' for commands.\033[0m\n")
    
    def export_lua(self):
        """Export to Lua cheat file"""
        lua_content = f"""-- MX Simulator Cheats Mod
-- Generated by NOX.CC CLI - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
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
            print("\033[92m✓ Successfully exported to cheats.lua!\033[0m\n")
            print("✓ Configured for 60% Keyboard - Press A to toggle cheats!\n")
        except Exception as e:
            print(f"\033[91m✗ Export failed: {e}\033[0m\n")
    
    def run(self):
        """Run the CLI"""
        self.display_header()
        self.display_status()
        self.display_values()
        
        print("Welcome. Two things to do before you start:")
        print("  1 Pick your hotkeys (next screen)")
        print("  2 after that, type 'help' if you want the full command list")
        print()
        print("\033[92mWelcome.\033[0m Pick the keys you want to use.")
        print("These work even when the game has focus.")
        print("press enter to keep · type 'none' to remove")
        print()
        print("  toggle cheat ON / OFF  [A] |")
        print()
        
        while self.running:
            try:
                command = input("\033[92mNOX.CC>\033[0m ").strip()
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\n\033[91mInterrupted. Exiting...\033[0m")
                self.running = False
            except Exception as e:
                print(f"\033[91m✗ Error: {e}\033[0m\n")

def main():
    nox = NOXCheats()
    nox.run()

if __name__ == "__main__":
    main()
