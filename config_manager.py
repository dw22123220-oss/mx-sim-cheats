#!/usr/bin/env python3
"""
MX Simulator Cheats Config Manager
Quickly edit cheat values from the terminal
"""

import json
import os
import sys

CONFIG_FILE = "cheats_config.json"

# Default config
DEFAULT_CONFIG = {
    "roll_resistance_multiplier": 0.5,
    "speed_boost_multiplier": 1.3,
    "grip_boost_multiplier": 1.2
}

def load_config():
    """Load config from JSON file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            print("Error reading config file, using defaults...")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save config to JSON file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print("✓ Config saved!")

def display_menu(config):
    """Display main menu"""
    print("\n" + "="*50)
    print("MX SIMULATOR CHEATS CONFIG MANAGER")
    print("="*50)
    print("\nCurrent Settings:")
    print(f"  1. Roll Resistance:  {config['roll_resistance_multiplier']} (0.1 - 1.0)")
    print(f"  2. Speed Boost:      {config['speed_boost_multiplier']} (1.0 - 2.0)")
    print(f"  3. Grip Boost:       {config['grip_boost_multiplier']} (1.0 - 2.0)")
    print("\nOptions:")
    print("  1-3 = Edit value")
    print("  4   = Reset to defaults")
    print("  5   = Export to cheats.lua")
    print("  Q   = Quit")
    print("="*50)

def edit_value(config, option):
    """Edit a specific value"""
    options = {
        '1': ('roll_resistance_multiplier', 0.1, 1.0, 'Roll Resistance'),
        '2': ('speed_boost_multiplier', 1.0, 2.0, 'Speed Boost'),
        '3': ('grip_boost_multiplier', 1.0, 2.0, 'Grip Boost')
    }
    
    if option not in options:
        print("Invalid option!")
        return
    
    key, min_val, max_val, name = options[option]
    print(f"\n{name} Multiplier")
    print(f"Current value: {config[key]}")
    print(f"Range: {min_val} - {max_val}")
    
    try:
        new_val = float(input("Enter new value: "))
        if min_val <= new_val <= max_val:
            config[key] = new_val
            print(f"✓ {name} set to {new_val}")
            save_config(config)
        else:
            print(f"Value must be between {min_val} and {max_val}!")
    except ValueError:
        print("Invalid input! Enter a number.")

def reset_config(config):
    """Reset to default values"""
    confirm = input("Reset all values to defaults? (y/n): ").lower()
    if confirm == 'y':
        config.update(DEFAULT_CONFIG)
        save_config(config)
        print("✓ Reset to defaults!")
    else:
        print("Cancelled.")

def export_to_lua(config):
    """Export config to cheats.lua format"""
    lua_content = f"""-- MX Simulator Cheats Mod
-- Features: Roll Resistance, Speed Boost, Grip Boost
-- Generated from config manager

-- Configuration
local ROLL_RESISTANCE_MULTIPLIER = {config['roll_resistance_multiplier']}  -- Lower = less roll resistance (0.1 - 1.0)
local SPEED_BOOST_MULTIPLIER = {config['speed_boost_multiplier']}      -- Higher = faster speed (1.0 - 2.0)
local GRIP_BOOST_MULTIPLIER = {config['grip_boost_multiplier']}       -- Higher = more grip (1.0 - 2.0)

-- Cheat States
local cheats = {{
    rollResistance = false,
    speedBoost = false,
    gripBoost = false
}}

-- Hotkeys
local TOGGLE_ROLL_RESISTANCE = 282  -- F1
local TOGGLE_SPEED_BOOST = 283      -- F2
local TOGGLE_GRIP_BOOST = 284       -- F3

-- Input detection
function update(dt)
    -- Check for F1 (Roll Resistance toggle)
    if isKeyPressed(TOGGLE_ROLL_RESISTANCE) then
        cheats.rollResistance = not cheats.rollResistance
        print("[MX Cheats] Roll Resistance: " .. (cheats.rollResistance and "ON" or "OFF"))
    end
    
    -- Check for F2 (Speed Boost toggle)
    if isKeyPressed(TOGGLE_SPEED_BOOST) then
        cheats.speedBoost = not cheats.speedBoost
        print("[MX Cheats] Speed Boost: " .. (cheats.speedBoost and "ON" or "OFF"))
    end
    
    -- Check for F3 (Grip Boost toggle)
    if isKeyPressed(TOGGLE_GRIP_BOOST) then
        cheats.gripBoost = not cheats.gripBoost
        print("[MX Cheats] Grip Boost: " .. (cheats.gripBoost and "ON" or "OFF"))
    end
    
    -- Apply cheats
    applyRollResistanceCheat(dt)
    applySpeedBoostCheat(dt)
    applyGripBoostCheat(dt)
end

-- Roll Resistance Cheat
function applyRollResistanceCheat(dt)
    if not cheats.rollResistance then return end
    
    local bike = getBike()
    if bike then
        -- Reduce roll resistance
        bike.rollResistance = bike.rollResistance * ROLL_RESISTANCE_MULTIPLIER
    end
end

-- Speed Boost Cheat
function applySpeedBoostCheat(dt)
    if not cheats.speedBoost then return end
    
    local bike = getBike()
    if bike then
        -- Increase engine power
        bike.enginePower = bike.enginePower * SPEED_BOOST_MULTIPLIER
        
        -- Increase velocity slightly
        if bike.velocity then
            bike.velocity = bike.velocity * (1 + (SPEED_BOOST_MULTIPLIER - 1) * 0.5)
        end
    end
end

-- Grip Boost Cheat
function applyGripBoostCheat(dt)
    if not cheats.gripBoost then return end
    
    local bike = getBike()
    if bike then
        -- Increase tire grip
        if bike.tires then
            bike.tires.grip = bike.tires.grip * GRIP_BOOST_MULTIPLIER
            bike.tires.traction = bike.tires.traction * GRIP_BOOST_MULTIPLIER
        end
        
        -- Improve handling
        bike.handling = bike.handling * GRIP_BOOST_MULTIPLIER
    end
end

-- Helper function to get bike object
function getBike()
    -- This will depend on MX Simulator's API
    -- Adjust based on actual game object structure
    if game and game.player and game.player.bike then
        return game.player.bike
    end
    return nil
end

-- Helper function to detect key press
function isKeyPressed(keyCode)
    -- Implementation depends on MX Simulator's input system
    -- This is a placeholder - adjust to match actual API
    if input and input.isKeyPressed then
        return input.isKeyPressed(keyCode)
    end
    return false
end

-- Initialize
print("[MX Cheats] Mod loaded!")
print("[MX Cheats] F1 = Roll Resistance | F2 = Speed Boost | F3 = Grip Boost")
"""
    
    with open('cheats.lua', 'w') as f:
        f.write(lua_content)
    print("✓ Exported to cheats.lua!")

def main():
    """Main application loop"""
    config = load_config()
    
    while True:
        display_menu(config)
        choice = input("\nEnter option: ").strip().upper()
        
        if choice == 'Q':
            print("Goodbye!")
            sys.exit(0)
        elif choice in ['1', '2', '3']:
            edit_value(config, choice)
        elif choice == '4':
            reset_config(config)
        elif choice == '5':
            export_to_lua(config)
        else:
            print("Invalid option!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
