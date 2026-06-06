---
title: "Evaluating rugby manager decision-making"
tag: "Acting on Simulated Systems"
series-blurb: "A collection of simulated examples of real-world actions explored through interactive dashboards. Each post covers a specific real-world decision problem in turn, demonstrating how simulations can inform real-world action-taking with illustrative (not production-ready) research models. No maths; just diagrams and straightforward descriptions all the way through."
order: 1
images:
- "https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/evaluating_rugby_manager_decision_making/trywizard-simulation-code.svg"
---

# Evaluating rugby manager decision-making
<div style="height:0.75em;"></div>

A rugby manager picks when to substitute each position group: bring on the front-row replacements early, or save them for the closing minutes?

The simulation below is fitted to thousands of real match events and treats every minute of a match as a model that learns the rate at which scoring events happen, minute by minute whose intensity depends on which players are on the pitch and how long they have been there.

<center><img src="https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/evaluating_rugby_manager_decision_making/trywizard-simulation-code.svg" width="700"/></center>

Drag the substitution-timing sliders for each position group and watch how the predicted win probability shifts.

```{=html}
<div id="dexetera-rugby" class="dexetera-widget">
<style>
#dexetera-rugby { font-family: system-ui, -apple-system, sans-serif; color: #2c3e50; line-height: 1.5; }
#dexetera-rugby .description { margin: 0 0 1em; color: #2c3e50; opacity: 0.85; font-size: 1rem; }
#dexetera-rugby code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.95em; background: rgba(60,120,216,0.08); padding: 0.05em 0.3em; border-radius: 3px; }
#dexetera-rugby .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 0.9em; }
#dexetera-rugby .panel { border: 1px solid #2c3e50; border-radius: 6px; padding: 0.8em 0.9em; background: #ffffff; display: flex; flex-direction: column; gap: 0.6em; box-sizing: border-box; }
#dexetera-rugby .panel-title { font-weight: 600; color: #2c3e50; font-size: 1rem; }
#dexetera-rugby canvas { display: block; width: 100%; max-width: 640px; height: auto; aspect-ratio: 640 / 400; margin: 0 auto; background: #ffffff; }
#dexetera-rugby .panel-readout { margin: 0; font-size: 1rem; color: #2c3e50; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-rugby .slider { display: grid; grid-template-columns: 1fr 80px; grid-template-areas: "name readout" "input input"; align-items: center; gap: 0.3em 1em; font-size: 1rem; }
#dexetera-rugby .slider-name { grid-area: name; color: #2c3e50; }
#dexetera-rugby .slider input[type="range"] { grid-area: input; width: 100%; accent-color: #b0447a; }
#dexetera-rugby .slider-readout { grid-area: readout; text-align: right; color: #b0447a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-rugby .panel-actions { display: flex; flex-wrap: wrap; gap: 0.6em; margin-top: 0.4em; }
#dexetera-rugby button.button-secondary { cursor: pointer; border: 1px solid #2c3e50; background: #ffffff; color: #2c3e50; padding: 0.4em 0.85em; border-radius: 6px; font-size: 1rem; font-family: inherit; }
#dexetera-rugby button.button-secondary:hover { background: #f4f6f9; }
#dexetera-rugby .status { margin: 1em 0 0; text-align: right; font-size: 0.9em; color: #2c3e50; opacity: 0.6; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
#dexetera-rugby .canvas-caption { margin: 0; font-size: 0.85rem; color: #2c3e50; opacity: 0.75; text-align: center; }#dexetera-rugby .canvas-caption-top { margin-bottom: 0.1em; }#dexetera-rugby .canvas-caption-axis { display: flex; justify-content: space-between; padding: 0 60px; margin: 0.1em 0 0.3em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; opacity: 0.6; }</style>
<p class="description">Rugby manager decision support: pick when each home position group comes off the pitch; the simulator (fitted to thousands of real match events) shows how the win-margin distribution shifts. This is a research model fitted to match events, not a rugby manager decision tool.</p>
<div class="dashboard">
    <section class="panel">
        <div class="panel-title">Simulation</div>
        <p class="canvas-caption canvas-caption-top">Score margin (home − away) for the in-progress match</p><canvas width="640" height="400"></canvas><p class="canvas-caption canvas-caption-axis"><span>−50</span><span>−25</span><span>0</span><span>+25</span><span>+50</span></p><p class="canvas-caption">Win-margin distribution across completed matches</p>
        
        <p class="panel-readout" data-readout="match_state">&nbsp;</p>
        
        <p class="panel-readout" data-readout="outcomes">&nbsp;</p>
        
    </section>
    
    <section class="panel">
        <div class="panel-title">Live controls</div>
        
        <label class="slider">
            <span class="slider-name">Front-row sub (min)</span>
            <input type="range" data-slider="front_row"
                   min="0" max="80" step="1" value="55">
            <span class="slider-readout" data-slider-readout="front_row">&nbsp;</span>
        </label>
        
        <label class="slider">
            <span class="slider-name">Back-row sub (min)</span>
            <input type="range" data-slider="back_row"
                   min="0" max="80" step="1" value="50">
            <span class="slider-readout" data-slider-readout="back_row">&nbsp;</span>
        </label>
        
        <label class="slider">
            <span class="slider-name">Halves sub (min)</span>
            <input type="range" data-slider="halves"
                   min="0" max="80" step="1" value="60">
            <span class="slider-readout" data-slider-readout="halves">&nbsp;</span>
        </label>
        
        <label class="slider">
            <span class="slider-name">Outside-backs sub (min)</span>
            <input type="range" data-slider="outside_backs"
                   min="0" max="80" step="1" value="55">
            <span class="slider-readout" data-slider-readout="outside_backs">&nbsp;</span>
        </label>
        
        
        <div class="panel-actions">
            <button type="button" class="button-secondary" data-reset>Reset simulation</button>
        </div>
        
    </section>
    
</div>
<p class="status" data-status>Loading…</p>
</div>
<script>
(function () {
    var widget = document.getElementById('dexetera-rugby');
    var RUNTIME_BASE = 'https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/dexetera/runtime/';
    var WASM_URL = 'https://pub-afdb1348ec964ca5b530aa758c0bdc56.r2.dev/assets/dexetera/widgets/rugby/main.wasm';
    var gameConfig = {"visualization":{"backgroundColor":"#fafafa","canvasHeight":400,"canvasWidth":640,"renderers":[{"partitionName":"","properties":{"color":"#cccccc","dashPattern":[3,3],"width":1,"x1":60,"x2":580,"y1":70,"y2":70},"type":"line"},{"partitionName":"match_state","properties":{"color":"#3c78d8","height":80,"lineWidth":2,"width":520,"x":60,"y":30},"type":"lineChart"},{"partitionName":"","properties":{"color":"#e3e6ec","width":1,"x1":60,"x2":580,"y1":128,"y2":128},"type":"line"},{"partitionName":"","properties":{"color":"#cfd4dc","dashPattern":[2,4],"width":1,"x1":320,"x2":320,"y1":170,"y2":374},"type":"line"},{"partitionName":"histogram_bars","properties":{"anchor":"topLeft","defaultHeight":0,"defaultWidth":0,"fillColor":"#7d8aa1"},"type":"rectangleSet"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":60,"x2":580,"y1":374,"y2":374},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":60,"x2":60,"y1":374,"y2":380},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":190,"x2":190,"y1":374,"y2":380},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":320,"x2":320,"y1":374,"y2":380},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":450,"x2":450,"y1":374,"y2":380},"type":"line"},{"partitionName":"","properties":{"color":"#2c3e50","width":1,"x1":580,"x2":580,"y1":374,"y2":380},"type":"line"}],"updateIntervalMs":0},"sliders":[{"name":"front_row","partition":"home_sub_snapshot","valueIndex":0,"default":55,"decimals":3},{"name":"back_row","partition":"home_sub_snapshot","valueIndex":1,"default":50,"decimals":3},{"name":"halves","partition":"home_sub_snapshot","valueIndex":2,"default":60,"decimals":3},{"name":"outside_backs","partition":"home_sub_snapshot","valueIndex":3,"default":55,"decimals":3}],"readouts":[{"partition":"match_state","template":"match {v7} · min {v6} · home {v1} · away {v2}","decimals":2},{"partition":"outcomes","template":"home win: {v0}% · matches: {v1}","decimals":1}],"showReset":true,"driver":{"kind":"inline","options":{"intervalMs":30}}};

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
                } else if (msg.type === 'status') {
                    setStatus(msg.data);
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
```

The link to this project can be [found here](https://github.com/umbralcalc/trywizard).

**Data and licence:** This is an entirely non-commercial research and learning model, built purely to demonstrate that a simulation can be fit to realistic match-event data. None of the underlying data is redistributed here; the dashboard ships only the fitted model coefficients, not any match records or source data. Unlike the other dashboards in this series there is no open-data licence to cite.