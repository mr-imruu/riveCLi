-- Confident line-art mascot. The scene is data bound to view model numbers; this
-- script turns the pointer into those numbers and never touches the scene graph.
--
-- Split of work:
--   this script   : cursor follow (eyes, face, head, hair), blink, hop, which phrase
--                   he says and for how long
--   state machine : hover listener -> Hover layer (brows, eyes, grin); `speaking`
--                   -> Mouth layer (flap) and Bubble layer (pop in)

local NAMES = {
    'faceX', 'faceY', 'headRot', 'headY', 'headSX', 'headSY', 'hairRot', 'lookX', 'lookY',
    'eyeSY', 'bodyY', 'p0', 'p1', 'p2', 'p3', 'p4',
}
local PHRASES = 5
local CX, CY = 250, 250

type Mascot = {
    size: Vector,
    vm: { [string]: Property<number> },
    hoverProp: Property<boolean>?,
    speakingProp: Property<boolean>?,
    wasHover: boolean,
    ready: boolean,
    time: number,
    -- pointer
    px: number, py: number, havePointer: boolean,
    lx: number, ly: number, -- smoothed look, -1..1
    -- hover
    cooldown: number,
    -- speech
    phrase: number, speak: number,
    -- hop spring
    hop: number, hopV: number,
    -- hair spring
    hair: number, hairV: number,
    -- blink
    blinkIn: number, blinkT: number,
}

local function clamp(v: number, lo: number, hi: number): number
    return math.max(lo, math.min(hi, v))
end

local function set(self: Mascot, name: string, v: number)
    local p = self.vm[name]
    if p ~= nil then
        p.value = v
    end
end

local function say(self: Mascot)
    local nxt = math.random(0, PHRASES - 1)
    if nxt == self.phrase then
        nxt = (nxt + 1) % PHRASES
    end
    self.phrase = nxt
    self.speak = 2.4
    self.cooldown = 1.2
end

function init(self: Mascot, context: Context): boolean
    -- init runs twice and the view model is absent the first time.
    local vm = context:viewModel()
    if vm == nil then
        return true
    end
    for _, n in NAMES do
        local p = vm:getNumber(n)
        if p ~= nil then
            self.vm[n] = p
        end
    end
    self.hoverProp = vm:getBoolean('hover')
    self.speakingProp = vm:getBoolean('speaking')
    self.ready = true
    return true
end

function resize(self: Mascot, size: Vector)
    self.size = size
end

function pointerMove(self: Mascot, event: PointerEvent)
    self.px = event.position.x
    self.py = event.position.y
    self.havePointer = true
end

function pointerExit(self: Mascot, event: PointerEvent)
    self.havePointer = false
end

function pointerDown(self: Mascot, event: PointerEvent)
    self.px = event.position.x
    self.py = event.position.y
    self.havePointer = true
    self.hopV = -420
    say(self)
end

function advance(self: Mascot, dt: number): boolean
    if not self.ready then
        return true
    end
    dt = math.min(dt, 1 / 20)
    self.time += dt
    local t = self.time

    -- Where is he looking? Idle: a lazy wander so he is alive before you arrive.
    local tx, ty = self.px, self.py
    if not self.havePointer then
        tx = CX + 190 * math.sin(t * 0.55)
        ty = CY + 70 * math.sin(t * 0.83 + 1.0)
    end
    local nx = clamp((tx - CX) / 220, -1, 1)
    local ny = clamp((ty - CY) / 220, -1, 1)
    local k = 1 - math.exp(-11 * dt)
    self.lx += (nx - self.lx) * k
    self.ly += (ny - self.ly) * k

    -- Hover is written by the state machine's listener; we only react to the edge.
    self.cooldown = math.max(0, self.cooldown - dt)
    local over = self.hoverProp ~= nil and self.hoverProp.value
    if over and not self.wasHover and self.cooldown <= 0 then
        say(self)
    end
    self.wasHover = over

    -- `speaking` drives the Mouth and Bubble layers.
    self.speak = math.max(0, self.speak - dt)
    if self.speakingProp ~= nil then
        local want = self.speak > 0
        if self.speakingProp.value ~= want then
            self.speakingProp.value = want
        end
    end

    -- Hop spring (click / reaction): negative = up.
    self.hopV += (-self.hop) * 300 * dt
    self.hopV -= self.hopV * 13 * dt
    self.hop += self.hopV * dt

    -- Blink.
    self.blinkIn -= dt
    if self.blinkIn <= 0 and self.blinkT <= 0 then
        self.blinkT = 0.16
        self.blinkIn = 2 + math.random() * 3.5
    end
    local blink = 1
    if self.blinkT > 0 then
        local ph = 1 - self.blinkT / 0.16
        blink = 1 - 0.92 * math.sin(math.pi * ph)
        self.blinkT -= dt
    end

    -- Head.
    local breathe = math.sin(t * 1.9)
    local headRot = self.lx * 0.13 + math.sin(t * 0.7) * 0.012
    local headY = CY + self.ly * 7 + breathe * 2.2 + self.hop
    local stretch = clamp(-self.hop * 0.0035, -0.25, 0.25)
    set(self, 'headRot', headRot)
    set(self, 'headY', headY)
    set(self, 'headSX', 1 - stretch * 0.6)
    set(self, 'headSY', 1 + stretch)
    set(self, 'faceX', self.lx * 15)
    set(self, 'faceY', self.ly * 9)
    set(self, 'bodyY', CY + breathe * 1.2)

    -- Hair lags behind the head.
    self.hairV += (-headRot * 0.9 - self.hair) * 180 * dt
    self.hairV -= self.hairV * 9 * dt
    self.hair += self.hairV * dt
    set(self, 'hairRot', self.hair + math.sin(t * 2.3) * 0.015)

    -- Eyes follow the pointer; the state machine widens them on hover.
    set(self, 'lookX', self.lx * 9)
    set(self, 'lookY', self.ly * 6)
    set(self, 'eyeSY', blink)

    for i = 0, PHRASES - 1 do
        set(self, 'p' .. i, if i == self.phrase then 1 else 0)
    end
    return true
end

return function(context: Context): Layout<Mascot>
    return {
        size = Vector.xy(0, 0),
        vm = {},
        ready = false,
        time = 0,
        px = CX, py = CY, havePointer = false,
        lx = 0, ly = 0,
        hoverProp = nil, speakingProp = nil, wasHover = false,
        cooldown = 0,
        phrase = 0, speak = 0,
        hop = 0, hopV = 0,
        hair = 0, hairV = 0,
        blinkIn = 2, blinkT = 0,
        init = init,
        resize = resize,
        advance = advance,
        pointerMove = pointerMove,
        pointerExit = pointerExit,
        pointerDown = pointerDown,
    }
end
