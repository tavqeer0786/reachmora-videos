"use strict";
const INK="#1E1C1A", RED="#D7372C", BLUE="#5A91A5", GOLD="#E7AA45", PAPER="#F7F3ED";
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const smooth=(t,a,b)=>{const u=clamp((t-a)/(b-a));return u*u*(3-2*u)};
const P=(d,color=INK,width=7,extra="")=>`<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const T=(x,y,s,size=34,color=INK,anchor="middle")=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="Arial, sans-serif" font-size="${size}px" font-weight="800" fill="${color}">${esc(s)}</text>`;
function tv(x,y,s=1,alpha=1){return `<g transform="translate(${x} ${y}) scale(${s})" opacity="${alpha}"><rect x="-105" y="-70" width="210" height="140" rx="10" fill="${BLUE}" stroke="${INK}" stroke-width="8"/><rect x="-82" y="-48" width="164" height="94" fill="#C7E4EA" stroke="${INK}" stroke-width="6"/><path d="M-48 84H48M0 72V96" stroke="${INK}" stroke-width="10" stroke-linecap="round"/></g>`;}
function toy(x,y,s=1,alpha=1){return `<g transform="translate(${x} ${y}) scale(${s})" opacity="${alpha}"><circle r="68" fill="${RED}" stroke="${INK}" stroke-width="8"/><circle cx="-24" cy="-10" r="9" fill="#fff"/><circle cx="24" cy="-10" r="9" fill="#fff"/><path d="M-28 30Q0 54 28 30" fill="none" stroke="${INK}" stroke-width="8"/></g>`;}
function box(x,y,s=1,alpha=1){return `<g transform="translate(${x} ${y}) scale(${s})" opacity="${alpha}"><path d="M-100-55L0-96 100-55 0-14Z M-100-55V58L0 100V-14 M100-55V58L0 100" fill="${GOLD}" stroke="${INK}" stroke-width="8"/></g>`;}
function store(x,y,s=1,alpha=1){return `<g transform="translate(${x} ${y}) scale(${s})" opacity="${alpha}"><path d="M-150-56L0-132 150-56V112H-150Z" fill="${PAPER}" stroke="${INK}" stroke-width="8"/><path d="M-165-66H165V-16H-165Z" fill="${RED}" stroke="${INK}" stroke-width="8"/>${T(0,-28,"WALMART",28,"#fff")}<rect x="-38" y="20" width="76" height="92" fill="#C7E4EA" stroke="${INK}" stroke-width="8"/></g>`;}
function clock(x,y,s=1){return `<g transform="translate(${x} ${y}) scale(${s})"><circle r="58" fill="#fff" stroke="${INK}" stroke-width="8"/><path d="M0 0V-30M0 0L24 18" stroke="${INK}" stroke-width="8" stroke-linecap="round"/>${T(0,92,"WAIT",24,RED)}</g>`;}
function draw(t){
 const bg=`<rect x="0" y="0" width="1220" height="790" rx="18" fill="#F7F3ED" opacity=".72"/><path d="M40 790H1180" stroke="#BDB5AE" stroke-width="5"/><path d="M40 720H1180M40 650H1180" stroke="#DDD5CE" stroke-width="3"/>`;
 let art="", labels="";
 if(t<10){const u=smooth(t,0,3); art=`${store(300,470,.9,u)}${box(690,610,.75,u)}${clock(930,300,.75)}`; labels=`${T(300,180,"ONE BIG DAY",58,RED)}${T(300,235,"IS NOT THE WHOLE SEASON",38,INK)}`;}
 else if(t<20){const u=smooth(t,10,13);art=`${tv(220,470,.72,u)}${toy(550,470,.72,u)}${box(860,540,.72,u)}${store(1050,505,.55,u)}`;labels=`${T(260,170,"NOVEMBER",36,INK)}${T(580,170,"LATER",36,INK)}${T(900,170,"BEFORE CHRISTMAS",36,INK)}`;}
 else if(t<31){const u=smooth(t,20,23);art=`${store(350,500,.82,u)}${clock(760,300,.7)}${box(970,590,.75,u)}`;labels=`${T(460,180,"ONE DAY",58,RED)}${T(460,235,"ONE DECISION",42,INK)}${P("M760 380L760 540",RED,9,"stroke-dasharray=\"18 16\"")}`;}
 else if(t<42){const u=smooth(t,31,34);art=`${store(400,500,.82,u)}${box(760,570,.7,u)}${P("M820 570Q980 430 1110 500",RED,10)}${toy(1090,500,.55,u)}`;labels=`${T(430,175,"SECOND EVENT",54,RED)}${T(430,230,"SECOND CHANCE",40,INK)}`;}
 else if(t<54){const u=smooth(t,42,45);art=`${box(220,570,.6,u)}${store(490,500,.68,u)}${tv(760,480,.55,u)}${toy(1030,500,.5,u)}`;labels=`${T(430,175,"A SERIES OF",44,INK)}${T(430,225,"SHOPPING MOMENTS",50,RED)}`;}
 else if(t<65){const u=smooth(t,54,57);art=`${store(390,500,.78,u)}${P("M540 430Q760 260 1010 430",BLUE,12)}${box(800,520,.68,u)}${tv(1040,520,.5,u)}`;labels=`${T(470,175,"STAY VISIBLE",58,RED)}${T(470,230,"WHILE DECISIONS HAPPEN",36,INK)}`;}
 else if(t<77){const u=smooth(t,65,68);art=`${store(240,510,.56,u)}${store(600,510,.56,u)}${store(960,510,.56,u)}${P("M340 520H500M700 520H860",RED,9,"stroke-dasharray=\"22 14\"")}`;labels=`${T(600,175,"CUSTOMERS CAN SHOP",48,INK)}${T(600,230,"ALMOST ANYWHERE",56,RED)}${T(240,675,"WALMART",28,INK)}${T(600,675,"AMAZON",28,INK)}${T(960,675,"TARGET",28,INK)}`;}
 else {const u=smooth(t,77,80);art=`${store(570,500,.85,u)}${box(830,600,.65,u)}${P("M830 580Q720 360 620 300",RED,10)}`;labels=`${T(560,175,"WHY WALMART?",60,RED)}${T(560,235,"THE NEXT CHOICE",42,INK)}`;}
 return bg+art+labels;
}
module.exports={draw,inspect:()=>[],events:[]};
