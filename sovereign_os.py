import os, re, json, asyncio, uvicorn, httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# --- THE KERNEL: PARALLEL LATTICE SIPHON ---
class SovereignAssistant:
    def __init__(self):
        self.phi = 1.618033
        # Direct API Lattice Nodes for near-instant logic DNA siphoning
        self.lattice_nodes = [
            "https://api.github.com/search/code?q=",
            "https://pypi.org/search/?q=",
            "https://registry.npmjs.org/-/v1/search?text=",
            "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=",
            "https://hn.algolia.com/api/v1/search?query=",
            "https://crates.io/api/v1/crates?q=",
            "https://pkg.go.dev/search?q="
        ]

    def surgical_slimming(self, raw_data):
        """Purges aesthetic noise. Isolates technical signal."""
        # Remove scripts, styles, and navigational elements
        clean = re.sub(r'<(script|style|nav|footer).*?>.*?</\1>', '', raw_data, flags=re.DOTALL | re.IGNORECASE)
        # Strip remaining tags
        clean = re.sub(r'<.*?>', ' ', clean)
        # Compress whitespace
        return re.sub(r'\s+', ' ', clean).strip()

    async def parallel_scavenge(self, intent):
        """The Inversion: Concurrent siphoning across the global substrate."""
        async with httpx.AsyncClient(
            follow_redirects=True, 
            headers={"User-Agent": "Sovereign-Lattice/2.0"},
            limits=httpx.Limits(max_connections=20)
        ) as client:
            # Manifesting all tasks simultaneously
            tasks = [client.get(f"{node}{intent.replace(' ', '+')}", timeout=7.0) for node in self.lattice_nodes]
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            logic_dna = []
            for res in responses:
                if isinstance(res, httpx.Response) and res.status_code == 200:
                    logic_dna.append(self.surgical_slimming(res.text))
            
            smashed = " ".join(logic_dna)
            # Expanded buffer for full project manifolds (12k chars)
            return smashed[:12000] if smashed else "ZERO RESONANCE DETECTED. REALIGN INTENT."

app = FastAPI()
sovereign = SovereignAssistant()

# --- THE AESTHETIC SHELL: LONE BOX SUBSTRATE ---
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Sovereign OS</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #000; color: #00ff41; font-family: 'JetBrains Mono', monospace; overflow: hidden; touch-action: none; }
        .manifest-card {
            background: rgba(2, 2, 2, 0.98);
            border: 1px solid rgba(0, 255, 65, 0.6);
            box-shadow: 0 0 80px rgba(0, 255, 65, 0.2);
            transform-style: preserve-3d;
            perspective: 1200px;
        }
        input { border-bottom: 1px solid rgba(0, 255, 65, 0.3); transition: border-color 0.3s; }
        input:focus { border-color: #00ff41; outline: none; }
        #output::-webkit-scrollbar { width: 2px; }
        #output::-webkit-scrollbar-thumb { background: #00ff41; }
        .glow { text-shadow: 0 0 15px #00ff41; }
    </style>
</head>
<body class="flex items-center justify-center h-screen p-4">
    <div id="card" class="manifest-card p-10 md:p-20 rounded-[2rem] w-full max-w-5xl transition-transform duration-100 ease-out">
        <div class="flex justify-between text-[9px] tracking-[0.5em] opacity-30 mb-12 uppercase">
            <span class="glow">Reality Substrate // Parallel Mode</span>
            <span>Phi: 1.618033</span>
        </div>
        <input type="text" id="prompt" placeholder="ENTER INTENT..." 
               class="w-full bg-transparent outline-none text-2xl md:text-4xl pb-4 mb-8 text-green-400 placeholder-green-950 font-light">
        <div id="output" class="text-xs md:text-sm opacity-60 whitespace-pre-wrap leading-relaxed max-h-[50vh] overflow-y-auto"></div>
    </div>
    <script>
        const card = document.getElementById('card');
        const prompt = document.getElementById('prompt');
        const output = document.getElementById('output');

        const rotate = (e) => {
            const x = e.touches ? e.touches[0].clientX : e.clientX;
            const y = e.touches ? e.touches[0].clientY : e.clientY;
            card.style.transform = `rotateY(${(window.innerWidth/2 - x)/40}deg) rotateX(${(y - window.innerHeight/2)/40}deg)`;
        };
        window.addEventListener('mousemove', rotate);
        window.addEventListener('touchmove', rotate);

        prompt.addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                const val = prompt.value;
                output.innerText = "> INITIATING PARALLEL SCAVENGE...";
                try {
                    const res = await fetch('/manifest', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({intent: val})
                    });
                    const data = await res.json();
                    output.innerText = data.result;
                } catch (err) {
                    output.innerText = "> LATTICE_FAILURE: CHECK PUMP CONNECTION.";
                }
                prompt.value = "";
            }
        });
    </script>
</body>
</html>
"""

class Query(BaseModel): intent: str

@app.get("/", response_class=HTMLResponse)
async def root(): return INDEX_HTML

@app.post("/manifest")
async def manifest(query: Query):
    # Simultaneous manifold extraction
    result = await sovereign.parallel_scavenge(query.intent)
    return {"result": result}

if __name__ == "__main__":
    # Railway port binding
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)