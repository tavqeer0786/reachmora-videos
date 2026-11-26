"use strict";
const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process");
const root=process.cwd(), project=path.resolve(process.argv[2]), upstream=path.resolve(process.argv[3]);
const {createCanvas,loadImage}=require(path.join(root,"skills/directing-stickman-videos/node_modules/@napi-rs/canvas"));
const W=1280,H=720,FPS=30,D=94.765737;
const ink="#171319", cream="#fffefa", red="#d7372c", yellow="#f5c84b";
const words=fs.readFileSync(path.join(project,"script.md"),"utf8").replace(/^#.*$/gm,"").trim().split(/\s+/).map(s=>s.replace(/[^A-Za-z0-9?'’-]/g,""));
const clean=words.filter(Boolean), start=.25, span=D-.5;
const timings=clean.map((text,i)=>({text,start:start+span*i/clean.length,end:start+span*(i+1.15)/clean.length}));
const groups=[]; for(let i=0;i<timings.length;i+=4){const g=timings.slice(i,i+4);groups.push({text:g.map(x=>x.text).join(" "),start:g[0].start,end:Math.min(D,g.at(-1).end)});}
function text(ctx,s,x,y,size,color=cream,align="center",stroke=6){ctx.save();ctx.font=`900 ${size}px Arial Black,Arial,sans-serif`;ctx.textAlign=align;ctx.textBaseline="middle";ctx.lineJoin="round";ctx.strokeStyle=ink;ctx.lineWidth=stroke;ctx.strokeText(s,x,y);ctx.fillStyle=color;ctx.fillText(s,x,y);ctx.restore();}
function ease(u){u=Math.max(0,Math.min(1,u));return u*u*(3-2*u)}
function line(ctx,a,b,color=ink,w=9){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=w;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(...a);ctx.lineTo(...b);ctx.stroke();ctx.restore();}
function rounded(ctx,x,y,w,h,fill,stroke=ink,sw=7,r=20){ctx.save();ctx.fillStyle=fill;ctx.strokeStyle=stroke;ctx.lineWidth=sw;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();ctx.stroke();ctx.restore();}
function arrow(ctx,a,b,color=red){line(ctx,a,b,color,10);const ang=Math.atan2(b[1]-a[1],b[0]-a[0]);line(ctx,b,[b[0]-22*Math.cos(ang-.55),b[1]-22*Math.sin(ang-.55)],color,10);line(ctx,b,[b[0]-22*Math.cos(ang+.55),b[1]-22*Math.sin(ang+.55)],color,10);}
async function main(){
 const asset=path.join(upstream,"skills/directing-stickman-videos/assets/b6/paint");
 const imgs={}; for(const k of ["hotel-panorama","hero-body","hero-head","buyer-body","buyer-head","buyer-greedy-head","ink-stroke","hero-hand","shoe-left","shoe-right"]){const file=path.join(asset,`${k}.png`);if(fs.existsSync(file))imgs[k]=await loadImage(file);}
 const out=path.join(project,"frames");fs.mkdirSync(out,{recursive:true});
 const total=Math.round(D*FPS);
 for(let f=0;f<total;f++){
  const t=f/FPS, c=createCanvas(W,H),ctx=c.getContext("2d");
  ctx.fillStyle="#ead9bb";ctx.fillRect(0,0,W,H);
  if(imgs["hotel-panorama"])ctx.drawImage(imgs["hotel-panorama"],0,0,W,H);
  ctx.fillStyle="#17131928";ctx.fillRect(0,0,W,H);
  const section=t<18?0:t<38?1:t<58?2:t<77?3:4;
  if(section===0){rounded(ctx,70,160,310,215,"#f7f1e7");text(ctx,"ONE SHOPPING TRIP?",225,205,28,red);text(ctx,"TV",150,290,32,ink);text(ctx,"TOYS",245,290,32,ink);text(ctx,"GROCERIES",315,330,25,ink);arrow(ctx,[410,270],[560,270],yellow);rounded(ctx,600,170,350,205,"#f7f1e7");text(ctx,"CONVENIENCE",775,225,34,red);text(ctx,"+ SCALE",775,285,48,ink);}
  if(section===1){rounded(ctx,55,145,250,240,"#f7f1e7");rounded(ctx,515,145,250,240,"#f7f1e7");rounded(ctx,975,145,250,240,"#f7f1e7");text(ctx,"STORE",180,205,32,red);text(ctx,"WEBSITE",640,205,32,red);text(ctx,"APP",1100,205,32,red);text(ctx,"PICKUP",180,300,28,ink);text(ctx,"DELIVERY",640,300,28,ink);text(ctx,"AVAILABILITY",1100,300,25,ink);arrow(ctx,[305,265],[505,265],yellow);arrow(ctx,[765,265],[965,265],yellow);}
  if(section===2){text(ctx,"HOLIDAY LIST",230,140,42,red);const list=["TELEVISION","TOYS","SNACKS","BATTERIES","DECORATIONS"];list.forEach((s,i)=>{rounded(ctx,80,190+i*65,310,48,"#f7f1e7");text(ctx,"✓  "+s,235,214+i*65,24,ink);});rounded(ctx,500,175,570,245,"#f7f1e7");text(ctx,"MANY NEEDS",785,225,42,red);text(ctx,"ONE ECOSYSTEM",785,300,42,ink);arrow(ctx,[400,330],[500,300],yellow);}
  if(section===3){rounded(ctx,90,155,420,230,"#f7f1e7");text(ctx,"ONLINE",300,205,34,red);text(ctx,"CHECK STOCK",300,270,28,ink);text(ctx,"CHOOSE DELIVERY",300,330,28,ink);rounded(ctx,760,155,420,230,"#f7f1e7");text(ctx,"IN STORE",970,205,34,red);text(ctx,"ONE TRIP",970,270,30,ink);text(ctx,"MANY ITEMS",970,330,30,ink);arrow(ctx,[520,270],[745,270],yellow);}
  if(section===4){rounded(ctx,120,155,340,245,"#f7f1e7");rounded(ctx,820,155,340,245,"#f7f1e7");text(ctx,"FIRST EVENT",290,215,34,red);text(ctx,"DIDN'T FIND IT",290,285,27,ink);text(ctx,"SECOND EVENT",990,215,34,red);text(ctx,"REASON TO RETURN",990,285,27,ink);arrow(ctx,[465,275],[815,275],yellow);text(ctx,"ONE PURCHASE  →  A HABIT?",640,500,38,cream);}
  // B6 painted characters, staged as moving meme commentators.
  const bob=Math.sin(t*3)*3, hx=section===4?360:270+Math.sin(t*.7)*25, bx=section===4?900:1010+Math.sin(t*.8+1)*20;
  if(imgs["hero-body"]){ctx.drawImage(imgs["hero-body"],hx-115,440+bob,230,235);ctx.drawImage(imgs[t>78?"buyer-greedy-head":"hero-head"],hx-150,275+bob,300,205);}
  if(imgs["buyer-body"]){ctx.drawImage(imgs["buyer-body"],bx-115,440-bob,230,235);ctx.drawImage(imgs[section===4?"buyer-greedy-head":"buyer-head"],bx-150,275-bob,300,205);}
  const cue=groups.find(g=>t>=g.start&&t<g.end); if(cue)text(ctx,cue.text.toUpperCase(),W/2,650,29,cream);
  fs.writeFileSync(path.join(out,String(f).padStart(6,"0")+".png"),c.toBuffer("image/png"));
 }
 const video=path.join(project,"walmart-black-friday-chapter-2-b6.mp4");
 cp.execFileSync("ffmpeg",["-y","-framerate",String(FPS),"-i",path.join(out,"%06d.png"),"-i",path.join(project,"voiceover.mp3"),"-t",String(D),"-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-c:a","aac","-b:a","192k","-shortest",video],{stdio:"inherit"});
 fs.writeFileSync(path.join(project,"render.json"),JSON.stringify({style:"B6 Meme Story Animation",duration:D,fps:FPS,voiceover:"ch-2.mp3",renderer:"GitHub Actions CPU",visuals:"B6 painted characters and world assets with Walmart-specific metaphors"},null,2));
}
main().catch(e=>{console.error(e);process.exit(1)});
