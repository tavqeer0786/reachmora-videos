"use strict";
const fs=require("fs"),path=require("path");
const p=process.argv[2]; let s=fs.readFileSync(p,"utf8");
const start=s.indexOf("function captions(t){"); const end=s.indexOf("function mixColor",start);
if(start<0||end<0)throw Error("caption function not found");
const replacement=`function captions(t){
 let gi=groups.findIndex((g,i)=>t>=words[g.lines[0][0]].start&&(i===groups.length-1?t<DURATION:t<words[groups[i+1].lines[0][0]].start-.015));
 if(gi<0)return ''; let g=groups[gi],html='',base=g.lines.length===3?230:262;
 for(let li=0;li<g.lines.length;li++){
  let x=1270,baseline=base+li*82.4;
  for(let index of g.lines[li]){
   let w=words[index], key=index===g.key, dt=t-w.start;
   if(dt>=0){ let ww=Math.max(38,w.screen.length*31)+(key?24:0), dy=key?0:4*(1-out(dt/.2)), u=clamp(dt/.2), col=key?mixColor('#F6CEC8','#FBFAF8',u):mixColor('#B5AFA7',ink,u), scale=key?.91+.09*(1+2.8*Math.pow(clamp(dt/.23)-1,3)+1.8*Math.pow(clamp(dt/.23)-1,2)):1;
    let elem=\`<text x="\${x+(key?12:0)}" y="\${baseline+dy}" font-family="Arial, sans-serif" font-size="62px" font-weight="700" fill="\${col}">\${w.screen}</text>\`; if(key)elem=\`<rect x="\${x}" y="\${baseline-60}" width="\${ww}" height="75" rx="3" fill="\${red}"/>\`+elem;
    html+=\`<g transform="translate(\${x+ww/2} \${baseline-25}) scale(\${scale}) translate(\${-x-ww/2} \${-baseline+25})">\${elem}</g>\`;
   } x+=ww+13.4;
  }
 }
 return html;
}
`;
s=s.slice(0,start)+replacement+s.slice(end);
s=s.replace('module.exports={frame,presenter,captions,levels,blinks};','module.exports={frame,qualityFrame:t=>frame(t),presenter,captions,levels,blinks,productionAssets:[{path:"assets/rig/spider-approved.svg"}]};');
fs.writeFileSync(p,s);
