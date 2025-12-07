import React,

{useState, useMemo}
from

'react';
import

{LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine}
from

'recharts';
import

{Play, RefreshCw}
from

'lucide-react';

const
MonteCarloSimulator = () = > {
    const[params, setParams] = useState({
    S0: 100,
    mu: 0.00,
    sigma: 0.20,
    T: 1.0,
    nPaths: 100,
    nSteps: 252
});

const[showPaths, setShowPaths] = useState(false);

// Generate
Monte
Carlo
paths
const
{paths, terminal} = useMemo(() = > {
if (!showPaths)
return {paths: [], terminal: []};

const
{S0, mu, sigma, T, nPaths, nSteps} = params;
const
dt = T / nSteps;
const
sqrtDt = Math.sqrt(dt);

const
allPaths = [];
const
terminalPrices = [];

for (let p = 0; p < nPaths; p++) {
    let S = S0;
const path =[{step: 0, price: S, path: p}];

for (let i = 1; i <= nSteps; i++) {
    const Z = Math.sqrt(-2 * Math.log(Math.random())) * Math.cos(2 * Math.PI * Math.random());
S = S * Math.exp((mu - 0.5 * sigma ** 2) * dt + sigma * sqrtDt * Z);
path.push({step: i, price: S, path: p});
}

allPaths.push(path);
terminalPrices.push(S);
}

return {paths: allPaths, terminal: terminalPrices};
}, [params, showPaths]);

// Aggregate
data
for chart(show every Nth step for performance)
const chartData = useMemo(() = > {
if (paths.length === 0) return[];

const
stepInterval = Math.max(1, Math.floor(params.nSteps / 50));
const
data = [];

for (let i = 0; i <= params.nSteps; i += stepInterval) {
    const point = {step: i};
paths.forEach((path, idx) = > {
if (idx < 20)
{ // Show
first
20
paths in chart
point[`path${idx}
`] = path[i].price;
}
});
data.push(point);
}

return data;
}, [paths, params.nSteps]);

// Calculate
statistics
const
stats = useMemo(() = > {
if (terminal.length === 0) return null;

const
sorted = [...terminal].sort((a, b) = > a - b);
const
mean = terminal.reduce((a, b) = > a + b, 0) / terminal.length;
const
variance = terminal.reduce((a, b) = > a + (b - mean) ** 2, 0) / terminal.length;
const
std = Math.sqrt(variance);

return {
    mean: mean.toFixed(2),
    std: std.toFixed(2),
    min: sorted[0].toFixed(2),
    max: sorted[sorted.length - 1].toFixed(2),
    p5: sorted[Math.floor(sorted.length * 0.05)].toFixed(2),
    p95: sorted[Math.floor(sorted.length * 0.95)].toFixed(2)
};
}, [terminal]);

const
runSimulation = () = > {
    setShowPaths(false);
setTimeout(() = > setShowPaths(true), 10);
};

return (
    < div className="w-full h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-6 overflow-auto" >
    < div className="max-w-7xl mx-auto" >
    < h1 className="text-3xl font-bold text-white mb-6" > Monte Carlo Stock Price Simulation < / h1 >

    {/ * Controls * /}
    < div className="bg-slate-800 rounded-lg p-6 mb-6 shadow-xl border border-slate-700" >
    < div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-4" >
    < div >
    < label className="text-slate-300 text-sm block mb-1" > Initial Price (S₀) < / label >
                                                                                   < input
type = "number"
value = {params.S0}
onChange = {(e) = > setParams({...
params, S0: parseFloat(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < div >
                < label
className = "text-slate-300 text-sm block mb-1" > Drift(μ) < / label >
                                                               < input
type = "number"
step = "0.01"
value = {params.mu}
onChange = {(e) = > setParams({...
params, mu: parseFloat(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < div >
                < label
className = "text-slate-300 text-sm block mb-1" > Volatility(σ) < / label >
                                                                    < input
type = "number"
step = "0.01"
value = {params.sigma}
onChange = {(e) = > setParams({...
params, sigma: parseFloat(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < div >
                < label
className = "text-slate-300 text-sm block mb-1" > Time(T
years) < / label >
           < input
type = "number"
step = "0.1"
value = {params.T}
onChange = {(e) = > setParams({...
params, T: parseFloat(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < div >
                < label
className = "text-slate-300 text-sm block mb-1" > Paths < / label >
                                                            < input
type = "number"
value = {params.nPaths}
onChange = {(e) = > setParams({...
params, nPaths: parseInt(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < div >
                < label
className = "text-slate-300 text-sm block mb-1" > Steps < / label >
                                                            < input
type = "number"
value = {params.nSteps}
onChange = {(e) = > setParams({...
params, nSteps: parseInt(e.target.value)})}
className = "w-full bg-slate-700 text-white px-3 py-2 rounded border border-slate-600"
            / >
            < / div >
                < / div >

                    < button
onClick = {runSimulation}
className = "bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition-colors"
            >
            {showPaths ? < RefreshCw
size = {20} / >: < Play
size = {20} / >}
{showPaths ? 'Re-run Simulation': 'Run Simulation'}
< / button >
    < / div >

        { / * Chart * /}
{showPaths & & (
    <>
    < div className="bg-slate-800 rounded-lg p-6 mb-6 shadow-xl border border-slate-700" >
    < h2 className="text-xl font-semibold text-white mb-4" > Price Paths (showing first 20) < / h2 >
< ResponsiveContainer
width = "100%"
height = {400} >
         < LineChart
data = {chartData} >
       < CartesianGrid
strokeDasharray = "3 3"
stroke = "#334155" / >
         < XAxis
dataKey = "step"
stroke = "#94a3b8"
label = {{value: 'Time Steps', position: 'insideBottom', offset: -5, fill: '#94a3b8'}}
        / >
        < YAxis
stroke = "#94a3b8"
label = {{value: 'Price', angle: -90, position: 'insideLeft', fill: '#94a3b8'}}
        / >
        < Tooltip
contentStyle = {{backgroundColor: '#1e293b', border: '1px solid #475569'}}
labelStyle = {{color: '#cbd5e1'}}
             / >
             < ReferenceLine
y = {params.S0}
stroke = "#ef4444"
strokeDasharray = "5 5" / >
                  {Array.
from

({length: Math.min(20, params.nPaths)}, (_, i) = > (
< Line
key={i}
type="monotone"
dataKey={`path${i}`}
stroke={`hsl(${(i * 360) / 20}, 70 %, 60 %)`}
dot = {false}
strokeWidth = {1.5}
strokeOpacity = {0.6}
                / >
))}
< / LineChart >
    < / ResponsiveContainer >
        < / div >

            { / * Statistics * /}
< div
className = "bg-slate-800 rounded-lg p-6 shadow-xl border border-slate-700" >
            < h2
className = "text-xl font-semibold text-white mb-4" > Terminal
Price
Statistics < / h2 >
               < div
className = "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4" >
            < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > Mean < / div >
                                                < div
className = "text-2xl font-bold text-white" >${stats.mean} < / div >
                                                               < / div >
                                                                   < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > Std
Dev < / div >
        < div
className = "text-2xl font-bold text-white" >${stats.std} < / div >
                                                              < / div >
                                                                  < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > Min < / div >
                                               < div
className = "text-2xl font-bold text-red-400" >${stats.min} < / div >
                                                                < / div >
                                                                    < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > Max < / div >
                                               < div
className = "text-2xl font-bold text-green-400" >${stats.max} < / div >
                                                                  < / div >
                                                                      < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > 5
th % ile < / div >
             < div
className = "text-2xl font-bold text-orange-400" >${stats.p5} < / div >
                                                                  < / div >
                                                                      < div
className = "bg-slate-700 p-4 rounded" >
            < div
className = "text-slate-400 text-sm" > 95
th % ile < / div >
             < div
className = "text-2xl font-bold text-cyan-400" >${stats.p95} < / div >
                                                                 < / div >
                                                                     < / div >
                                                                         < / div >
                                                                             < / >
)}
< / div >
    < / div >
);
};

export
default
MonteCarloSimulator;