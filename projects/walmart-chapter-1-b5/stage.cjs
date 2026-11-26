"use strict";
const INK="#1E1C1A", RED="#D7372C", BLUE="#4E7180", GOLD="#E2A84E", PAPER="#EBE7E1";
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const ease=u=>{u=clamp(u);return u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2};
const txt=(x,y,s,size=44,color=INK,anchor="middle")=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Arial, sans-serif" font-size="${size}px" font-weight="700" fill="${color}">${esc(s)}</text>`;
function tv(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><rect x="-120" y="-74" width="240" height="150" rx="10" fill="#344B5C" stroke="${INK}" stroke-width="8"/><rect x="-98" y="-52" width="196" height="108" fill="#8FC9D8" stroke="${INK}" stroke-width="5"/><path d="M-58 96H58M0 76V96" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>${txt(0,15,"TV",40,"#fff")}</g>`}
function toy(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><circle r="74" fill="#D7372C" stroke="${INK}" stroke-width="8"/><circle cx="-25" cy="-10" r="10" fill="#fff"/><circle cx="25" cy="-10" r="10" fill="#fff"/><path d="M-30 28Q0 54 30 28" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>${txt(0,125,"TOYS",25,INK)}</g>`}
function box(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-115-58L0-105 115-58 0-12Z M-115-58V65L0 113V-12 M115-58V65L0 113" fill="${GOLD}" stroke="${INK}" stroke-width="8"/>${txt(0,8,"LATER",22,INK)}</g>`}
function store(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-170-70L0-145 170-70V120H-170Z" fill="#F4F1EA" stroke="${INK}" stroke-width="8"/><path d="M-185-82H185V-28H-185Z" fill="${RED}" stroke="${INK}" stroke-width="8"/>${txt(0,-42,"WALMART",32,"#fff")}<rect x="-45" y="18" width="90" height="102" fill="#8FC9D8" stroke="${INK}" stroke-width="8"/>${txt(0,165,"RETURN",24,INK)}</g>`}
function cart(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-120-70H110L75 20H-80Z" fill="#F4F1EA" stroke="${INK}" stroke-width="8"/><circle cx="-45" cy="60" r="18" fill="#444"/><circle cx="65" cy="60" r="18" fill="#444"/><path d="M-145-105L-120-70" stroke="${INK}" stroke-width="10" stroke-linecap="round"/>${txt(0,-18,"SHOP",30,INK)}</g>`}
function scene(t){
 let a="";
 if(t<10){a=store(430,610,.72)+cart(760,640,.8)+tv(1010,600,.62);}
 else if(t<22){let u=ease((t-10)/12);a=tv(340,610,.65)+toy(650,590,.56)+box(960,615,.65)+txt(650,280,"NOVEMBER",48,RED)+txt(650,340,"LATER",48,INK);}
 else if(t<34){a=cart(530,640,.82)+box(880,620,.76)+txt(700,280,"ONE DAY",56,RED)+txt(700,350,"ONE DECISION",45,INK);}
 else if(t<47){a=store(520,610,.78)+box(850,615,.70)+txt(690,260,"SECOND EVENT",54,RED)+txt(690,330,"SECOND CHANCE",44,INK);}
 else if(t<61){a=store(380,610,.56)+store(760,610,.56)+store(1140,610,.56)+txt(760,245,"A SEASON OF",48,RED)+txt(760,310,"OPPORTUNITIES",48,INK);}
 else if(t<74){a=store(430,620,.6)+tv(760,600,.55)+toy(1060,610,.48)+txt(760,250,"STAY VISIBLE",56,RED);}
 else {a=store(300,620,.5)+txt(690,260,"AMAZON",44,INK)+txt(690,330,"TARGET",44,INK)+txt(690,400,"WALMART?",54,RED)+cart(1000,640,.62);}
 return `<g><path d="M90 760H1220" stroke="#C7BFB7" stroke-width="6"/><path d="M90 820H1220M90 880H1220M90 940H1220" stroke="#D8D0C8" stroke-width="3"/><circle cx="1100" cy="200" r="110" fill="#F4C96B" opacity=".28"/>${a}</g>`;
}
module.exports={draw:scene,inspect:()=>[],events:[]};
