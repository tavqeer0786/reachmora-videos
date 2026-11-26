"use strict";
const fs=require("node:fs"),path=require("node:path"),cp=require("node:child_process");
const [dir,audio,script,chapter]=process.argv.slice(2);
if(!dir||!audio||!script)throw new Error("usage: prepare-project.cjs PROJECT AUDIO SCRIPT CHAPTER");
const probe=JSON.parse(cp.execFileSync("ffprobe",["-v","error","-show_format","-of","json",audio],{encoding:"utf8"}));
const duration=Number(probe.format.duration),W=1280,H=720,FPS=30;
const bed=path.join(dir,"room-tone.wav");
cp.execFileSync("ffmpeg",["-y","-f","lavfi","-i",`anoisesrc=color=pink:amplitude=0.003:duration=${duration.toFixed(3)}:sample_rate=48000`,"-c:a","pcm_s16le",bed],{stdio:"ignore"});
const raw=fs.readFileSync(script,"utf8").replace(/^#.*$/gm,"").replace(/\*\*/g,"").trim();
const words=raw.split(/\s+/).filter(Boolean).map(x=>x.replace(/[^A-Za-z0-9?'’-]/g,""));
const clean=words.filter(Boolean), captions=[];
const group=5, usable=duration-.35;
for(let i=0;i<clean.length;i+=group){const arr=clean.slice(i,i+group),start=.18+usable*i/clean.length,end=Math.min(duration,start+usable*arr.length/clean.length*.98);captions.push({start:Number(start.toFixed(3)),end:Number(Math.max(start+.18,end).toFixed(3)),text:arr.join(" ")});}
function text(s,x=86,y=70,size=52,color="#191916",w=1080){return {type:"text",text:s,x,y,size,color,w,bold:true};}
function img(path,x,y,w,keys=[]){return {type:"image",path,x,y,w,keys};}
function pose(n,x=730,y=25,w=420,keys=[]){return {type:"pose",pose:n,x,y,w,keys};}
function arrow(x,y,w,color="#EC4338"){return {type:"arrow",x,y,w,color,lineWidth:5,keys:[{t:0,progress:0},{t:.45,progress:1}]};}
function line(x,y,points,color="#191916",lineWidth=4){return {type:"line",x,y,points,color,lineWidth};}
const assets={cal:"@b1/calendar-crayon.png",tv:"@b1/camera-handdrawn.png",note:"@b1/idea-note-crayon.png",bulb:"@b1/idea-bulb-crayon.png",clap:"@b1/clapper-crayon.png",script:"@b1/script-page-crayon.png",open:"@b1/open-source-crayon.png",yt:"@b1/youtube-crayon.png"};
function shot(i,start,end){
 const t=i%10, S=[];
 const span=end-start;
 const titles=chapter==="1"?["ONE SHOPPING DAY","THE LIST KEEPS GROWING","PEOPLE BUY IN STAGES","THE SEASON COMES IN WAVES","A SECOND CHANCE","NOT EVERYONE IS READY","ANOTHER REASON TO LOOK","BLACK FRIDAY ISN'T THE FINISH","MORE THAN ONE MOMENT","THE QUESTION"]:["PRICE IS ONLY ONE PART","A STORE AND A SCREEN","THE HOLIDAY LIST","MANY NEEDS. ONE TRIP.","CHECK STOCK FIRST","PICKUP OR DELIVERY","THE SAME SHOPPING SYSTEM","ONE BASKET, MANY DECISIONS","CONVENIENCE HAS A JOB","THE NEXT VISIT"];
 S.push(text(titles[t],86,58,t===0?56:50,t%3===0?"#EC4338":"#191916"));
 const motionKeys=[{t:0,y:35,angle:-.015},{t:Math.min(.7,span-.5),y:25,angle:.012},{t:Math.min(1.4,span-.35),y:35,angle:-.01},{t:Math.min(2.1,span-.2),y:25,angle:.01},{t:Math.max(2.2,span-.05),y:35,angle:-.015}].filter((k,i,a)=>i===0||k.t>a[i-1].t&&k.t<span);
 S.push(pose((i+t)%3,720,15,430,motionKeys));
 if(t===0){S.push(img(assets.cal,90,265,190),img(assets.tv,330,280,180),arrow(520,370,250,"#EC4338"),img(assets.note,815,270,220));}
 if(t===1){S.push(img(assets.note,90,250,220),img(assets.bulb,390,260,180),line(620,370,[[0,0],[220,-40],[410,25]],"#EC4338",5),img(assets.cal,940,250,180));}
 if(t===2){S.push(img(assets.tv,100,260,180),img(assets.note,360,270,190),img(assets.clap,650,260,190),img(assets.script,940,250,190));}
 if(t===3){S.push(img(assets.cal,90,250,180),line(310,360,[[0,0],[165,0],[330,-90],[500,0]],"#EC4338",6),img(assets.clap,855,255,190));}
 if(t===4){S.push(img(assets.clap,100,270,190),arrow(355,370,220),img(assets.note,650,260,200),text("ANOTHER LOOK",700,490,36,"#EC4338",500));}
 if(t===5){S.push(img(assets.tv,100,270,170),img(assets.note,370,260,190),text("NOT READY",640,300,44,"#EC4338",300),line(620,365,[[0,0],[240,0]],"#191916",4));}
 if(t===6){S.push(img(assets.open,90,250,210),img(assets.script,385,250,190),arrow(620,375,220),img(assets.cal,930,255,180));}
 if(t===7){S.push(img(assets.clap,100,250,190),img(assets.cal,380,250,170),line(600,370,[[0,0],[180,0],[330,-65],[480,0]],"#EC4338",6),text("STILL SHOPPING",650,500,36,"#191916",500));}
 if(t===8){S.push(img(assets.note,90,250,190),img(assets.bulb,390,250,180),img(assets.tv,700,270,180),arrow(900,370,180));}
 if(t===9){S.push(img(assets.open,90,250,190),img(assets.yt,400,270,180),line(640,375,[[0,0],[240,0]],"#EC4338",5),text(chapter==="1"?"WHY COME BACK?":"WHAT KEEPS THEM?",720,510,38,"#EC4338",650));}
 return {start,end,layers:S};
}
const shots=[], count=Math.ceil(duration/3.2);
for(let i=0;i<count;i++){const start=Number((i*duration/count).toFixed(3)),end=i===count-1?duration:Number(((i+1)*duration/count).toFixed(3));shots.push(shot(i,start,end));}
const project={version:1,style:"B1",width:W,height:H,fps:FPS,voice:{path:"narration.mp3",lead:0,tail:0,contains_sfx:false},ambience:[{path:"room-tone.wav",start:0,end:duration,gain:.03,offset:0,loop:true,fadeIn:1,fadeOut:1}],captions,shots,sfx:shots.map((s,i)=>({time:Number((s.start+.25).toFixed(3)),kind:i%3===0?"paper":"tap",gain:.12})),reference_review:{author_id:"codex",capability:{mode:"sample_target",environment:"GitHub Actions CPU with upstream B1 autopilot renderer",limitations:[]}},metadata:{chapter,source_script:path.basename(script)}};
fs.mkdirSync(dir,{recursive:true});fs.writeFileSync(path.join(dir,"project.json"),JSON.stringify(project,null,2));
console.log(JSON.stringify({dir,duration,words:clean.length,shots:shots.length,captions:captions.length}));
