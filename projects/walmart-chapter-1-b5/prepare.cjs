"use strict";
const fs=require("fs"),path=require("path"),{spawnSync}=require("child_process");
const dir=__dirname, text=fs.readFileSync(path.join(dir,"script.md"),"utf8").replace(/^#.*$/gm,"").trim();
const sentences=text.split(/(?<=[.!?])\s+/).filter(Boolean), duration=87.9061, words=[]; let all=[];
for(const sentence of sentences) all=all.concat(sentence.replace(/[—–]/g," ").match(/[A-Za-z0-9+']+/g)||[]);
const step=duration/all.length; all.forEach((w,i)=>words.push({text:w,start:i*step,end:(i+1)*step-.01,screen:w.toUpperCase()}));
const groups=[]; let i=0; for(const sentence of sentences){const count=(sentence.match(/[A-Za-z0-9+']+/g)||[]).length, ids=Array.from({length:count},(_,j)=>i+j); const lines=[]; for(let j=0;j<ids.length;j+=4)lines.push(ids.slice(j,j+4)); groups.push({key:ids[Math.min(1,ids.length-1)],lines}); i+=count;}
fs.writeFileSync(path.join(dir,"word-timings.json"),JSON.stringify({words},null,2)); fs.writeFileSync(path.join(dir,"caption-groups.json"),JSON.stringify(groups,null,2)); fs.writeFileSync(path.join(dir,"speech-levels.json"),JSON.stringify(Array.from({length:Math.ceil(duration*30)},(_,n)=>.18+.12*Math.abs(Math.sin(n*.19))));
