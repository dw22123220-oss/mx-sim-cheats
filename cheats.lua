-- MX Simulator Cheats Mod
-- Features: Roll Resistance, Speed Boost, Grip Boost

-- Configuration
local ROLL_RESISTANCE_MULTIPLIER = 0.5  -- Lower = less roll resistance (0.1 - 1.0)
local SPEED_BOOST_MULTIPLIER = 2.0      -- Higher = faster speed (1.0 - 2.0) - MAXIMUM SPEED!
local GRIP_BOOST_MULTIPLIER = 1.2       -- Higher = more grip (1.0 - 2.0)

-- Cheat States
local cheats = {
    rollResistance = false,
    speedBoost = false,
    gripBoost = false
}

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
        
        -- Increase velocity significantly
        if bike.velocity then
            bike.velocity = bike.velocity * (1 + (SPEED_BOOST_MULTIPLIER - 1) * 0.75)
        end
        
        -- Increase top speed
        if bike.maxSpeed then
            bike.maxSpeed = bike.maxSpeed * SPEED_BOOST_MULTIPLIER
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
