"use strict";
const fs=require("node:fs"),path=require("node:path");
const project=process.argv[2], script=fs.readFileSync(path.join(project,"script.md"),"utf8");
const cfg=JSON.parse(fs.readFileSync(path.join(project,"scene/config.json"),"utf8"));
cfg.duration=87.9061; cfg.fps=30; cfg.width=1920; cfg.height=1080;
fs.writeFileSync(path.join(project,"scene/config.json"),JSON.stringify(cfg,null,2));
fs.copyFileSync(path.join(project,"stage.cjs"),path.join(project,"scene/stage.cjs"));
const words=script.replace(/^#.*$/gm,"").trim().split(/\s+/).filter(Boolean);
const n=words.length, start=0.35, end=cfg.duration-0.45, span=end-start;
const timed=words.map((text,i)=>({text:text.replace(/[^A-Za-z0-9?'-]/g,"")||text,screen:text.replace(/[^A-Za-z0-9?'-]/g,"")||text,start:start+span*i/n,end:start+span*(i+0.92)/n}));
fs.writeFileSync(path.join(project,"scene/word-timings.json"),JSON.stringify({words:timed},null,2));
const groups=[]; for(let i=0;i<n;i+=3){const ids=[i,Math.min(i+1,n-1),Math.min(i+2,n-1)].filter((v,j,a)=>a.indexOf(v)===j);groups.push({lines:[ids],key:ids[0]});}
fs.writeFileSync(path.join(project,"scene/caption-groups.json"),JSON.stringify(groups,null,2));
const frames=Math.round(cfg.duration*cfg.fps), levels=Array.from({length:frames},(_,i)=>0.22+0.2*(0.5+0.5*Math.sin(i/4.7)));
fs.writeFileSync(path.join(project,"scene/speech-levels.json"),JSON.stringify(levels));
console.log(JSON.stringify({project,words:n,duration:cfg.duration,frames}));
