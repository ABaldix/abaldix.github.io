// Shared state data for VivaVoltia calculators.
// code: [name, avg residential price $/kWh (EIA, Aug 2026), peak sun hours (NREL, rounded), typical export credit as share of retail]
window.VV_STATES = {
            AL: ["Alabama", 0.163, 4.8, 1],
            AK: ["Alaska", 0.294, 2.9, 1],
            AZ: ["Arizona", 0.151, 6.3, 0.5],
            AR: ["Arkansas", 0.144, 4.7, 1],
            CA: ["California", 0.298, 5.8, 0.25],
            CO: ["Colorado", 0.172, 5.4, 1],
            CT: ["Connecticut", 0.245, 4.0, 1],
            DE: ["Delaware", 0.187, 4.4, 1],
            DC: ["District of Columbia", 0.260, 4.4, 1],
            FL: ["Florida", 0.150, 5.2, 1],
            GA: ["Georgia", 0.159, 4.9, 0.5],
            HI: ["Hawaii", 0.472, 5.6, 0.25],
            ID: ["Idaho", 0.134, 4.8, 0.5],
            IL: ["Illinois", 0.193, 4.2, 0.5],
            IN: ["Indiana", 0.170, 4.2, 0.5],
            IA: ["Iowa", 0.171, 4.3, 1],
            KS: ["Kansas", 0.155, 5.0, 1],
            KY: ["Kentucky", 0.138, 4.3, 0.5],
            LA: ["Louisiana", 0.129, 4.9, 0.5],
            ME: ["Maine", 0.321, 4.0, 1],
            MD: ["Maryland", 0.214, 4.4, 1],
            MA: ["Massachusetts", 0.305, 4.1, 1],
            MI: ["Michigan", 0.230, 3.9, 0.5],
            MN: ["Minnesota", 0.172, 4.3, 1],
            MS: ["Mississippi", 0.144, 4.8, 0.5],
            MO: ["Missouri", 0.160, 4.6, 0.6],
            MT: ["Montana", 0.156, 4.4, 1],
            NE: ["Nebraska", 0.135, 4.8, 1],
            NV: ["Nevada", 0.127, 6.1, 0.75],
            NH: ["New Hampshire", 0.276, 4.0, 0.75],
            NJ: ["New Jersey", 0.246, 4.3, 1],
            NM: ["New Mexico", 0.165, 6.2, 1],
            NY: ["New York", 0.286, 3.9, 1],
            NC: ["North Carolina", 0.149, 4.8, 0.75],
            ND: ["North Dakota", 0.133, 4.4, 0.5],
            OH: ["Ohio", 0.194, 4.0, 0.75],
            OK: ["Oklahoma", 0.148, 5.2, 0.5],
            OR: ["Oregon", 0.159, 4.2, 1],
            PA: ["Pennsylvania", 0.218, 4.0, 1],
            RI: ["Rhode Island", 0.282, 4.1, 1],
            SC: ["South Carolina", 0.158, 4.9, 0.75],
            SD: ["South Dakota", 0.152, 4.7, 0.5],
            TN: ["Tennessee", 0.134, 4.6, 0.5],
            TX: ["Texas", 0.159, 5.3, 0.5],
            UT: ["Utah", 0.133, 5.5, 0.5],
            VT: ["Vermont", 0.238, 3.9, 1],
            VA: ["Virginia", 0.176, 4.6, 1],
            WA: ["Washington", 0.146, 3.6, 1],
            WV: ["West Virginia", 0.163, 4.1, 1],
            WI: ["Wisconsin", 0.194, 4.1, 0.75],
            WY: ["Wyoming", 0.144, 5.0, 0.75]
};
// States with a full "Is solar worth it" guide (slug under /articles/)
window.VV_GUIDES = {CA: "is-solar-worth-it-california", TX: "is-solar-worth-it-texas", FL: "is-solar-worth-it-florida", AZ: "is-solar-worth-it-arizona", NY: "is-solar-worth-it-new-york", NJ: "is-solar-worth-it-new-jersey", MA: "is-solar-worth-it-massachusetts", NC: "is-solar-worth-it-north-carolina", CO: "is-solar-worth-it-colorado", IL: "is-solar-worth-it-illinois", NV: "is-solar-worth-it-nevada", GA: "is-solar-worth-it-georgia", PA: "is-solar-worth-it-pennsylvania", VA: "is-solar-worth-it-virginia", MD: "is-solar-worth-it-maryland", SC: "is-solar-worth-it-south-carolina", UT: "is-solar-worth-it-utah", MI: "is-solar-worth-it-michigan", CT: "is-solar-worth-it-connecticut", HI: "is-solar-worth-it-hawaii", OH: "is-solar-worth-it-ohio", WA: "is-solar-worth-it-washington", OR: "is-solar-worth-it-oregon", MN: "is-solar-worth-it-minnesota", NM: "is-solar-worth-it-new-mexico", WI: "is-solar-worth-it-wisconsin", MO: "is-solar-worth-it-missouri"};
// Fill a <select> with all states, sorted by name
window.vvFillStates = function (sel) {
    var S = window.VV_STATES;
    Object.keys(S).sort(function (a, b) { return S[a][0].localeCompare(S[b][0]); }).forEach(function (c) {
        var o = document.createElement("option"); o.value = c; o.textContent = S[c][0]; sel.appendChild(o);
    });
};
