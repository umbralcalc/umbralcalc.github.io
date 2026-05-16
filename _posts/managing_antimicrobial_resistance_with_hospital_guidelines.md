---
title: "Managing antimicrobial resistance (AMR) with hospital guidelines"
tag: "Acting on Simulated Systems"
series-blurb: "A collection of simulated examples of real-world actions explored through interactive dashboards. Each post is devoted to a specific real-world decision problem in turn, and walks through how to play with the dashboard to discover the best action. No maths, just diagrams and straightforward descriptions all the way through."
order: 2
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/managing_antimicrobial_resistance_with_hospital_guidelines/antimicrobial-resistance-code.svg"
---

# Managing antimicrobial resistance (AMR) with hospital guidelines
<div style="height:0.75em;"></div>

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/dashboard-disclaimer.svg" width="700"/></center>

Antibiotic-resistant infections are rising in English hospitals: can stewardship policies bring them back down, and how much room is there to do so?

The simulation below is fitted to ten years of UKHSA surveillance data and models how cephalosporin prescribing pressure shapes the balance of susceptible and resistant E. coli inside a hospital, generating bloodstream infections as a stochastic consequence.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/managing_antimicrobial_resistance_with_hospital_guidelines/antimicrobial-resistance-code.svg" width="400"/></center>

Pick a prescribing policy and watch how the resistance ratio and resistant infection burden evolve over time.

```{=html}
<div id="dexetera-amr" class="dexetera-widget">
<style>
#dexetera-amr { font-family: system-ui, -apple-system, sans-serif; color: #2c3e50; line-height: 1.5; }
#dexetera-amr .description { margin: 0 0 1em; color: #2c3e50; opacity: 0.85; font-size: 1rem; }
#dexetera-amr code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.95em; background: rgba(60,120,216,0.08); padding: 0.05em 0.3em; border-radius: 3px; }
#dexetera-amr .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 0.9em; }
#dexetera-amr .panel { border: 1px solid #2c3e50; border-radius: 6px; padding: 0.8em 0.9em; background: #ffffff; display: flex; flex-direction: column; gap: 0.6em; box-sizing: border-box; }
#dexetera-amr .panel-title { font-weight: 600; color: #2c3e50; font-size: 1rem; }
#dexetera-amr canvas { display: block; width: 100%; max-width: 640px; height: auto; aspect-ratio: 640 / 400; margin: 0 auto; background: #ffffff; }
#dexetera-amr .panel-readout { margin: 0; font-size: 1rem; color: #2c3e50; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-amr .slider { display: grid; grid-template-columns: 1fr 80px; grid-template-areas: "name readout" "input input"; align-items: center; gap: 0.3em 1em; font-size: 1rem; }
#dexetera-amr .slider-name { grid-area: name; color: #2c3e50; }
#dexetera-amr .slider input[type="range"] { grid-area: input; width: 100%; accent-color: #b0447a; }
#dexetera-amr .slider-readout { grid-area: readout; text-align: right; color: #b0447a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-amr .panel-actions { display: flex; flex-wrap: wrap; gap: 0.6em; margin-top: 0.4em; }
#dexetera-amr button.button-secondary { cursor: pointer; border: 1px solid #2c3e50; background: #ffffff; color: #2c3e50; padding: 0.4em 0.85em; border-radius: 6px; font-size: 1rem; font-family: inherit; }
#dexetera-amr button.button-secondary:hover { background: #f4f6f9; }
#dexetera-amr .status { margin: 1em 0 0; text-align: right; font-size: 0.9em; color: #2c3e50; opacity: 0.6; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-amr .canvas-caption { margin: 0; font-size: 0.85rem; color: #2c3e50; opacity: 0.75; text-align: center; }#dexetera-amr .canvas-caption-top { margin-bottom: 0.1em; }#dexetera-amr .canvas-caption-mid { margin: 0.2em 0 0.1em; }#dexetera-amr .canvas-caption-cmp { margin: 0.4em 0 0.1em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; opacity: 0.6; }#dexetera-amr .policy-selector { display: flex; flex-direction: column; gap: 0.4em; font-size: 1rem; margin-bottom: 0.2em; }#dexetera-amr .policy-selector-label { color: #2c3e50; font-weight: 600; }#dexetera-amr .policy-options { display: flex; flex-direction: column; gap: 0.3em; }#dexetera-amr .policy-options label { display: flex; align-items: center; gap: 0.4em; color: #2c3e50; cursor: pointer; }#dexetera-amr .policy-options input[type="radio"] { accent-color: #b0447a; }#dexetera-amr .policy-conditional { display: none; }#dexetera-amr .policy-conditional.is-active { display: block; }#dexetera-amr .policy-empty-note { color: #2c3e50; opacity: 0.65; font-size: 0.9rem; font-style: italic; }</style>
<p class="description">Hospital prescribing policy support: pick a stewardship strategy and policy parameters; the simulator (fitted to UKHSA surveillance data) shows the resulting resistance ratio and the cumulative burden of resistant bloodstream infections over 50 years. This is a research model fitted to surveillance data, not a clinical decision aid.</p>
<div class="dashboard">
    <section class="panel">
        <div class="panel-title">Simulation</div>
        <p class="canvas-caption canvas-caption-top">Resistance ratio over time (auto-scaled)</p><canvas width="640" height="400"></canvas><p class="canvas-caption canvas-caption-mid">Cumulative resistant BSI over 50 years</p><p class="canvas-caption canvas-caption-cmp">Comparison: your policy (magenta) vs the four reference policies (grey)</p>
        
        <p class="panel-readout" data-readout="display_counts">&nbsp;</p>
        
        <p class="panel-readout" data-readout="display_rates">&nbsp;</p>
        
    </section>
    
    <section class="panel">
        <div class="panel-title">Live controls</div>
        
        <div class="policy-selector"><span class="policy-selector-label">Prescribing policy</span><div class="policy-options"><label><input type="radio" name="amr-policy" value="0" checked>Baseline (constant)</label><label><input type="radio" name="amr-policy" value="1">Cycling (alternate)</label><label><input type="radio" name="amr-policy" value="2">Threshold (escalate)</label><label><input type="radio" name="amr-policy" value="3">Restriction (ramp)</label></div><input type="range" data-slider="policy" min="0" max="3" step="1" value="0" style="display:none"><span data-slider-readout="policy" style="display:none"></span></div>
        
        <div class="policy-conditional" data-policy="1"><label class="slider">
            <span class="slider-name">Cycling period (timesteps)</span>
            <input type="range" data-slider="cycle_period"
                   min="1" max="52" step="1" value="13">
            <span class="slider-readout" data-slider-readout="cycle_period">&nbsp;</span>
        </label></div>
        
        <div class="policy-conditional" data-policy="2"><label class="slider">
            <span class="slider-name">Threshold resistance fraction</span>
            <input type="range" data-slider="threshold"
                   min="0.05" max="0.5" step="0.01" value="0.15">
            <span class="slider-readout" data-slider-readout="threshold">&nbsp;</span>
        </label></div>
        
        <div class="policy-conditional" data-policy="3"><label class="slider">
            <span class="slider-name">Restriction ramp (timesteps)</span>
            <input type="range" data-slider="ramp_period"
                   min="4" max="104" step="1" value="26">
            <span class="slider-readout" data-slider-readout="ramp_period">&nbsp;</span>
        </label></div>
        
        
        <div class="panel-actions">
            <div class="policy-conditional" data-policy="0"><p class="policy-empty-note">Baseline uses a constant prescribing rate — no extra parameters to tune.</p></div><button type="button" class="button-secondary" data-reset>Reset simulation</button>
        </div>
        
    </section>
    
</div>
<p class="status" data-status>Loading…</p>
</div>
<script>
(function () {
    var widget = document.getElementById('dexetera-amr');
    var RUNTIME_BASE = 'https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/dexetera/runtime/';
    var WASM_URL = 'https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/dexetera/widgets/amr/main.wasm';
    var gameConfig = {"visualization":{"backgroundColor":"#fafafa","canvasHeight":400,"canvasWidth":640,"renderers":[{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":60,"x2":580,"y1":126,"y2":126},"type":"line"},{"partitionName":"resistance_ratio","properties":{"color":"#3c78d8","height":90,"lineWidth":2,"width":520,"x":60,"y":36},"type":"lineChart"},{"partitionName":"","properties":{"color":"#e3e6ec","width":1,"x1":60,"x2":580,"y1":144,"y2":144},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":60,"x2":580,"y1":216,"y2":216},"type":"line"},{"partitionName":"cumulative_bsi","properties":{"color":"#3c78d8","height":60,"lineWidth":2,"width":520,"x":60,"y":156},"type":"lineChart"},{"partitionName":"","properties":{"color":"#e3e6ec","width":1,"x1":60,"x2":580,"y1":222,"y2":222},"type":"line"},{"partitionName":"reference_bars","properties":{"anchor":"topLeft","defaultHeight":0,"defaultWidth":0,"fillColor":"#7d8aa1"},"type":"rectangleSet"},{"partitionName":"user_bar","properties":{"anchor":"topLeft","defaultHeight":0,"defaultWidth":0,"fillColor":"#b0447a"},"type":"rectangleSet"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"Baseline","textAlign":"right","x":212,"y":258},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"Cycling","textAlign":"right","x":212,"y":286},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"Threshold","textAlign":"right","x":212,"y":314},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"Restriction","textAlign":"right","x":212,"y":342},"type":"text"},{"partitionName":"","properties":{"color":"#b0447a","fontSize":18,"text":"Your policy","textAlign":"right","x":212,"y":370},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"187","textAlign":"left","x":488,"y":258},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"166","textAlign":"left","x":488,"y":286},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"153","textAlign":"left","x":488,"y":314},"type":"text"},{"partitionName":"","properties":{"color":"#2c3e50","fontSize":18,"text":"152","textAlign":"left","x":488,"y":342},"type":"text"},{"partitionName":"cumulative_bsi","properties":{"color":"#b0447a","fontSize":18,"text":"{value}","textAlign":"left","x":488,"y":370},"type":"text"}],"updateIntervalMs":0},"sliders":[{"name":"policy","partition":"policy_action","valueIndex":0,"default":0,"decimals":3},{"name":"cycle_period","partition":"policy_action","valueIndex":1,"default":13,"decimals":3},{"name":"threshold","partition":"policy_action","valueIndex":2,"default":0.15,"decimals":2},{"name":"ramp_period","partition":"policy_action","valueIndex":3,"default":26,"decimals":3}],"readouts":[{"partition":"display_counts","template":"year {v0} of 50 · cumulative R BSI {v2}","decimals":0},{"partition":"display_rates","template":"ceph rate {v0} · R fraction {v1}","decimals":3}],"showReset":true,"driver":{"kind":"inline","options":{"intervalMs":30}}};

    // Load the renderer script lazily, sharing one promise across every
    // dexetera widget on the same page.
    function ensureRenderer() {
        if (self.dexetera && self.dexetera.createRenderer) return Promise.resolve();
        if (self.__dexeteraLoading) return self.__dexeteraLoading;
        self.__dexeteraLoading = new Promise(function (resolve, reject) {
            var s = document.createElement('script');
            s.src = RUNTIME_BASE + 'renderer.js';
            s.onload = function () { resolve(); };
            s.onerror = function () { reject(new Error('failed to load ' + s.src)); };
            document.head.appendChild(s);
        });
        return self.__dexeteraLoading;
    }

    function $(sel) { return widget.querySelector(sel); }
    function $$(sel) { return widget.querySelectorAll(sel); }

    function setStatus(msg) {
        var el = $('[data-status]');
        if (el) el.textContent = msg;
    }

    var slidersByPartition = (function () {
        var grouped = {};
        for (var i = 0; i < gameConfig.sliders.length; i++) {
            var s = gameConfig.sliders[i];
            if (!grouped[s.partition]) grouped[s.partition] = [];
            grouped[s.partition].push(s);
        }
        return grouped;
    })();

    var worker = null;

    function publishActions() {
        for (var i = 0; i < gameConfig.sliders.length; i++) {
            var s = gameConfig.sliders[i];
            var input = $('[data-slider="' + s.name + '"]');
            var ro = $('[data-slider-readout="' + s.name + '"]');
            if (input && ro) ro.textContent = parseFloat(input.value).toFixed(s.decimals);
        }
        if (!worker) return;
        var partitions = {};
        for (var partition in slidersByPartition) {
            if (!Object.prototype.hasOwnProperty.call(slidersByPartition, partition)) continue;
            var group = slidersByPartition[partition];
            var maxIdx = -1;
            for (var j = 0; j < group.length; j++) maxIdx = Math.max(maxIdx, group[j].valueIndex);
            var values = new Array(maxIdx + 1);
            for (var k = 0; k <= maxIdx; k++) values[k] = 0;
            for (var l = 0; l < group.length; l++) {
                var sl = group[l];
                var inp = $('[data-slider="' + sl.name + '"]');
                values[sl.valueIndex] = parseFloat(inp ? inp.value : sl.default);
            }
            partitions[partition] = values;
        }
        worker.postMessage({ action: 'setActions', partitions: partitions });
    }

    function applyReadout(template, decimals, partitionState) {
        var s = template;
        s = s.replace(/\{t\}/g, Math.floor(partitionState.timesteps));
        s = s.replace(/\{v(\d*)\}/g, function (_, idx) {
            var i = idx === '' ? 0 : parseInt(idx, 10);
            var v = partitionState.state.values[i];
            return (v === undefined) ? '' : v.toFixed(decimals);
        });
        return s;
    }

    function ensureWorkerUrl() {
        if (self.__dexeteraWorkerUrl) return Promise.resolve(self.__dexeteraWorkerUrl);
        if (self.__dexeteraWorkerLoading) return self.__dexeteraWorkerLoading;
        self.__dexeteraWorkerLoading = fetch(RUNTIME_BASE + 'worker.js')
            .then(function (r) {
                if (!r.ok) throw new Error('failed to fetch worker.js: ' + r.status);
                return r.text();
            })
            .then(function (src) {
                var shim = '(function(){var BASE=' + JSON.stringify(RUNTIME_BASE) +
                    ';var orig=self.importScripts;self.importScripts=function(){' +
                    'var args=Array.prototype.map.call(arguments,function(u){' +
                    'return new URL(u,BASE).href;});return orig.apply(self,args);};})();\n';
                var blob = new Blob([shim, src], { type: 'application/javascript' });
                self.__dexeteraWorkerUrl = URL.createObjectURL(blob);
                return self.__dexeteraWorkerUrl;
            });
        return self.__dexeteraWorkerLoading;
    }

    function startWorker(renderer) {
        if (worker) worker.terminate();
        ensureWorkerUrl().then(function (workerUrl) {
        worker = new Worker(workerUrl);
        worker.onmessage = function (e) {
            var msg = e.data;
            if (msg.type === 'partitionState') {
                renderer.update(msg.data);
                renderer.render();
                for (var i = 0; i < gameConfig.readouts.length; i++) {
                    var r = gameConfig.readouts[i];
                    if (r.partition !== msg.data.partitionName) continue;
                    var el = $('[data-readout="' + r.partition + '"]');
                    if (el) el.textContent = applyReadout(r.template, r.decimals, msg.data);
                }
                if (worker && msg.data.timesteps >= 200) { worker.terminate(); worker = null; setStatus('Year 50 reached. Use Reset to rerun.'); }
            } else if (msg.type === 'status') {
                setStatus(msg.data);
                if (msg.data === 'inline driver ready') publishActions();
            } else if (msg.type === 'error') {
                console.error('dexetera worker error:', msg.data);
                setStatus('Error: ' + msg.data);
            }
        };
        worker.onerror = function (err) {
            console.error('dexetera worker error:', err);
            setStatus('Worker error: ' + err.message);
        };
        worker.postMessage({
            action: 'start',
            wasmBinary: new URL(WASM_URL, document.baseURI).href,
            driver: gameConfig.driver,
        });
        publishActions();
        }).catch(function (err) {
            console.error(err);
            setStatus('Failed to load dexetera worker: ' + err.message);
        });
    }

    ensureRenderer().then(function () {
        var canvas = $('canvas');
        var renderer = self.dexetera.createRenderer(canvas, gameConfig.visualization);

        for (var i = 0; i < gameConfig.sliders.length; i++) {
            var s = gameConfig.sliders[i];
            var el = $('[data-slider="' + s.name + '"]');
            if (el) el.addEventListener('input', publishActions);
        }
        if (gameConfig.showReset) {
            var btn = $('[data-reset]');
            if (btn) btn.addEventListener('click', function () { startWorker(renderer); });
        }
        publishActions();
        startWorker(renderer);
    }).catch(function (err) {
        console.error(err);
        setStatus('Failed to load dexetera runtime: ' + err.message);
    });
})();
</script>

<script>
(function () {
    var widget = document.getElementById('dexetera-amr');
    if (!widget) return;
    var radios = widget.querySelectorAll('input[name="amr-policy"]');
    var slider = widget.querySelector('[data-slider="policy"]');
    var conditionals = widget.querySelectorAll('.policy-conditional');
    var resetBtn = widget.querySelector('[data-reset]');

    function applyPolicy(value) {
        if (slider) {
            slider.value = String(value);
            slider.dispatchEvent(new Event('input', { bubbles: true }));
        }
        for (var i = 0; i < conditionals.length; i++) {
            var c = conditionals[i];
            if (c.getAttribute('data-policy') === String(value)) {
                c.classList.add('is-active');
            } else {
                c.classList.remove('is-active');
            }
        }
    }

    // Each radio button change re-runs the simulation from t=0 with the
    // newly-chosen policy. The hidden slider's value is set first so that
    // the reset's publishActions() picks up the right policy on the new
    // worker's very first setActions message; the Reset click then
    // terminates any in-flight worker and spins up a fresh one. Without
    // this, the simulation only ever runs once (or whatever was selected
    // when Reset was last clicked), which is the trap the rugby
    // dashboard avoids by not having a categorical choice at all.
    for (var i = 0; i < radios.length; i++) {
        radios[i].addEventListener('change', function (e) {
            applyPolicy(parseInt(e.target.value, 10));
            if (resetBtn) resetBtn.click();
        });
    }
    var initial = 0;
    for (var j = 0; j < radios.length; j++) {
        if (radios[j].checked) { initial = parseInt(radios[j].value, 10); break; }
    }
    // Initial state — sync the slider + conditional visibility but do
    // NOT click Reset (the dexetera IIFE handles the very first sim
    // start; clicking Reset on init would race the renderer load).
    applyPolicy(initial);
})();
</script>
```

The link to this project can be [found here](https://github.com/umbralcalc/antimicrobial-resistance).